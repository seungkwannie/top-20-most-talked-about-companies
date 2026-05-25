import collections
import config


def process_text_frequencies(raw_text_pool):
    counter = collections.Counter()

    # 1. Quick safety guard clause: if data is empty or None
    if not raw_text_pool:
        return []

    for item in raw_text_pool:
        # 2. Extract the actual text string from the item
        text_to_process = ""

        if isinstance(item, dict):
            title = item.get("title") or ""
            description = item.get("description") or item.get("content") or ""
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

    # Keep your fallback logic for 0 counts intact
    for official_name in set(config.COMPANY_LOOKUP.values()):
        if official_name not in counter:
            counter[official_name] = 0

    return counter.most_common(config.DISPLAY_LIMIT)