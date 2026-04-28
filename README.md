# 🔮 Multi-Source Review Sentiment Analyzer

> **Industry-grade NLP pipeline** that collects company reviews from multiple sources and performs hybrid VADER + BERT sentiment analysis, visualised in a modern Streamlit dashboard.

---

## 📸 Features

| Feature | Details |
|---|---|
| 🤖 Hybrid NLP | VADER (rule-based) + BERT (multilingual transformer) fusion |
| 🌐 Multi-Source | Manual text · URL scraping · CSV/TXT upload · API |
| 🌍 Multilingual | English · Hindi · Punjabi · Hinglish with auto-detection |
| 📊 Rich Charts | Pie, bar, gauge, scatter timeline |
| 💾 Persistence | SQLite (auto-created) via SQLAlchemy ORM |
| ⚡ Real-time | Instant single-review quick test |
| 📤 Export | Download results as CSV |

---

## 🗂 Project Structure

```
project/
├── backend/
│   ├── main.py                # FastAPI app + startup
│   ├── config.py              # All settings / env-vars
│   ├── routes/
│   │   ├── analyze.py         # POST /analyze, /analyze/batch, GET /analyze/history
│   │   ├── scrape.py          # POST /scrape
│   │   └── aggregate.py       # POST /aggregate, GET /aggregate/sessions
│   ├── services/
│   │   ├── sentiment.py       # VADER + BERT + hybrid analysis
│   │   ├── scraper.py         # BS4 + Selenium scraping
│   │   ├── aggregator.py      # Multi-source merge + stats
│   │   └── preprocess.py      # Cleaning, lang detect, translation
│   ├── models/
│   │   └── database.py        # SQLAlchemy ORM models + helpers
│   └── utils/
│       └── helpers.py         # CSV parsing, pagination, etc.
├── frontend/
│   └── app.py                 # Streamlit dashboard (landing / login / dashboard)
├── data/                      # SQLite DB created here at runtime
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone / unzip the project

```bash
cd project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note on BERT:** The first run downloads the multilingual sentiment model (~700 MB). Subsequent runs use the local cache.

### 4. (Optional) Environment variables

Create a `.env` file in the project root:

```env
GOOGLE_PLACES_API_KEY=your_key_here   # optional – for Places API
SCRAPE_DELAY=2.0                       # seconds between requests
MAX_REVIEWS=20                         # cap per source
```

---

## ▶️ Running

Open **two terminals** from the `project/` directory.

### Terminal 1 – Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

API will be live at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### Terminal 2 – Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Dashboard will open at: `http://localhost:8501`

---

## 🔑 Login Credentials (Demo)

| Username | Password |
|---|---|
| `admin` | `admin123` |
| `user` | `review2024` |

---

## 🌐 API Reference

### `GET /api/v1/health`
Check if the backend is running.

### `POST /api/v1/analyze/`
Analyze a single review.
```json
{
  "text": "The product is amazing!",
  "company": "Zomato",
  "source": "manual",
  "save": true
}
```

### `POST /api/v1/analyze/batch`
Analyze a list of reviews.
```json
{
  "reviews": ["Great service", "Terrible experience"],
  "company": "Flipkart"
}
```

### `POST /api/v1/scrape/`
Scrape and analyze reviews from a URL.
```json
{
  "url": "https://example.com/reviews",
  "company": "ACME",
  "analyze": true
}
```

### `POST /api/v1/aggregate/` (multipart/form-data)
Full multi-source analysis.

| Field | Type | Required |
|---|---|---|
| `company` | string | ✅ |
| `review_text` | string | optional |
| `url` | string | optional |
| `file` | CSV/TXT | optional |

### `GET /api/v1/aggregate/sessions`
List recent analysis sessions.

### `GET /api/v1/analyze/history/{company}`
Fetch sentiment history for a company.

---

## 🤖 Sentiment Labels

| Label | Emoji | Meaning |
|---|---|---|
| positive | 😊 | Generally happy feedback |
| neutral | 😐 | Mixed or factual content |
| negative | 😡 | Unhappy feedback |
| angry | 😤 | Strong anger or frustration |

### Score interpretation

| Score | Grade | Meaning |
|---|---|---|
| 0.80 – 1.00 | A+ | Excellent |
| 0.70 – 0.79 | A | Very Good |
| 0.60 – 0.69 | B | Good |
| 0.50 – 0.59 | C | Average |
| 0.40 – 0.49 | D | Below Average |
| 0.00 – 0.39 | F | Poor |

---

## 🧩 Architecture

```
User Input / URL / CSV
        │
        ▼
┌──────────────────┐    ┌─────────────────────┐
│  FastAPI Backend  │◄───│  Streamlit Frontend  │
│                  │    └─────────────────────┘
│  Preprocess      │
│    │             │
│  Scraper (BS4 /  │
│  Selenium)       │
│    │             │
│  Aggregator      │
│    │             │
│  ┌────────────┐  │
│  │  VADER     │  │
│  │  BERT      │──┤──► Hybrid Result
│  │  (Hybrid)  │  │
│  └────────────┘  │
│    │             │
│  SQLite DB       │
└──────────────────┘
```

---

## 🔧 Customisation

### Add a new scraper
Add a function to `backend/services/scraper.py` following the pattern of `scrape_trustpilot()`.

### Change the BERT model
Set `BERT_MODEL_NAME` in `backend/config.py`. Any HuggingFace sentiment model works.

### Add a language
Extend `detect_language()` in `backend/services/preprocess.py`.

---

## 📦 Built With

- **FastAPI** – high-performance Python web framework
- **Streamlit** – rapid data app UI
- **vaderSentiment** – rule-based English sentiment
- **HuggingFace Transformers** – multilingual BERT model
- **SQLAlchemy + SQLite** – ORM + embedded database
- **BeautifulSoup4 + Selenium** – web scraping
- **Plotly** – interactive charts
- **deep-translator** – multi-language translation

---

## 📄 Licence

MIT – Free to use for educational and portfolio projects.

---

*Developed as an Industrial Training Project · 2024*
