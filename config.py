# import os, dotenv
# import streamlit as st
#
# MAX_NEWS_ARTICLES = 100
# DISPLAY_LIMIT = 20
# NEWS_API_KEY = None
# SCRAPINGBEE_API_KEY = None
# COMPANY_LOOKUP = {
#     "AAPL": "Apple Inc.",
#     "Apple": "Apple Inc.",
#     "apple": "Apple Inc.",
#
#     "NVDA": "NVIDIA Corp.",
#     "Nvidia": "NVIDIA Corp.",
#     "nvidia": "NVIDIA Corp.",
#
#     "TSLA": "Tesla Inc.",
#     "Tesla": "Tesla Inc.",
#     "tesla": "Tesla Inc.",
#
#     # --- Big Tech & AI Hyperscalers ---
#     "MSFT": "Microsoft Corp.",
#     "Microsoft": "Microsoft Corp.",
#     "microsoft": "Microsoft Corp.",
#
#     "GOOGL": "Alphabet Inc.",
#     "Google": "Alphabet Inc.",
#     "google": "Alphabet Inc.",
#
#     "AMZN": "Amazon.com Inc.",
#     "Amazon": "Amazon.com Inc.",
#     "amazon": "Amazon.com Inc.",
#
#     "META": "Meta Platforms Inc.",
#     "Meta": "Meta Platforms Inc.",
#     "meta": "Meta Platforms Inc.",
#
#     # --- Semiconductors & Hardware Infrastructure ---
#     "AMD": "Advanced Micro Devices Inc.",
#     "Amd": "Advanced Micro Devices Inc.",
#     "amd": "Advanced Micro Devices Inc.",
#
#     "AVGO": "Broadcom Inc.",
#     "Broadcom": "Broadcom Inc.",
#     "broadcom": "Broadcom Inc.",
#
#     "TSM": "Taiwan Semiconductor Manufacturing Co.",
#     "Tsmc": "Taiwan Semiconductor Manufacturing Co.",
#     "tsmc": "Taiwan Semiconductor Manufacturing Co.",
#
#     "MU": "Micron Technology Inc.",
#     "Micron": "Micron Technology Inc.",
#     "micron": "Micron Technology Inc.",
#
#     "INTC": "Intel Corp.",
#     "Intel": "Intel Corp.",
#     "intel": "Intel Corp.",
#
#     "ASML": "ASML Holding N.V.",
#     "Asml": "ASML Holding N.V.",
#     "asml": "ASML Holding N.V.",
#
#     # --- Enterprise Software, Cloud & Cyber ---
#     "ORCL": "Oracle Corp.",
#     "Oracle": "Oracle Corp.",
#     "oracle": "Oracle Corp.",
#
#     "CRM": "Salesforce Inc.",
#     "Salesforce": "Salesforce Inc.",
#     "salesforce": "Salesforce Inc.",
#
#     "PLTR": "Palantir Technologies Inc.",
#     "Palantir": "Palantir Technologies Inc.",
#     "palantir": "Palantir Technologies Inc.",
#
#     "NET": "Cloudflare Inc.",
#     "Cloudflare": "Cloudflare Inc.",
#     "cloudflare": "Cloudflare Inc.",
#
#     "IBM": "International Business Machines Corp.",
#     "Ibm": "International Business Machines Corp.",
#     "ibm": "International Business Machines Corp.",
#
#     # --- E-Commerce & Consumer Giants ---
#     "NFLX": "Netflix Inc.",
#     "Netflix": "Netflix Inc.",
#     "netflix": "Netflix Inc.",
#
#     "BABA": "Alibaba Group Holding Ltd.",
#     "Alibaba": "Alibaba Group Holding Ltd.",
#     "alibaba": "Alibaba Group Holding Ltd.",
#
#     "WMT": "Walmart Inc.",
#     "Walmart": "Walmart Inc.",
#     "walmart": "Walmart Inc.",
#
#     "NKE": "Nike Inc.",
#     "Nike": "Nike Inc.",
#     "nike": "Nike Inc.",
#
#     # --- Financials & Payments ---
#     "V": "Visa Inc.",
#     "Visa": "Visa Inc.",
#     "visa": "Visa Inc.",
#
#     "MA": "Mastercard Inc.",
#     "Mastercard": "Mastercard Inc.",
#     "mastercard": "Mastercard Inc.",
#
#     "JPM": "JPMorgan Chase & Co.",
#     "Jpmorgan": "JPMorgan Chase & Co.",
#     "jpmorgan": "JPMorgan Chase & Co.",
#
#     "GS": "The Goldman Sachs Group Inc.",
#     "Goldman": "The Goldman Sachs Group Inc.",
#     "goldman": "The Goldman Sachs Group Inc.",
#
#     # --- Energy, Automotive & Biotech/Pharma ---
#     "LLY": "Eli Lilly & Co.",
#     "Lilly": "Eli Lilly & Co.",
#     "lilly": "Eli Lilly & Co.",
#
#     "XOM": "Exxon Mobil Corp.",
#     "Exxon": "Exxon Mobil Corp.",
#     "exxon": "Exxon Mobil Corp.",
#
#     "CEG": "Constellation Energy Corp.",
#     "Constellation": "Constellation Energy Corp.",
#     "constellation": "Constellation Energy Corp.",
# }
#
# if hasattr(st, "secrets") and "NEWS_API_KEY" in st.secrets:
#     NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
#     SCRAPINGBEE_API_KEY = st.secrets.get("SCRAPINGBEE_API_KEY", "No api key.")
#
# elif os.path.exists(".env"):
#     dotenv.load_dotenv()
#     NEWS_API_KEY = os.environ.get("NEWS_API_KEY") if os.environ.get(
#         "NEWS_API_KEY") != "your_news_api_key_here" else "No api key."
#     SCRAPINGBEE_API_KEY = os.environ.get("SCRAPINGBEE_API_KEY") if os.environ.get(
#         "SCRAPINGBEE_API_KEY") != "your_scrapingbee_key_here" else "No api key."
#
#     if NEWS_API_KEY == "No api key." or SCRAPINGBEE_API_KEY == "No api key.":
#         raise NotImplementedError("No api keys found in .env file.")
#
# else:
#     raise NotImplementedError("Configuration Error: Neither .env file nor Streamlit Secrets were found.")
#
# # This allows your local print testing to still work fine
# if __name__ == '__main__':
#     print(f"NEWS_API_KEY: {NEWS_API_KEY}")
#     print(f"SCRAPINGBEE_API_KEY: {SCRAPINGBEE_API_KEY}")

