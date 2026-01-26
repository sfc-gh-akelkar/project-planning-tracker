"""
Duplicate Detection Module
Identifies similar and potentially duplicate use cases across member companies.
"""

import re
from collections import Counter


def tokenize(text):
    """Simple tokenization - lowercase and split on non-alphanumeric."""
    if not text:
        return []
    return re.findall(r'\b[a-z]+\b', text.lower())


def calculate_similarity(text1, text2):
    """
    Calculate similarity between two texts using Jaccard similarity
    with additional weighting for important terms.
    """
    if not text1 or not text2:
        return 0.0
    
    # Tokenize
    tokens1 = set(tokenize(text1))
    tokens2 = set(tokenize(text2))
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                  'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
                  'could', 'should', 'may', 'might', 'must', 'shall', 'this', 'that',
                  'these', 'those', 'all', 'each', 'every', 'both', 'few', 'more',
                  'most', 'other', 'some', 'such', 'no', 'not', 'only', 'own', 'same',
                  'so', 'than', 'too', 'very', 'can', 'just', 'using', 'use', 'data'}
    
    tokens1 = tokens1 - stop_words
    tokens2 = tokens2 - stop_words
    
    if not tokens1 or not tokens2:
        return 0.0
    
    # Jaccard similarity
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    
    jaccard = len(intersection) / len(union) if union else 0.0
    
    return jaccard


def calculate_tag_overlap(tags1, tags2):
    """Calculate overlap between tag lists."""
    if not tags1 or not tags2:
        return 0.0
    
    set1 = set([t.lower() for t in tags1])
    set2 = set([t.lower() for t in tags2])
    
    intersection = set1 & set2
    union = set1 | set2
    
    return len(intersection) / len(union) if union else 0.0


def find_duplicates(df, threshold=0.4):
    """
    Find potential duplicate use cases in the dataframe.
    
    Args:
        df: DataFrame with use cases
        threshold: Minimum similarity score to flag as potential duplicate
    
    Returns:
        List of duplicate pairs with similarity scores
    """
    duplicates = []
    
    # Convert to list for iteration
    use_cases = df.to_dict('records')
    n = len(use_cases)
    
    for i in range(n):
        for j in range(i + 1, n):
            uc1 = use_cases[i]
            uc2 = use_cases[j]
            
            # Skip if same use case
            if uc1['id'] == uc2['id']:
                continue
            
            # Calculate similarities
            title_sim = calculate_similarity(uc1['title'], uc2['title'])
            desc_sim = calculate_similarity(uc1['description'], uc2['description'])
            tag_sim = calculate_tag_overlap(uc1.get('tags', []), uc2.get('tags', []))
            
            # Category match bonus
            category_match = 1.0 if uc1['category'] == uc2['category'] else 0.0
            
            # Weighted overall similarity
            overall_sim = (
                title_sim * 0.4 +
                desc_sim * 0.3 +
                tag_sim * 0.2 +
                category_match * 0.1
            )
            
            if overall_sim >= threshold:
                duplicates.append({
                    'id1': uc1['id'],
                    'title1': uc1['title'],
                    'company1': uc1['lead_company'],
                    'status1': uc1['status'],
                    'id2': uc2['id'],
                    'title2': uc2['title'],
                    'company2': uc2['lead_company'],
                    'status2': uc2['status'],
                    'similarity': overall_sim,
                    'title_similarity': title_sim,
                    'description_similarity': desc_sim,
                    'tag_overlap': tag_sim,
                    'same_category': category_match == 1.0
                })
    
    # Sort by similarity descending
    duplicates.sort(key=lambda x: x['similarity'], reverse=True)
    
    return duplicates


def get_consolidation_recommendations(duplicates, df):
    """
    Generate recommendations for consolidating duplicate use cases.
    
    Args:
        duplicates: List of duplicate pairs from find_duplicates
        df: Original DataFrame
    
    Returns:
        List of consolidation recommendations
    """
    recommendations = []
    
    for dup in duplicates:
        if dup['similarity'] >= 0.7:
            # High similarity - recommend merge
            rec = {
                'type': 'merge',
                'priority': 'high',
                'message': f"Consider merging {dup['id1']} and {dup['id2']} - very high similarity ({dup['similarity']:.0%})",
                'details': dup
            }
        elif dup['similarity'] >= 0.5:
            # Medium similarity - recommend review
            rec = {
                'type': 'review',
                'priority': 'medium',
                'message': f"Review {dup['id1']} and {dup['id2']} for potential overlap ({dup['similarity']:.0%})",
                'details': dup
            }
        else:
            # Lower similarity - just flag for awareness
            rec = {
                'type': 'monitor',
                'priority': 'low',
                'message': f"Monitor {dup['id1']} and {dup['id2']} - some overlap detected ({dup['similarity']:.0%})",
                'details': dup
            }
        
        # Add recommendation about which company should lead
        uc1 = df[df['id'] == dup['id1']].iloc[0] if len(df[df['id'] == dup['id1']]) > 0 else None
        uc2 = df[df['id'] == dup['id2']].iloc[0] if len(df[df['id'] == dup['id2']]) > 0 else None
        
        if uc1 is not None and uc2 is not None:
            # Recommend the one with more progress to lead
            if uc1['progress'] > uc2['progress']:
                rec['recommended_lead'] = dup['id1']
            elif uc2['progress'] > uc1['progress']:
                rec['recommended_lead'] = dup['id2']
            else:
                # If same progress, recommend the one started earlier
                rec['recommended_lead'] = dup['id1'] if uc1['start_date'] < uc2['start_date'] else dup['id2']
        
        recommendations.append(rec)
    
    return recommendations
