#!/usr/bin/env python
import os
from simserver import SessionServer
from gensim import utils
import Pyro4

import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)


class GensimServer(object):

    def __init__(self, output=None):
        pass
        if output is None:
            self.output = u""

    def findSimilarities(self, texts):
        gsDir = os.getcwd()
        logger.debug(u"GSDir %s" % gsDir)

        gss = gsDir + os.sep + u"gensim_server" + os.sep
        logger.debug(u"%s" % gss)

        server = SessionServer(gss)

        corpus = [{u"id": u"doc_%i" % num, u"tokens": utils.simple_preprocess(text)} for num, text in enumerate(texts)]

        # send 1k docs at a time
        # utils.upload_chunked(server, corpus, chunksize=1000)

        # server.train(corpus, method=u"lsi")

        # index the same documents that we trained on...
        # server.index(corpus)

        # overall index size unchanged (just 3 docs overwritten)
        # server.index(corpus[:3])

        # Option Ons
        if True:
            for n in range(0, len(texts)):
                doc = u"doc_%d" % n
                self.output += u"Find similar doc_%d to %s%s" % (n, corpus[n][u"tokens"], os.linesep)
                logger.info(self.output[:-1])

                for sim in server.find_similar(doc):
                    m = int(sim[0][-1:])
                    if m != n:
                        self.output += u"\t%s \t %3.2f : %s%s" % (sim[0], float(sim[1]), corpus[m][u"tokens"], os.linesep)
                        logger.info(self.output[:-1])

                        d = [unicode(x) for x in corpus[n][u"tokens"]]
                        e = [unicode(y) for y in corpus[m][u"tokens"]]

                        s1 = set(e)
                        s2 = set(d)
                        common = s1 & s2
                        lc = [x for x in common]
                        self.output += u"\tCommon Topics : %s%s" % (lc, os.linesep)
                        logger.info(self.output[:-1])

            else:
                # Option two
                doc = {u"tokens": utils.simple_preprocess(u"Graph and minors and humans and trees.")}
                logger.info(u"%s" % server.find_similar(doc, min_score=0.4, max_results=50))

        return self.output


def main():
    gs = GensimServer()
    Pyro4.Daemon.serveSimple({gs: u"org.GensimServer"}, ns=True)

if __name__ == u"__main__":
    main()
