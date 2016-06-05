#!/usr/bin/env python
import demjson

if __name__ == u"__main__":
    json = u"""{"a":1,"b":2,"c":3,"d":4,"e":5}"""

    text = demjson.decode(json)
    print(u"%s" % text)
