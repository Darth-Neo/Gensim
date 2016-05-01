#!/usr/bin/env python
import sys

import Pyro4.util

if __name__ == u"__main__":
    try:
        sys.excepthook = Pyro4.util.excepthook

        gs = Pyro4.Proxy(u"PYRONAME:org.GensimServer")

        print gs

    except ValueError, msg:
        pass
