from fetch_news import fetch_news

import streamlit as st

st.title("Stock News Agent")
ticker = st.text_input("Enter a stock ticker", "AAPL")

if st.button("Fetch News"):
    st.write(fetch_news(ticker))
