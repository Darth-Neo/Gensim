#!/usr/bin/env python
# __author__ = "morrj140"
from collections import defaultdict
import Logger
import os
import pytest
from gensim import corpora, models, similarities, matutils, utils
from gensim.models import lsimodel
from simserver import SessionServer

logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)

fileDictionary = u"./run/Dictionary.dict"
fileCorpus = u"./run/corpus.mm"
fileIndex = u"./run/corpus.mm.index"


def logValues(d, traverse=False, n=0):
    if isinstance(d, dict):
        for k, v in d.items():
            print(u"%d.%s[%s]" % (n, k, v))
            n += 1

            if traverse is True:
                logValues(v)

    elif isinstance(d, list):
        for v in d:
            print(u"%d.%s." % (n, v))
            n += 1

            if traverse is True:
                logValues(v)


class MyCorpus(object):
    corpus = None
    dictionary = None

    def __init__(self, corpusFile):

        if os.path.isfile(corpusFile):
            self.corpus = corpora.MmCorpus(corpusFile)

    def __iter__(self):
        for line in self.corpus:
            # assume there"s one document per line, tokens separated by whitespace
            yield self.dictionary.doc2bow(line.lower().split())


def ns(numpy_matrix, number_of_corpus_features, scipy_sparse_matrix):
    corpus = matutils.Dense2Corpus(numpy_matrix)

    # numpy_matrix = matutils.corpus2dense(corpus, num_terms=number_of_corpus_features)

    corpus = matutils.Sparse2Corpus(scipy_sparse_matrix)
    # scipy_csc_matrix = matutils.corpus2csc(corpus)


def updateCorpus(docs):
    nt = 50
    nw = 5

    cwd = os.getcwd()

    fileDictionary = u"./run/Dictionary.dict"
    fileCorpus = u"./run/corpus.mm"
    fileIndex = u"./run/corpus.mm.index"

    dictionary = corpora.Dictionary.load(fileDictionary)
    corpus = MyCorpus(fileCorpus).corpus

    # Dictionary
    logger.debug(u"Dictionary ======================================>")
    n = 0
    for k, v in dictionary.items():
        logger.debug(u"%d.%s[%s]" % (n, k, v))
        n += 1

    # Corpus
        logger.debug(u"Corpus ======================================>")
    n = 0
    for v in corpus:
        logger.debug(u"%d.[%s]\t %s" % (n, v, docs[n]))
        n += 1

    # File Index
    # index = similarities.MatrixSimilarity.load(fileIndex)
    # numpy_matrix = matutils.corpus2dense(corpus, num_terms=nt)
    # logger.info("numpy_matrix[%d]" % (len(index)))
    # for x in numpy_matrix:
    #    logger.info("%s" % x)

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    tfidf = models.TfidfModel(corpus)
    logger.debug(u"tfidf: %s" % str(tfidf))

    corpus_tfidf = tfidf[corpus]
    logger.debug(u"corpus_tfidf: %s" % str(corpus_tfidf))

    # I can print out the topics for LSI
    lsi = lsimodel.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=nt)

    logger.debug(u"LSI Complete")
    corpus_lsi = lsi[corpus]

    logger.debug(u"lsi.print_topics: " + str(lsi.print_topics))

    lsiList = lsi.print_topics(num_topics=nt, num_words=nw)

    n = 0
    print(u"LSI ======================================>")
    for x in lsiList:
        n += 1
        print(u"%d.%s" % (n, x))
        logger.debug(u"LSI: %d %s" % (n, x))


