import pandas as pd
import streamlit as st

from classifier import classify_headlines
from fetch_news import fetch_news

st.set_page_config(page_title="Stock News Sentiment", page_icon="📰")
st.title("Stock News Sentiment")

ticker = st.text_input("Ticker", value="AAPL").strip().upper()

if st.button("Analyze"):
    if not ticker:
        st.warning("Enter a ticker.")
    else:
        headlines = fetch_news(ticker)
        if not headlines:
            st.info("No headlines found.")
        else:
            results = classify_headlines(headlines)
            df = pd.DataFrame(results)
            st.table(df[["headline", "sentiment"]])
