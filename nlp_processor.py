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

    # Process the raw list of dictionaries returned from the GDELT API request
    for article in raw_articles_pool:
        if not isinstance(article, dict):
            continue

        # 2. Extract the headline title text from the GDELT payload
        # GDELT uses lowercase keys like 'title', 'url', and 'seendate'
        title_text = article.get("title", "")
        if not title_text:
            continue

        # Convert to lowercase once per article for case-insensitive matching
        title_text_lower = title_text.lower()

        # 3. Scan the title text for your configured companies
        for ticker, full_name in config.COMPANY_LOOKUP.items():
            # Strip out generic business suffixes ("Inc.", "Corp.") to match how journalists write headlines
            clean_name = full_name.replace("Inc.", "").replace("Corp.", "").replace("com", "").strip()
            clean_name_lower = clean_name.lower()

            # Check if either the natural name or the stock symbol is explicitly mentioned in the headline text
            # e.g., matching "Tesla" or "TSLA" inside "TSLA stock spikes as Tesla launches new feature"
            if clean_name_lower in title_text_lower or f" {ticker.lower()} " in f" {title_text_lower} ":
                counter.update([full_name])

    # 4. Fallback logic for 0 counts remains completely intact
    for official_name in set(config.COMPANY_LOOKUP.values()):
        if official_name not in counter:
            counter[official_name] = 0

    return counter.most_common(config.DISPLAY_LIMIT)
