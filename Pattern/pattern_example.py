#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pattern.web import *
from pattern.text import *
from pattern.text.search import *
from pattern.text import tag, tree, pluralize, singularize

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def logNGRAMS(s,n=2):
    sl = ngrams(s, n=n)
    logger.info(u"NGrams : %d" % n)
    for ns in sl:
        logger.info(u"NGRAMS.%d : [%s]" % (n, ns))

def logPOS(s,lpos=u"NN"):
    tg = tag(s)
    for word, pos in tg:
        if pos == lpos:
            logger.info(u"Word : %s[%s]" % (word, pos))

    return tg

def logChunks(chunks):
    for chunk in chunks:
        logger.info(u"Chunk : %s" % chunk)

def logSentences(sentences):
    for sentence in sentences:
        logger.info(u"Sentence : %s" % sentence)


def logWordsPOS(q):
    for word in q[0].words:
        logger.info(word.string + word.tag)

def h2pt():
    # plaintext = strip + decode + collapse

    # mongodb
    client = MongoClient(u'mongodb://localhost:27017/')
    db = client[u'SolutionEngineeringDB']
    collection = db[u'ProjectDetails']

    cursor = collection.find()
    n = 0
    for pdp in cursor[:5]:
        n += 1
        logger.info(u"%d.%s[%s]" % (n, pdp[u"spider"], pdp[u"last_updated"]))
        html = pdp[u"Text"]

        try:
            s = plaintext(html, keep={u'h1':[], u'h2':[], u'strong':[], u'a':[u'href']})

            tags = logPOS(s)
            txt = Text(tags)

            sentences = Sentence(tags)
            logSentences(sentences)

            chunks = Chunk(sentences)
            logChunks(chunks)

            logNGRAMS(s, n=4)
            logNGRAMS(s, n=3)
            logNGRAMS(s, n=2)

            nps = parse(s, lemmata=True, tags=True, chunks=True)
            ns = parsetree(s)

            # Execute a Regular Expression Search
            p = r'(N[NP])+'
            q = search(p, ns)
            logWordsPOS(q)

        except Exception, msg:
            logger.error(u"%s" % msg)

if __name__ == u"__main__":
    h2pt()
