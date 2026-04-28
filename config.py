# """
# Configuration settings - Enhanced for better scraping.
# """

# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATA_DIR = BASE_DIR / "data"
# DATA_DIR.mkdir(exist_ok=True)

# DATABASE_URL = f"sqlite:///{DATA_DIR}/reviews.db"

# # Scraping Settings
# SCRAPE_DELAY_SECONDS = float(os.getenv("SCRAPE_DELAY", "3.0"))
# MAX_REVIEWS_PER_SOURCE = int(os.getenv("MAX_REVIEWS", "30"))
# REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# # Entity Classification Keywords
# COLLEGE_KEYWORDS = [
#     "college", "university", "institute", "school", "academy", "iit", "nit", "bits",
#     "कॉलेज", "विश्वविद्यालय", "संस्थान"
# ]

# FOOD_KEYWORDS = [
#     "restaurant", "cafe", "pizza", "hotel", "dhaba", "food", "bakery", "mall",
#     "रेस्तरां", "कैफे", "दुकान"
# ]

# # Sentiment Settings
# VADER_POSITIVE_THRESHOLD = 0.05
# VADER_NEGATIVE_THRESHOLD = -0.05

# # Emotion Keywords
# EMOTION_KEYWORDS = {
#     "joy": ["happy", "excellent", "amazing", "great", "awesome", "wonderful", "fantastic", "love", "perfect", "best", "good", "nice", "शानदार", "बढ़िया"],
#     "anger": ["worst", "fraud", "bad", "terrible", "awful", "horrible", "useless", "waste", "hate", "angry", "furious", "scam", "cheat", "fake", "बेकार", "धोखा", "खराब"],
#     "sadness": ["disappointed", "poor", "unhappy", "sad", "upset", "regret", "निराश", "दुखी"],
#     "fear": ["scared", "worried", "anxious", "fear", "डर"],
#     "surprise": ["shocked", "surprised", "unexpected", "आश्चर्य"],
#     "disgust": ["disgusting", "gross", "revolting", "ghastly", "घृणित"],
#     "trust": ["reliable", "professional", "trustworthy", "honest", "विश्वसनीय", "भरोसेमंद"],
#     "anticipation": ["excited", "looking forward", "can't wait", "hopeful", "उत्सुक"]
# }

# # Aspect Keywords
# ASPECT_KEYWORDS = {
#     "food": ["food", "taste", "meal", "dish", "flavor", "cuisine", "dinner", "lunch", "breakfast"],
#     "service": ["service", "staff", "support", "waiter", "waitress", "employee", "team", "customer service"],
#     "price": ["price", "cost", "expensive", "cheap", "affordable", "value", "pricing", "money"],
#     "quality": ["quality", "standard", "premium", "best", "worst"],
#     "delivery": ["delivery", "shipping", "packaging", "dispatch", "timely"],
#     "ambiance": ["ambiance", "atmosphere", "environment", "vibe", "decor", "interior"]
# }

# ANGER_KEYWORDS = [
#     "terrible", "awful", "horrible", "disgusting", "worst", "bad", "pathetic", 
#     "useless", "waste", "hate", "angry", "furious", "outraged", "ridiculous", 
#     "annoying", "frustrating", "disappointed", "scam", "fraud", "cheated", 
#     "fake", "ripoff", "looted", "बेकार", "घटिया", "खराब", "धोखा", "फालतू"
# ]

# # NLP Model
# BERT_MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
# BERT_MAX_LENGTH = 512

# # Supported Languages
# SUPPORTED_LANGUAGES = ["en", "hi", "pa", "hinglish"]

# # App Meta
# APP_TITLE = "SentimentIQ - Multi-Source Review Analyzer"
# APP_VERSION = "3.0.0"
# API_PREFIX = "/api/v1"

# # CORS
# ALLOWED_ORIGINS = ["*"]
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
    APP_NAME = "SentimentIQ"
    APP_VERSION = "2.0.0"
    MAX_REVIEWS = 50
    CONFIDENCE_THRESHOLD = 0.6
    HISTORY_FILE = "data/history.json"
    DEMO_MODE = False