#!/usr/bin/env python
# __author__ = "morrj140"
import os
from ReadConf import *
import Pyro4

import Logger
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

    # Pyro4 example
    check = Pyro4.locateNS().lookup(u"org.GensimServer")
    server = Pyro4.Proxy(check)

    output = server.findSimilarities(getTexts())

    logger.info(u"%s%s" % (os.linesep, output))

if __name__ == u"__main__":
    GensimClient(getTexts())
