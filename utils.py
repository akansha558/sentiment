import json
import os
from datetime import datetime
from typing import Dict, List
import pandas as pd
from collections import Counter
import re

def save_to_history(entity_name: str, location: str, stats: Dict, df: pd.DataFrame):
    history_file = "data/history.json"
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entity_name": entity_name,
        "location": location,
        "total_reviews": stats['total'],
        "avg_rating": stats['avg_rating'],
        "avg_sentiment": stats['avg_sentiment'],
        "positive_percentage": stats['positive_percentage'],
        "negative_percentage": stats['negative_percentage'],
    }
    
    history.insert(0, entry)
    history = history[:20]
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    return history

def load_history() -> List[Dict]:
    history_file = "data/history.json"
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def extract_keywords(df: pd.DataFrame, top_n: int = 10) -> List[str]:
    all_text = ' '.join(df['review_text'].tolist())
    words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
    stop_words = {'the', 'and', 'for', 'that', 'this', 'with', 'was', 'were', 'have', 'has', 'had', 'but', 'not', 'are', 'all', 'can', 'from', 'they', 'their', 'what', 'will', 'would'}
    filtered_words = [w for w in words if w not in stop_words]
    word_counts = Counter(filtered_words)
    return [word for word, count in word_counts.most_common(top_n)]