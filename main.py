import data_ingestor, nlp_processor
import streamlit as st

st.title("TOP 20 MOST TALKED ABOUT COMPANIES")

def top_20_companies():
    st.header("Fetching news articles...")
    news = data_ingestor.fetch_trending_news()
    st.header("Processing news articles...")
    processed_news = nlp_processor.process_text_frequencies(news)
    st.header("Displaying results...")
    # st.header("TOP 20 MOST TALKED ABOUT COMPANIES ===")
    for rank, (company, mentions) in enumerate(processed_news, start=1):
        st.header(f"{rank}. {company} — Mentioned {mentions} times")

st.button("Show Top 20 Companies", on_click=top_20_companies)

