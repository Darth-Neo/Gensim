#!/usr/bin/env python
# __author__ = "morrj140"
from pymongo import MongoClient
import Logger
import os
from gensim import utils
from simserver import SessionServer

logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)

similarity = 0.50

def getTextsFromMongoDB():
    text = u""
    texts = u""
    words = list()

    # mongodb
    client = MongoClient(u"mongodb://localhost:27017/")
    db = client[u"SolutionEngineeringDB"]
    textDetails = db[u"TextDetails"]

    if True:
        db.Gensim.remove()

    try:
        cursor = textDetails.find()
        for pdp in cursor:
            text = u""
            for word in pdp[u"Tags"]:
                text = u"%s%s " % (text, word[0])


        text = u"%s,%s" % (text,os.linesep)
        words.append(text)
        logger.debug(u"Text : %s" % text[:50])

    except Exception,msg:
        logger.debug(u"%s" % msg)

    return words


def getTexts():

    if True:
        texts = list()

        with open(u"../PMIS Requirements.csv", u"rb") as f:
            lines = f.readlines()

            lines = lines[0].decode(u"utf-8", errors=u"replace")
            for x in lines.split(u"\r"):
                try:
                    y = x.split(u",")[0].strip(u"\"\"")
                    texts.append(y)
                except Exception, msg:
                    logger.error(u"%s" % msg)

        logger.debug(u"Texts : %d" % len(texts))
        return texts
    else:
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

    logger.debug(u"%s" % server.status())

    try:
        corpus = [{u"id": u"doc_%i" % num, u"tokens": utils.simple_preprocess(text)} for num, text in enumerate(texts)]

        # send 1k docs at a time
        utils.upload_chunked(server, corpus, chunksize=1000)

        server.train(corpus, method=u"lsi")

        # index the same documents that we trained on...
        server.index(corpus)

    except Exception, msg:
        logger.debug(u"%s" % msg)

    # Option Ons
    for n in range(0, len(texts)):
        doc = u"doc_%d" % n

        try:
            for sim in server.find_similar(doc):
                m = sim[0]

                # Compares 'doc_m' to 'doc_n'
                if sim[0] != doc:

                    if float(sim[1]) > similarity:

                        logger.info(u"++Find similar doc_%d to %s" % (n, corpus[n][u"tokens"],))

                        mi = int(m.index(u"_") + 1)
                        nm = int(m[mi:])

                        logger.info(u"\t%s %3.2f %s" % (sim[0], sim[1], corpus[nm][u"tokens"]))

                        logger.info(u"Within Threshold : %s\t%s \t %3.2f" % (m[mi:], sim[0], float(sim[1])))

                        d = [unicode(x) for x in corpus[n][u"tokens"]]
                        e = [unicode(y) for y in corpus[nm][u"tokens"]]

                        s1 = set(e)
                        s2 = set(d)
                        common = s1 & s2
                        lc = [x for x in common]

                        if len(lc) > 3:
                            logger.info(u"\t===>Common Topics : %s%s" % (lc, os.linesep))
        except Exception, msg:
            logger.error(u"%s - %d : %d" % (msg, nm, n))

    if False:
        # Option two
        doc = {u"tokens": utils.simple_preprocess(u"Graph and minors and humans and trees.")}
        logger.info(u"%s" % server.find_similar(doc, min_score=0.4, max_results=50))


if __name__ == u"__main__":

    if True:
        GensimClient(getTexts())
    elif False:
        GensimClient(getTextsFromMongoDB())
    else:
        with open(u"V1_RTP_Requirements.csv", "rb") as f:
            text = f.readlines()

        GensimClient(text)