import os, dotenv
import streamlit as st

MAX_NEWS_ARTICLES = 100
DISPLAY_LIMIT = 20
FINNHUB_API_KEY = None  # Changed variable name to reflect Finnhub

COMPANY_LOOKUP = {
    "AAPL": "Apple Inc.",
    "Apple": "Apple Inc.",
    "apple": "Apple Inc.",

    "NVDA": "NVIDIA Corp.",
    "Nvidia": "NVIDIA Corp.",
    "nvidia": "NVIDIA Corp.",

    "TSLA": "Tesla Inc.",
    "Tesla": "Tesla Inc.",
    "tesla": "Tesla Inc.",

    # --- Big Tech & AI Hyperscalers ---
    "MSFT": "Microsoft Corp.",
    "Microsoft": "Microsoft Corp.",
    "microsoft": "Microsoft Corp.",

    "GOOGL": "Alphabet Inc.",
    "Google": "Alphabet Inc.",
    "google": "Alphabet Inc.",

    "AMZN": "Amazon.com Inc.",
    "Amazon": "Amazon.com Inc.",
    "amazon": "Amazon.com Inc.",

    "META": "Meta Platforms Inc.",
    "Meta": "Meta Platforms Inc.",
    "meta": "Meta Platforms Inc.",

    # --- Semiconductors & Hardware Infrastructure ---
    "AMD": "Advanced Micro Devices Inc.",
    "Amd": "Advanced Micro Devices Inc.",
    "amd": "Advanced Micro Devices Inc.",

    "AVGO": "Broadcom Inc.",
    "Broadcom": "Broadcom Inc.",
    "broadcom": "Broadcom Inc.",

    "TSM": "Taiwan Semiconductor Manufacturing Co.",
    "Tsmc": "Taiwan Semiconductor Manufacturing Co.",
    "tsmc": "Taiwan Semiconductor Manufacturing Co.",

    "MU": "Micron Technology Inc.",
    "Micron": "Micron Technology Inc.",
    "micron": "Micron Technology Inc.",

    "INTC": "Intel Corp.",
    "Intel": "Intel Corp.",
    "intel": "Intel Corp.",

    "ASML": "ASML Holding N.V.",
    "Asml": "ASML Holding N.V.",
    "asml": "ASML Holding N.V.",

    # --- Enterprise Software, Cloud & Cyber ---
    "ORCL": "Oracle Corp.",
    "Oracle": "Oracle Corp.",
    "oracle": "Oracle Corp.",

    "CRM": "Salesforce Inc.",
    "Salesforce": "Salesforce Inc.",
    "salesforce": "Salesforce Inc.",

    "PLTR": "Palantir Technologies Inc.",
    "Palantir": "Palantir Technologies Inc.",
    "palantir": "Palantir Technologies Inc.",

    "NET": "Cloudflare Inc.",
    "Cloudflare": "Cloudflare Inc.",
    "cloudflare": "Cloudflare Inc.",

    "IBM": "International Business Machines Corp.",
    "Ibm": "International Business Machines Corp.",
    "ibm": "International Business Machines Corp.",

    # --- E-Commerce & Consumer Giants ---
    "NFLX": "Netflix Inc.",
    "Netflix": "Netflix Inc.",
    "netflix": "Netflix Inc.",
    "BABA": "Alibaba Group Holding Ltd.",
    "Alibaba": "Alibaba Group Holding Ltd.",
    "alibaba": "Alibaba Group Holding Ltd.",

    "WMT": "Walmart Inc.",
    "Walmart": "Walmart Inc.",
    "walmart": "Walmart Inc.",

    "NKE": "Nike Inc.",
    "Nike": "Nike Inc.",
    "nike": "Nike Inc.",

    # --- Financials & Payments ---
    "V": "Visa Inc.",
    "Visa": "Visa Inc.",
    "visa": "Visa Inc.",

    "MA": "Mastercard Inc.",
    "Mastercard": "Mastercard Inc.",
    "mastercard": "Mastercard Inc.",

    "JPM": "JPMorgan Chase & Co.",
    "Jpmorgan": "JPMorgan Chase & Co.",
    "jpmorgan": "JPMorgan Chase & Co.",

    "GS": "The Goldman Sachs Group Inc.",
    "Goldman": "The Goldman Sachs Group Inc.",
    "goldman": "The Goldman Sachs Group Inc.",

    # --- Energy, Automotive & Biotech/Pharma ---
    "LLY": "Eli Lilly & Co.",
    "Lilly": "Eli Lilly & Co.",
    "lilly": "Eli Lilly & Co.",

    "XOM": "Exxon Mobil Corp.",
    "Exxon": "Exxon Mobil Corp.",
    "exxon": "Exxon Mobil Corp.",

    "CEG": "Constellation Energy Corp.",
    "Constellation": "Constellation Energy Corp.",
    "constellation": "Constellation Energy Corp.",
}

# --- API Key Configuration ---
if hasattr(st, "secrets") and "FINNHUB_API_KEY" in st.secrets:
    FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]

elif os.path.exists(".env"):
    dotenv.load_dotenv()
    # Check if the environment variable is missing or still set to the default placeholder string
    FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY") if os.environ.get(
        "FINNHUB_API_KEY") != "your_finnhub_api_key_here" else "No api key."

    if FINNHUB_API_KEY == "No api key." or FINNHUB_API_KEY is None:
        raise NotImplementedError("Finnhub api key missing or not configured in .env file.")

else:
    raise NotImplementedError("Configuration Error: Neither .env file nor Streamlit Secrets were found.")

# Local print testing
if __name__ == '__main__':
    print(f"FINNHUB_API_KEY: {FINNHUB_API_KEY}")

