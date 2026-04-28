import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from backend.review_fetcher import review_fetcher
from backend.sentiment_analyzer import sentiment_analyzer
from backend.utils import save_to_history, load_history
from backend.utils import extract_keywords
from backend.config import Config

st.set_page_config(page_title=Config.APP_NAME, page_icon="🎯", layout="wide")

st.markdown("""
<style>
.main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem; }
.sentiment-card { padding: 1rem; border-radius: 10px; text-align: center; color: white; margin: 0.5rem; }
.positive { background: linear-gradient(135deg, #10b981, #059669); }
.negative { background: linear-gradient(135deg, #ef4444, #dc2626); }
.neutral { background: linear-gradient(135deg, #f59e0b, #d97706); }
.review-box { background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid; }
.review-positive { border-left-color: #10b981; }
.review-negative { border-left-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

if 'current_df' not in st.session_state:
    st.session_state.current_df = None

def create_sentiment_pie_chart(df):
    counts = df['sentiment_label'].value_counts()
    fig = px.pie(values=counts.values, names=counts.index, title="Sentiment Distribution", color=counts.index, color_discrete_map={'Positive': '#10b981', 'Negative': '#ef4444', 'Neutral': '#f59e0b'})
    return fig

def create_rating_bar_chart(df):
    counts = df['rating'].value_counts().sort_index()
    fig = px.bar(x=counts.index, y=counts.values, title="Rating Distribution", labels={'x': 'Rating', 'y': 'Count'})
    return fig

def create_sentiment_gauge(score):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=score, title={'text': "Sentiment Score"}, number={'suffix': "%"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#7c3aed"}, 'steps': [{'range': [0, 33], 'color': "rgba(239,68,68,0.3)"}, {'range': [33, 66], 'color': "rgba(245,158,11,0.3)"}, {'range': [66, 100], 'color': "rgba(16,185,129,0.3)"}]}))
    fig.update_layout(height=250)
    return fig

st.markdown("<div class='main-header'><h1>🎯 SentimentIQ</h1><p>Advanced Sentiment Analysis for Any Business</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## About")
    st.info("Fetches real reviews from Google Maps • Analyzes sentiment • Interactive dashboard")
    st.markdown("---")
    st.markdown("## Recent")
    history = load_history()
    for item in history[:5]:
        st.write(f"📌 {item['entity_name']} - {item['avg_sentiment']:.0f}%")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    entity_name = st.text_input("🏢 Company / Restaurant Name", placeholder="e.g., Starbucks, Taj Hotel")
with col2:
    location = st.text_input("📍 Location (Optional)", placeholder="e.g., New York")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze and entity_name:
    with st.spinner(f"Analyzing {entity_name}..."):
        df = review_fetcher.fetch_reviews(entity_name, location)
        if not df.empty:
            df = sentiment_analyzer.analyze_dataframe(df)
            stats = sentiment_analyzer.get_summary_stats(df)
            save_to_history(entity_name, location, stats, df)
            st.session_state.current_df = df
            st.session_state.current_stats = stats
            st.session_state.current_entity = entity_name
            st.success(f"✅ Found {stats['total']} reviews!")
            st.balloons()

if st.session_state.current_df is not None:
    df = st.session_state.current_df
    stats = st.session_state.current_stats
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f"<div class='sentiment-card positive'><h3>📊 Total</h3><h2>{stats['total']}</h2></div>", unsafe_allow_html=True)
    with col2: sentiment_class = "positive" if stats['avg_sentiment'] >= 60 else "negative" if stats['avg_sentiment'] <= 40 else "neutral"
    st.markdown(f"<div class='sentiment-card {sentiment_class}'><h3>💬 Sentiment</h3><h2>{stats['avg_sentiment']:.0f}%</h2></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='sentiment-card positive'><h3>⭐ Rating</h3><h2>{stats['avg_rating']}/5</h2></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='sentiment-card positive'><h3>😊 Positive</h3><h2>{stats['positive_percentage']:.0f}%</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(create_sentiment_pie_chart(df), use_container_width=True)
    with col2: st.plotly_chart(create_rating_bar_chart(df), use_container_width=True)
    
    st.plotly_chart(create_sentiment_gauge(stats['avg_sentiment']), use_container_width=True)
    
    keywords = extract_keywords(df)
    if keywords:
        st.subheader("🔑 Key Topics")
        cols = st.columns(5)
        for i, kw in enumerate(keywords[:10]):
            cols[i % 5].markdown(f"<div style='background: #7c3aed33; padding: 0.3rem; border-radius: 5px; text-align: center'>{kw}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👍 Positive Reviews")
        for _, review in df[df['sentiment_label'] == 'Positive'].head(3).iterrows():
            st.markdown(f"<div class='review-box review-positive'>⭐ {review['rating']}/5<br>{review['review_text'][:200]}...</div>", unsafe_allow_html=True)
    with col2:
        st.subheader("👎 Critical Reviews")
        for _, review in df[df['sentiment_label'] == 'Negative'].head(3).iterrows():
            st.markdown(f"<div class='review-box review-negative'>⭐ {review['rating']}/5<br>{review['review_text'][:200]}...</div>", unsafe_allow_html=True)
    
    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Download CSV", csv, f"{st.session_state.current_entity}_analysis.csv", "text/csv")