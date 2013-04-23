import topia.termextract.extract
keywordExtractor = topia.termextract.extract.TermExtractor()

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def getKeywords(str):
    # keyword tagging

    keywords0 = sorted(keywordExtractor(str))
    # var keywords1: all keywords
    keywords1 = map(lambda x: x[0], keywords0)
    # var keywords2: keywords appearing at least 2x
    keywords2 = map(lambda x: x[0], [y for y in keywords0 if y[1] > 1])
    keywords = keywords2
    if(len(keywords) < 3):
        keywords = keywords + keywords1[:5]

    return f7(keywords)
