#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pattern.web import *
from pattern.text import *
from pattern.text.search import *
from pattern.text import tag, tree, pluralize, singularize
from stopWords import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def logNGRAMS(s,n=2):
    sl = ngrams(s, n=n)
    logger.debug(u"NGrams : %d" % n)
    for ns in sl:
        logger.debug(u"NGRAMS.%d : [%s]" % (n, ns))

    return sl

def stripTokens(word):
    for nw in strp:
        word = word.strip(nw)

    return word

def processPOS(s):
    w = u""
    tg = tag(s)
    n = 0
    m = 0
    newTags = list()

    for word, pos in tg:
        if word not in stop:
            if len(word) > 1:
                m += 1
                w = singularize(word)
                tg = list()
                tg.append(word)
                tg.append(pos)
                newTags.append(tg)
                logger.debug(u"%d.Keep    : %s [%s]" % (m, w, pos))
        else:
            n += 1
            logger.debug(u"%d.========> Dropped : %s[%s]" % (n, word, pos))
    return newTags, m, n

def setupMongoDB():
    # mongodb
    client = MongoClient(u"mongodb://localhost:27017/")
    db = client[u"SolutionEngineeringDB"]
    projectDetails = db[u"ProjectDetails"]
    textDetails = db[u"TextDetails"]

    if True:
        db.TextDetails.remove()

    return projectDetails, textDetails

def getValue(value):
    v = u""
    try:
        v = value[0]
        return v
    except Exception, msg:
        logger.debug(u"%s" % msg)

    return v

def h2pt():
    wst = u""
    
    start_time = startTimer()

    # mongodb
    projectDetails, textDetails = setupMongoDB()

    cursor = projectDetails.find()
    n = 0
    for pdp in cursor:
        n += 1

        try:
            logger.debug(u"%d.%s[%s]" % (n, pdp[u"spider"], pdp[u"last_updated"]))
            html = pdp[u"Text"]

            if html is None or len(html) == 0:
                logger.warn(u"html is None for %s:%s:%s:%s" %
                            (pdp[u"project"], pdp[u"server"],
                             pdp[u"spider"], pdp[u"Url"]))
                continue

            s = plaintext(html, keep={u'h1':[], u'h2':[], u'strong':[], u'a':[]})

            wst = stripTokens(s)

            tags, kept, dropped = processPOS(wst)

            logger.info(u"Kept : %d\tDropped : %d" % (kept, dropped))

            sl4 = logNGRAMS(wst, n=4)
            sl3 = logNGRAMS(wst, n=3)
            sl2 = logNGRAMS(wst, n=2)

            # Execute a Regular Expression Search
            ns = parsetree(wst)
            p = r'(N[NP])+'
            q = search(p, ns)

            md = dict()
            md[u"Tags"] = tags
            md[u"NG2"] = getValue(sl2)
            md[u"NG3"] = getValue(sl3)
            md[u"NG4"] = getValue(sl4)
            md[u"Words"] = getValue(q)
            textDetails.insert(dict(md))

        except Exception, msg:
            logger.debug(u"%s" % msg)

    stopTimer(start_time)

if __name__ == u"__main__":
    h2pt()
