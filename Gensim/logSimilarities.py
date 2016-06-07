#!/usr/bin/env python
import os
import sys
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def stripOutput(s):
    t = s.strip(u"]").strip(u"u'").strip(u"[").strip(u"u'")
    return t

def updateCounts(term, d):
    if isinstance(term, list):
        for t in term:
            if t in d:
                d[t] += 1
            else:
                d[t] = 1
    return d


if __name__ == u"__main__":
    fileSim = u".%srun%sSimilarity.lp" % (os.sep, os.sep)
    fileSimCSV = fileSim[:-3] + u".csv"
    similarities = loadList(fileSim)
    d = dict()

    with open(fileSimCSV, u"wb") as fs:
        fs.write("Doc_n,Doc_m,Similarity,CommonTerms")
        fs.write(os.linesep)

        for similarity in similarities:
            output = u""
            for doc in similarity:
                if isinstance(doc, float):
                    output += u"%3.2f, " % doc
                elif isinstance(doc, (str, unicode)):
                    output += u"%s, " % doc
                elif isinstance(doc, (list, tuple)):
                    line = u":".join([term for term in doc])
                    d = updateCounts(doc, d)
                    output += line

            logger.info(output)
            fs.write(output)
            fs.write(os.linesep)

        logger.info(u"Saved CSV File : %s" % fileSimCSV)

        ds = d.items()

        nds = sorted(ds,key=lambda ds: ds[1], reverse=True)

        fs.write("%sTerm, Frequency%s" % (os.linesep, os.linesep))
        for k, v in nds:
            output = (u"%s,%s" % (k, v))
            logger.info(u"%s" % output)
            fs.write(output)
            fs.write(os.linesep)