import collections, config

def process_text_frequencies(raw_text_pool):
    counter = collections.Counter()
    for word in raw_text_pool:
        words_list = word.lower().split()
        
        for individual_word in words_list:
            clean_word = individual_word.strip(",.!?\"'")
            
            
            if clean_word in config.COMPANY_LOOKUP:
                official_name = config.COMPANY_LOOKUP[clean_word]
                counter.update([official_name])
    
    for official_name in set(config.COMPANY_LOOKUP.values()):
        if official_name not in counter:
            counter[official_name] = 0
    
    return counter.most_common(config.DISPLAY_LIMIT)