"""
Review Fetcher - Works with or without apify-client
"""

import pandas as pd
from datetime import datetime, timedelta
from backend.config import Config

class ReviewFetcher:
    def __init__(self):
        self.token = Config.APIFY_TOKEN
        self.use_demo = Config.DEMO_MODE or not self.token
        self.client = None
        
        if not self.use_demo:
            try:
                # Try to import apify_client only if available
                from apify_client import ApifyClient
                self.client = ApifyClient(self.token)
                print("✅ Apify client initialized")
            except ImportError:
                print("⚠️ apify_client not installed, using demo mode")
                self.use_demo = True
            except Exception as e:
                print(f"⚠️ Apify init failed: {e}")
                self.use_demo = True
    
    def fetch_reviews(self, entity_name: str, location: str = "") -> pd.DataFrame:
        """Fetch reviews - automatically uses demo mode if API unavailable"""
        
        if self.use_demo:
            return self._get_demo_data(entity_name, location)
        
        # Try real API (only if client exists)
        try:
            if self.client:
                # Your API fetching code here
                pass
        except Exception as e:
            print(f"API fetch failed: {e}, using demo data")
            return self._get_demo_data(entity_name, location)
    
    def _get_demo_data(self, entity_name: str, location: str = "") -> pd.DataFrame:
        """Generate demo data for testing"""
        # Demo reviews
        reviews_data = [
            {"review_text": f"Great experience at {entity_name}! Highly recommend.", "rating": 5, "date": "2024-01-15"},
            {"review_text": f"Very disappointed with {entity_name}. Poor service.", "rating": 2, "date": "2024-01-10"},
            {"review_text": f"Average experience at {entity_name}. Nothing special.", "rating": 3, "date": "2024-01-05"},
            {"review_text": f"Excellent {entity_name}! Will definitely come back.", "rating": 5, "date": "2024-01-01"},
            {"review_text": f"Good value for money at {entity_name}.", "rating": 4, "date": "2023-12-28"},
        ]
        
        df = pd.DataFrame(reviews_data)
        print(f"📝 Using demo data for {entity_name} ({len(df)} reviews)")
        return df

# Create global instance
review_fetcher = ReviewFetcher()