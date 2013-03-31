
import nltk
import string

# use brown or webtext corpus
corpus = nltk.corpus.brown.words()
corpusSize = len(corpus)
corpusWordFd = nltk.FreqDist(corpus)

def tag(str, minOccurance=2, wordN=8):
    tokens1 = nltk.wordpunct_tokenize(str)
    tokens = [w for w in tokens1 if not w.lower() in nltk.corpus.stopwords.words('english')]
    tokens = [''.join(c for c in s if c not in string.punctuation) for s in tokens]
    tokens = [s for s in tokens if s] # clear empty words

    #this takes tooooo long: tfidfTokens = map(lambda x: corpusCollection.tf_idf(x, tokens), [tokens[4]])

    # frequency distribution how often a word in the tokenized text
    wordFd = nltk.FreqDist(tokens1)

    tok2 = [t for t in tokens if wordFd[t] >= minOccurance]
    x = map(lambda x: (x, wordFd.freq(x) - corpusWordFd.freq(x)), tok2)
    x = list(set(x))
    x = sorted(x, key=lambda tup: tup[1], reverse=True)
    x = x[:wordN]
    x = map(lambda w: w[0], x)
    return x

