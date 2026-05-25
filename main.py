import data_ingestor, nlp_processor
import streamlit as st
import altair as alt
import pandas as pd

# st.title("TOP 20 MOST TALKED ABOUT COMPANIES")
#
# def top_20_companies():
#     # st.header("Fetching news articles...")
#     news = data_ingestor.fetch_trending_news()
#     # st.header("Processing news articles...")
#     processed_news = nlp_processor.process_text_frequencies(news)
#     # st.header("Displaying results...")
#     # st.header("TOP 20 MOST TALKED ABOUT COMPANIES ===")
#     for rank, (company, mentions) in enumerate(processed_news, start=1):
#         st.header(f"{rank}. {company} — Mentioned {mentions} times")
#
# st.button("Show Top 20 Companies", on_click=top_20_companies)

st.set_page_config(page_title="Company Trends", page_icon="📈", layout="centered")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">📈 TOP 20 MOST TALKED ABOUT COMPANIES</div>', unsafe_allow_html=True)
st.write("Discover which companies are dominating the headlines right now.")
st.divider()

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if st.button("🔄 Fetch & Analyze Live News", type="primary", use_container_width=True):
    st.session_state.show_results = True

# Display results
if st.session_state.show_results:
    with st.status("Analyzing live news feeds...", expanded=True) as status:
        st.write("Fetching articles from sources...")
        news = data_ingestor.fetch_trending_news()

        st.write("Running NLP frequency analysis...")
        processed_news = nlp_processor.process_text_frequencies(news)

        status.update(label="Analysis complete!", state="complete", expanded=False)

    st.subheader("🏆 Top Trending Leaders")

    top_3 = processed_news[:3]
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]

    for i, (company, mentions) in enumerate(top_3):
        if i < len(cols):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <p style="font-size: 1.5rem; margin: 0;">{medals[i]}</p>
                        <h4 style="margin: 5px 0;">{company}</h4>
                        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;"><b>{mentions}</b> mentions</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.divider()

    tab1, tab2 = st.tabs(["📊 Data View", "📜 Full Ranking List"])

    with tab1:
        df = pd.DataFrame(processed_news, columns=["Company", "Mentions"])
        df = df.sort_values(by="Mentions", ascending=True)

        df["Company"] = (
            df["Company"]
            .str.replace(", Inc.", "", case=False)
            .str.replace(" Inc.", "", case=False)
            .str.replace(", N.V.", "", case=False)
            .str.replace(" Corp.", "", case=False)
        )

        chart = (
            alt.Chart(df)
            .mark_bar(color="#3B82F6")
            .encode(
                x=alt.X(
                    "Mentions:Q",
                    axis=alt.Axis(
                        labelAngle=0,
                        title="Mentions",
                    ),
                ),
                y=alt.Y(
                    "Company:N",
                    sort="-x",
                    axis=alt.Axis(title=None),
                ),
                tooltip=["Company", "Mentions"],
            )
            .properties(height=500)
        )

        st.altair_chart(chart, use_container_width=True)

    with tab2:
        for rank, (company, mentions) in enumerate(processed_news, start=1):
            st.write(f"**{rank}. {company}** — `{mentions} mentions`")

