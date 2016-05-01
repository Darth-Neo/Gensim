#!/usr/bin/env python
# __author__ = "morrj140"
import Logger
import os
from gensim import utils
from ReadConf import *
from simserver import SessionServer

logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)


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


def GensimClient(texts):
    gsDir = os.getcwd()
    logger.debug(u"GSDir %s" % gsDir)

    gss = gsDir + os.sep + u"gensim_server" + os.sep
    logger.debug(u"%s" % gss)

    server = SessionServer(gss)

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


if __name__ == u"__main__":
    GensimClient(getTexts())
