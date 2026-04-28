import pandas as pd
from textblob import TextBlob
from typing import Dict

class SentimentAnalyzer:
    def analyze_text(self, text: str) -> Dict:
        if not text or len(text.strip()) < 5:
            return {"label": "Neutral", "score": 50, "polarity": 0, "subjectivity": 0}
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"
        
        score = (polarity + 1) / 2 * 100
        
        return {
            "label": label,
            "score": round(score, 2),
            "polarity": round(polarity, 4),
            "subjectivity": round(subjectivity, 4)
        }
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = "review_text") -> pd.DataFrame:
        df_analyzed = df.copy()
        sentiment_results = df_analyzed[text_column].apply(self.analyze_text)
        df_analyzed['sentiment_label'] = sentiment_results.apply(lambda x: x['label'])
        df_analyzed['sentiment_score'] = sentiment_results.apply(lambda x: x['score'])
        df_analyzed['sentiment_polarity'] = sentiment_results.apply(lambda x: x['polarity'])
        df_analyzed['subjectivity'] = sentiment_results.apply(lambda x: x['subjectivity'])
        return df_analyzed
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        if df.empty:
            return {"total": 0, "avg_rating": 0, "avg_sentiment": 0, "sentiment_counts": {}, "rating_distribution": {}, "positive_percentage": 0, "negative_percentage": 0}
        
        sentiment_counts = df['sentiment_label'].value_counts().to_dict()
        rating_distribution = df['rating'].value_counts().sort_index().to_dict()
        total = len(df)
        positive_count = sentiment_counts.get('Positive', 0)
        
        return {
            "total": total,
            "avg_rating": round(df['rating'].mean(), 2),
            "avg_sentiment": round(df['sentiment_score'].mean(), 2),
            "sentiment_counts": sentiment_counts,
            "rating_distribution": rating_distribution,
            "positive_percentage": round((positive_count / total) * 100, 1) if total > 0 else 0,
            "negative_percentage": round(((total - positive_count - sentiment_counts.get('Negative', 0)) / total) * 100, 1) if total > 0 else 0
        }

sentiment_analyzer = SentimentAnalyzer()