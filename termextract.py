import topia.termextract.extract
keywordExtractor = topia.termextract.extract.TermExtractor()

def getKeywords(str):
    # keyword tagging

    keywords0 = sorted(keywordExtractor(str))
    # var keywords1: all keywords
    keywords1 = map(lambda x: x[0], keywords0)
    # var keywords2: keywords appearing at least 2x
    keywords2 = map(lambda x: x[0], [y for y in keywords0 if y[1] > 1])
    keywords = keywords2

    return keywords
