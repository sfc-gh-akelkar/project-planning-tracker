"""
Export Utilities Module
Handles exporting data to various formats including Excel and HTML one-pagers.
"""

import io
from datetime import datetime


def export_to_excel(df):
    """
    Export use cases dataframe to Excel format.
    
    Args:
        df: DataFrame with use cases
    
    Returns:
        Bytes object containing Excel file
    """
    try:
        import pandas as pd
        
        # Create a copy and flatten lists for Excel
        export_df = df.copy()
        
        # Convert list columns to comma-separated strings
        if 'participating_companies' in export_df.columns:
            export_df['participating_companies'] = export_df['participating_companies'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) else x
            )
        
        if 'tags' in export_df.columns:
            export_df['tags'] = export_df['tags'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) else x
            )
        
        # Create Excel file in memory
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='Use Cases', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Use Cases']
            for idx, col in enumerate(export_df.columns):
                max_length = max(
                    export_df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        output.seek(0)
        return output.getvalue()
    
    except Exception as e:
        # Fallback to CSV if openpyxl not available
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode('utf-8')


def generate_one_pager(pager_type, selection, session_state):
    """
    Generate an HTML one-pager summary.
    
    Args:
        pager_type: Type of one-pager (Member Company, Use Case, etc.)
        selection: Selected item name
        session_state: Streamlit session state with data
    
    Returns:
        HTML string for the one-pager
    """
    from data.sample_data import MEMBER_COMPANIES, get_company_name, get_company_color
    
    df = session_state.use_cases
    contacts_df = session_state.contacts
    
    current_date = datetime.now().strftime('%B %d, %Y')
    
    if pager_type == "Member Company":
        company = next((c for c in MEMBER_COMPANIES if c['name'] == selection), None)
        company_id = company['id'] if company else None
        color = company['color'] if company else "#0066B1"
        
        company_uc = df[
            (df['lead_company'] == company_id) |
            (df['participating_companies'].apply(lambda x: company_id in x if company_id else False))
        ]
        contacts = contacts_df[contacts_df['company'] == company_id]
        
        # Build use cases list HTML
        uc_list = ""
        for _, row in company_uc.iterrows():
            role = "Lead" if row['lead_company'] == company_id else "Participant"
            uc_list += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{row['id']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{row['title']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{role}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{row['status']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{row['progress']}%</td>
            </tr>
            """
        
        # Build contacts list HTML
        contacts_list = ""
        for _, contact in contacts.iterrows():
            primary = "⭐ " if contact['is_primary'] else ""
            contacts_list += f"""
            <div style="margin-bottom: 12px;">
                <strong>{primary}{contact['name']}</strong><br>
                {contact['role']}<br>
                📧 {contact['email']} | 📞 {contact['phone']}
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{selection} - One Pager</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 40px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    border-bottom: 4px solid {color};
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    color: {color};
                }}
                .header p {{
                    color: #666;
                    margin: 10px 0 0 0;
                }}
                .branding {{
                    float: right;
                    text-align: right;
                    color: #999;
                    font-size: 14px;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .section h2 {{
                    color: {color};
                    font-size: 18px;
                    margin-bottom: 15px;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #eee;
                }}
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                }}
                .metric {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .metric-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: {color};
                }}
                .metric-label {{
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th {{
                    background: {color}15;
                    color: {color};
                    padding: 10px;
                    text-align: left;
                    font-weight: 600;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    text-align: center;
                    color: #999;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="branding">
                        DDPA × Snowflake<br>
                        {current_date}
                    </div>
                    <h1>🦷 {selection}</h1>
                    <p>Member Company Overview</p>
                </div>
                
                <div class="section">
                    <h2>📊 Key Metrics</h2>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">{len(df[df['lead_company'] == company_id])}</div>
                            <div class="metric-label">Leading</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{len(company_uc)}</div>
                            <div class="metric-label">Total Involved</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{len(company_uc[company_uc['status'] == 'In Progress'])}</div>
                            <div class="metric-label">In Progress</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{company_uc['progress'].mean():.0f}%</div>
                            <div class="metric-label">Avg Progress</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>👥 Key Contacts</h2>
                    {contacts_list if contacts_list else "<p>No contacts assigned</p>"}
                </div>
                
                <div class="section">
                    <h2>📋 Use Cases</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>Role</th>
                                <th>Status</th>
                                <th>Progress</th>
                            </tr>
                        </thead>
                        <tbody>
                            {uc_list if uc_list else "<tr><td colspan='5'>No use cases</td></tr>"}
                        </tbody>
                    </table>
                </div>
                
                <div class="footer">
                    Generated by Delta Dental Project Planning Tracker | DDPA × Snowflake Partnership
                </div>
            </div>
        </body>
        </html>
        """
        
        return html.encode('utf-8')
    
    else:
        # Generic one-pager for other types
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{selection} - One Pager</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #0066B1;
                    border-bottom: 3px solid #0066B1;
                    padding-bottom: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🦷 {selection}</h1>
                <p><strong>Type:</strong> {pager_type}</p>
                <p><strong>Generated:</strong> {current_date}</p>
                <hr>
                <p>This one-pager provides an overview of {selection}.</p>
                <div style="margin-top: 40px; text-align: center; color: #999; font-size: 12px;">
                    Generated by Delta Dental Project Planning Tracker | DDPA × Snowflake Partnership
                </div>
            </div>
        </body>
        </html>
        """
        
        return html.encode('utf-8')


def export_roadmap_to_pptx(df, filename="roadmap.pptx"):
    """
    Export roadmap to PowerPoint format.
    This is a placeholder for future implementation.
    
    Args:
        df: DataFrame with use cases
        filename: Output filename
    
    Returns:
        Bytes object containing PPTX file
    """
    # Placeholder - would use python-pptx library
    raise NotImplementedError("PowerPoint export coming soon")


def export_meeting_notes(meetings_df, format='markdown'):
    """
    Export meeting notes in various formats.
    
    Args:
        meetings_df: DataFrame with meeting data
        format: Output format ('markdown', 'html', 'txt')
    
    Returns:
        String with formatted meeting notes
    """
    if format == 'markdown':
        output = "# Meeting Notes\n\n"
        
        for _, meeting in meetings_df.iterrows():
            output += f"## {meeting['title']}\n"
            output += f"**Date:** {meeting['date']}\n\n"
            output += f"**Attendees:** {', '.join(meeting['attendees'])}\n\n"
            output += f"**Companies:** {', '.join(meeting['companies'])}\n\n"
            output += f"### Summary\n{meeting['summary']}\n\n"
            output += "### Action Items\n"
            for item in meeting['action_items']:
                output += f"- [ ] {item}\n"
            output += "\n---\n\n"
        
        return output
    
    elif format == 'html':
        output = "<html><body><h1>Meeting Notes</h1>"
        
        for _, meeting in meetings_df.iterrows():
            output += f"<h2>{meeting['title']}</h2>"
            output += f"<p><strong>Date:</strong> {meeting['date']}</p>"
            output += f"<p><strong>Attendees:</strong> {', '.join(meeting['attendees'])}</p>"
            output += f"<h3>Summary</h3><p>{meeting['summary']}</p>"
            output += "<h3>Action Items</h3><ul>"
            for item in meeting['action_items']:
                output += f"<li>{item}</li>"
            output += "</ul><hr>"
        
        output += "</body></html>"
        return output
    
    else:
        output = "MEETING NOTES\n" + "=" * 50 + "\n\n"
        
        for _, meeting in meetings_df.iterrows():
            output += f"{meeting['title']}\n"
            output += f"Date: {meeting['date']}\n"
            output += f"Attendees: {', '.join(meeting['attendees'])}\n\n"
            output += f"Summary:\n{meeting['summary']}\n\n"
            output += "Action Items:\n"
            for item in meeting['action_items']:
                output += f"  - {item}\n"
            output += "\n" + "-" * 50 + "\n\n"
        
        return output
