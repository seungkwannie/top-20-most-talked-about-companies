# import collections
# import config
#
#
# def process_text_frequencies(raw_text_pool):
#     counter = collections.Counter()
#
#     # 1. Quick safety guard clause: if data is empty or None
#     if not raw_text_pool:
#         return []
#
#     for item in raw_text_pool:
#         text_to_process = ""
#
#         if isinstance(item, dict):
#             # CHANGED HERE: Added Finnhub keys 'headline' and 'summary' alongside original fallbacks
#             title = item.get("headline") or item.get("title") or ""
#             description = item.get("summary") or item.get("description") or item.get("content") or ""
#             text_to_process = f"{title} {description}"
#         elif isinstance(item, str):
#             text_to_process = item
#         else:
#             continue
#
#         words_list = text_to_process.lower().split()
#
#         for individual_word in words_list:
#             clean_word = individual_word.strip(",.!?\"'")
#
#             if clean_word in config.COMPANY_LOOKUP:
#                 official_name = config.COMPANY_LOOKUP[clean_word]
#                 counter.update([official_name])
#
#     # Fallback logic for 0 counts remains intact
#     for official_name in set(config.COMPANY_LOOKUP.values()):
#         if official_name not in counter:
#             counter[official_name] = 0
#
#     return counter.most_common(config.DISPLAY_LIMIT)
###########################################################################
# import collections
# import config
#
#
# def process_text_frequencies(raw_text_pool):
#     counter = collections.Counter()
#
#     # 1. Quick safety guard clause: if data is empty or None
#     if not raw_text_pool:
#         return []
#
#     for item in raw_text_pool:
#         text_to_process = ""
#
#         if isinstance(item, dict):
#             # UPDATED HERE: Alpha Vantage maps headlines to 'title' and summaries to 'summary'
#             title = item.get("title") or ""
#             description = item.get("summary") or ""
#             text_to_process = f"{title} {description}"
#         elif isinstance(item, str):
#             text_to_process = item
#         else:
#             continue
#
#         words_list = text_to_process.lower().split()
#
#         for individual_word in words_list:
#             clean_word = individual_word.strip(",.!?\"'")
#
#             if clean_word in config.COMPANY_LOOKUP:
#                 official_name = config.COMPANY_LOOKUP[clean_word]
#                 counter.update([official_name])
#
#     # Fallback logic for 0 counts remains intact
#     for official_name in set(config.COMPANY_LOOKUP.values()):
#         if official_name not in counter:
#             counter[official_name] = 0
#
#     return counter.most_common(config.DISPLAY_LIMIT)

import collections
import config


def process_text_frequencies(raw_articles_pool):
    counter = collections.Counter()

    # 1. Quick safety guard clause: if data is empty or None
    if not raw_articles_pool:
        return []

    # Note: Pass the raw list of dictionaries ('data' payload from Marketaux)
    # instead of a pool of string headlines/summaries.
    for article in raw_articles_pool:
        if not isinstance(article, dict):
            continue

        # 2. Extract entities pre-identified by Marketaux's AI
        entities = article.get("entities", [])

        for entity in entities:
            # Marketaux provides the exact uppercase stock ticker (e.g., 'TSLA', 'AAPL')
            ticker = entity.get("symbol")
            if not ticker:
                continue

            ticker_upper = ticker.upper()

            # 3. Match against your local config lookup dictionary
            # For example, if config.COMPANY_LOOKUP['TSLA'] equals 'Tesla, Inc.'
            if ticker_upper in config.COMPANY_LOOKUP:
                official_name = config.COMPANY_LOOKUP[ticker_upper]
                counter.update([official_name])

            # Alternative fallback: If the ticker isn't explicitly mapped in config,
            # you can use the name Marketaux provides natively in the payload!
            elif entity.get("name"):
                official_name = entity.get("name")
                counter.update([official_name])

    # Fallback logic for 0 counts remains intact
    for official_name in set(config.COMPANY_LOOKUP.values()):
        if official_name not in counter:
            counter[official_name] = 0

    return counter.most_common(config.DISPLAY_LIMIT)
