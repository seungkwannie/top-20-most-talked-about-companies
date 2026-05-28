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

import collections
import config


def process_text_frequencies(raw_text_pool):
    counter = collections.Counter()

    # 1. Quick safety guard clause: if data is empty or None
    if not raw_text_pool:
        return []

    for item in raw_text_pool:
        text_to_process = ""

        if isinstance(item, dict):
            # UPDATED HERE: Alpha Vantage maps headlines to 'title' and summaries to 'summary'
            title = item.get("title") or ""
            description = item.get("summary") or ""
            text_to_process = f"{title} {description}"
        elif isinstance(item, str):
            text_to_process = item
        else:
            continue

        words_list = text_to_process.lower().split()

        for individual_word in words_list:
            clean_word = individual_word.strip(",.!?\"'")

            if clean_word in config.COMPANY_LOOKUP:
                official_name = config.COMPANY_LOOKUP[clean_word]
                counter.update([official_name])

    # Fallback logic for 0 counts remains intact
    for official_name in set(config.COMPANY_LOOKUP.values()):
        if official_name not in counter:
            counter[official_name] = 0

    return counter.most_common(config.DISPLAY_LIMIT)