def createCorpus(docs):
    ntexts = u""

    # remove common words and tokenize
    stoplist = set(u"for a of the and to in".split())

    texts = [[word for word in document.lower().split() if word not in stoplist] for document in docs]

    frequency = defaultdict(int)

    for text in texts:
        for token in text:
            frequency[token] += 1

            ntexts = [[token for token in text if frequency[token] > 1] for text in texts]

    n = 0
    for document in docs:
        logger.debug(u"%s\n\t%s" % (document, ntexts[n]))
        n += 1

    diictionary = corpora.Dictionary(ntexts)

    logger.debug(u"Words")
    printValues(diictionary)

    logger.debug(u"Tokens")
    printValues(diictionary.token2id)

    # Document Test to Bag of Words
    corpus = [diictionary.doc2bow(text) for text in ntexts]

    # remove stop words and words that appear only once
    stop_ids = [diictionary.token2id[stopword] for stopword in stoplist if stopword in diictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in diictionary.dfs.iteritems() if docfreq == 1]

    # remove stop words and words that appear only once
    diictionary.filter_tokens(stop_ids + once_ids)

    # remove gaps in id sequence after words that were removed
    diictionary.compactify()

    lsi = models.LsiModel(corpus, id2word=diictionary, num_topics=4)

    doc = docs[0]

    vec_bow = diictionary.doc2bow(doc.lower().split())

    # convert the query to LSI space
    logger.debug(u"LSI %s" % doc)
    vec_lsi = lsi[vec_bow]
    logger.debug(vec_lsi)

    # transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])

    # perform a similarity query against the corpus
    sims = index[vec_lsi]

    # print (document_number, document_similarity) 2-tuples
    logger.debug(u"Simularity")
    n = 0
    for v in list(enumerate(sims)):
        logger.debug(u"%d.%s.%s" % (n, v, docs[n]))
        logger.debug(u"\t%s" % ntexts[n])
        n += 1

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    diictionary.save(fileDictionary)
    corpora.MmCorpus.serialize(fileCorpus, corpus)
    lsi.save(fileIndex)


@pytest.fixture(scope=u"module")
def getTexts():
    texts = [u"Human machine interface for lab abc computer applications",
             u"A survey of user opinion of computer system response time",
             u"The EPS user interface management system",
             u"System and human system engineering testing of EPS",
             u"Relation of user perceived response time to error measurement",
             u"The generation of random binary unordered trees",
             u"The intersection graph of paths in trees",
             u"Graph minors IV Widths of trees and well quasi ordering",
             u"Graph minors A survey",
             u"Why use a computer"]

    return texts


@pytest.mark.Gensim
def test_Gensim(texts):
    gsDir = os.getcwd()
    logger.debug(u"GSDir %s" % gsDir)

    gss = gsDir + os.sep + u"gensim_server" + os.sep
    logger.debug(u"%s" % gss)

    server = SessionServer(gss)

    u""" texts = [u"Human machine interface for lab abc computer applications",
             u"A survey of user opinion of computer system response time",
             u"The EPS user interface management system",
             u"System and human system engineering testing of EPS",
             u"Relation of user perceived response time to error measurement",
             u"The generation of random binary unordered trees",
             u"The intersection graph of paths in trees",
             u"Graph minors IV Widths of trees and well quasi ordering",
             u"Graph minors A survey",
             u"Why use a computer"]
    """

    logger.info(u"%s" % server.status())

    corpus = [{u"id": u"doc_%i" % num, u"tokens": utils.simple_preprocess(text)} for num, text in enumerate(texts)]

    # send 1k docs at a time
    utils.upload_chunked(server, corpus, chunksize=1000)

    server.train(corpus, method=u"lsi")

    # index the same documents that we trained on...
    server.index(corpus)

    # supply a list of document ids to be removed from the index
    # server.delete(["doc_5", "doc_8"])

    # overall index size unchanged (just 3 docs overwritten)
    server.index(corpus[:3])

    # Option Ons
    for n in range(0, len(texts)):
        doc = u"doc_%d" % n
        logger.info(u"Find similar doc_%d to %s" % (n, corpus[n][u"tokens"]))
        for sim in server.find_similar(doc):
            m = int(sim[0][-1:])
            if m != n:
                logger.info(u"\t%s \t %3.2f : %s" % (sim[0], float(sim[1]), corpus[m][u"tokens"]))

                d = [unicode(x) for x in corpus[n][u"tokens"]]
                e = [unicode(y) for y in corpus[m][u"tokens"]]

                s1 = set(e)
                s2 = set(d)
                common = s1 & s2
                lc = [x for x in common]
                logger.info(u"\tCommon Topics : %s\n" % (lc))

    if False:
        # Option two
        doc = {u"tokens": utils.simple_preprocess(u"Graph and minors and humans and trees.")}
        logger.info(u"%s" % server.find_similar(doc, min_score=0.4, max_results=50))

    # Pyro4 example
    # service = Pyro4.Proxy(Pyro4.locateNS().lookup("gensim.testserver"))

if __name__ == u"__main__":
    test_Gensim(getTexts())
