#!/usr/bin/env python
import os
from simserver import SessionServer

if __name__ == u"__main__":
    gsDir = os.getcwd()
    print u"GSDir %s" % gsDir

    gss = gsDir + os.sep + u"gensim_server" + os.sep
    print(u"%s" % gss)

    server = SessionServer(gss)

    print server

    try:
        bye = input(u"Pause")

    except Exception, msg:
        pass
