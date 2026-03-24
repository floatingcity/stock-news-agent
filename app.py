import json
import os
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Stock News Sentiment", page_icon="📰")
st.title("Stock News Sentiment")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_headlines(ticker: str, limit: int = 10) -> list[str]:
    url = f"https://news.google.com/rss/search?q={ticker}+stock"
    with urlopen(url, timeout=10) as response:
        rss_feed = response.read()
    root = ET.fromstring(rss_feed)
    return [
        title.text.strip()
        for title in root.findall("./channel/item/title")
        if title.text and title.text.strip()
    ][:limit]


def analyze(headlines: list[str]) -> list[dict]:
    prompt = (
        "For each headline, return JSON array entries with keys: "
        "headline, sentiment (Positive/Negative/Neutral), summary (max 18 words).\n"
        f"Headlines: {json.dumps(headlines)}"
    )
    res = client.responses.create(model="gpt-4.1-mini", input=prompt)
    text = res.output_text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    rows = json.loads(text)
    allowed = {"Positive", "Negative", "Neutral"}
    clean = []
    for r in rows:
        s = str(r.get("sentiment", "Neutral")).title()
        clean.append(
            {
                "headline": r.get("headline", ""),
                "sentiment": s if s in allowed else "Neutral",
                "summary": r.get("summary", ""),
            }
        )
    return clean


ticker = st.text_input("Ticker", value="AAPL").strip().upper()
if st.button("Analyze"):
    if not ticker:
        st.warning("Enter a ticker.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY environment variable.")
    else:
        headlines = get_headlines(ticker)
        if not headlines:
            st.info("No headlines found.")
        else:
            try:
                st.dataframe(pd.DataFrame(analyze(headlines)), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
