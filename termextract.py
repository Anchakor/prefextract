# -*- coding: utf-8 -*-

import re
from htmlentitydefs import name2codepoint
import topia.termextract.extract
keywordExtractor = topia.termextract.extract.TermExtractor()

def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint),
        lambda m: unichr(name2codepoint[m.group(1)]), s)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def getKeywords(str):
    # keyword tagging

    str = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:/\+\-"\'&\.,; ]', ' ', str)
    str = htmlentitydecode(str)
    str = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:/\+\-&\., ]', ' ', str)
    keywords0 = sorted(keywordExtractor(str))
    # var keywords1: all keywords
    keywords1 = map(lambda x: x[0], keywords0)
    # var keywords2: keywords appearing at least 2x
    keywords2 = map(lambda x: x[0], [y for y in keywords0 if y[1] > 1])
    keywords = keywords2
    if(len(keywords) < 3):
        keywords = keywords + keywords1[:5]

    return f7(keywords)
