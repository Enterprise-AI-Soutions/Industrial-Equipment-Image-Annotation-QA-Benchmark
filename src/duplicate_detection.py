from collections import Counter

def find_duplicates(items):
    counts = Counter(items)
    return [k for k,v in counts.items() if v > 1]
