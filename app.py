from collections import OrderedDict

import streamlit as st

from fetch_news import fetch_news


BULLISH_KEYWORDS = {
    "beat",
    "beats",
    "surge",
    "surges",
    "jump",
    "jumps",
    "rally",
    "rallies",
    "gain",
    "gains",
    "growth",
    "upgrade",
    "upgrades",
    "record high",
    "strong",
    "soar",
    "soars",
    "profit",
    "profits",
    "bullish",
}

BEARISH_KEYWORDS = {
    "miss",
    "misses",
    "drop",
    "drops",
    "fall",
    "falls",
    "slump",
    "slumps",
    "downgrade",
    "downgrades",
    "weak",
    "lawsuit",
    "investigation",
    "loss",
    "losses",
    "bearish",
    "plunge",
    "plunges",
    "cut",
    "cuts",
}

SENTIMENT_ORDER = OrderedDict(
    [
        ("Bullish", BULLISH_KEYWORDS),
        ("Bearish", BEARISH_KEYWORDS),
        ("Neutral", set()),
    ]
)


def classify_headline(headline: str) -> str:
    normalized_headline = headline.lower()

    bullish_matches = sum(
        keyword in normalized_headline for keyword in BULLISH_KEYWORDS
    )
    bearish_matches = sum(
        keyword in normalized_headline for keyword in BEARISH_KEYWORDS
    )

    if bullish_matches > bearish_matches:
        return "Bullish"
    if bearish_matches > bullish_matches:
        return "Bearish"
    return "Neutral"


def group_headlines_by_sentiment(headlines: list[str]) -> dict[str, list[str]]:
    grouped_headlines = {sentiment: [] for sentiment in SENTIMENT_ORDER}

    for headline in headlines:
        grouped_headlines[classify_headline(headline)].append(headline)

    return grouped_headlines


st.title("Stock News Agent")
ticker = st.text_input("Enter a stock ticker", "AAPL")

if st.button("Fetch News"):
    headlines = fetch_news(ticker)

    if not headlines:
        st.warning("No headlines were found for that ticker.")
    else:
        grouped_headlines = group_headlines_by_sentiment(headlines)

        st.subheader("Classified Headlines")
        for sentiment in SENTIMENT_ORDER:
            st.markdown(f"### {sentiment}")
            sentiment_headlines = grouped_headlines[sentiment]

            if sentiment_headlines:
                for headline in sentiment_headlines:
                    st.write(f"- {headline}")
            else:
                st.write("- None")
