#!/usr/bin/env python
# __author__ = "morrj140"
from pymongo import MongoClient

import os
from gensim import utils
from simserver import SessionServer
from stopWords import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

similarity = 0.80

def stripTokens(words):

    stripped = u""
    stopped = u""
    newWords = u""

    for word in words.split():
        if word in strp:
            stripped += word + u" "
        elif word in stop:
            stopped += word + u" "
        else:
            newWords += word + u" "

    return newWords, stopped, stripped

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

        text = u"%s,%s" % (text, os.linesep)
        words.append(text)
        logger.debug(u"Text : %s" % text[:50])

    except Exception, msg:
        logger.debug(u"%s" % msg)

    return words

def getTexts(fileText):
    if True:
        texts = list()

        with open(fileText, u"rb") as f:
            lines = f.readlines()

            lines = lines[0].decode(u"utf-8", errors=u"replace")
            for x in lines.split(u"\r"):
                try:
                    y = x.split(u",")[0].strip(u"\"\"")
                    y, stopped, stripped = stripTokens(y)
                    texts.append(y)
                except Exception, msg:
                    logger.error(u"%s" % msg)

        logger.info(u"Texts : %d" % len(texts))
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

        logger.info(u"Texts : %d" % len(texts))
        return texts

def findSimilar(texts, server, corpus):

    similarities = list()

    # Option Ons
    for n in range(0, len(texts)):
        doc_n = u"doc_%d" % n
        logger.info(u"%s" % doc_n)
        try:
            for sim in server.find_similar(doc_n):
                doc_m = sim[0]
                doc_similarity = float(sim[1])
                # Compares 'doc_m' to 'doc_n'
                if doc_m != doc_n and doc_similarity > similarity:
                    mi = int(doc_m.index(u"_") + 1)
                    nm = int(doc_m[mi:])

                    d = [unicode(x) for x in corpus[n][u"tokens"]]
                    e = [unicode(y) for y in corpus[nm][u"tokens"]]

                    s1 = set(e)
                    s2 = set(d)
                    common = s1 & s2
                    lc = [x for x in common]

                    if len(lc) == 0:
                        logger.error(u"Something is wrong here!")
                        raise Exception
                    else:
                        similar = list()
                        similar.append(doc_n)
                        similar.append(doc_m)
                        similar.append(float(sim[1]))
                        similar.append(lc)
                        similarities.append(similar)

                        logger.info(u"\t%s\t%s\t%3.2f\tCommon : %s" % (doc_n, doc_m, doc_similarity, lc))

        except Exception, msg:
            logger.error(u"%s", msg)

        if False:
            # Option two
            doc = {u"tokens": utils.simple_preprocess(u"Graph and minors and humans and trees.")}
            logger.info(u"%s" % server.find_similar(doc, min_score=0.4, max_results=50))
            logger.error(u"%s - %d : %d" % (msg, nm, n))

    return similarities

def GensimClient(texts):
    similarities = None

    gsDir = os.getcwd()
    gss = gsDir + os.sep + u"gensim_server" + os.sep
    server = SessionServer(gss)

    logger.debug(u"%s" % server.status())

    try:
        corpus = [{u"id": u"doc_%i" % num, u"tokens": utils.simple_preprocess(text)} for num, text in enumerate(texts)]

        # send 1k docs at a time
        utils.upload_chunked(server, corpus, chunksize=1000)

        server.train(corpus, method=u"lsi")

        # index the same documents that we trained on...
        server.index(corpus)

        similarities = findSimilar(texts, server, corpus)

    except Exception, msg:
        logger.debug(u"%s" % msg)

    return similarities


if __name__ == u"__main__":

    runDdir = u'.%srun' % os.sep
    if not os.path.isdir(runDdir):
        os.makedirs(runDdir)

    fileRequirements = u"..%sPMIS Requirements_v3.csv" % os.sep
    fileSimilarities = u"run%sSimilarity.lp" % os.sep

    if True:
        similarities = GensimClient(getTexts(fileRequirements))
    else:
        similarities = GensimClient(getTextsFromMongoDB())

    saveList(similarities, fileSimilarities)
