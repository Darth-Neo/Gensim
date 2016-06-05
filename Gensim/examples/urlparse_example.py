#!/usr/bin/python
import urllib2
import os
import sys
import getpass
from BeautifulSoup import BeautifulSoup
import cookielib
from pickel_me import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

AGENT = u"Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0"
keywords = u"<meta name='keywords' content='news, breaking news, latest news, current news, world news, national news'>"

if __name__ == u"__main__":

    pages = list()
    urls_file = u"bookmarks.p"
    # pages = load_urls(urls_file)

    pages.insert(0, u"http://www.foxnews.com")

    # Authentication
    # user=getpass.getpass(prompt="UserName : ", stream=sys.stderr)
    # user = "morrj140"
    # print("Username : %s" % user)
    # passwd=getpass.getpass(prompt="Password : ", stream=sys.stderr)

    # Authentication Handler
    # authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # authinfo.add_password(None, SERVER, user, passwd)
    # authHandler = urllib2.HTTPBasicAuthHandler(authinfo)

    # Cookie Handler
    # cj = cookielib.LWPCookieJar()
    # if os.path.isfile(COOKIEFILE):
    #    print("Load Cookies - %s" % COOKIEFILE)
    #    cj.load(COOKIEFILE)

    # cookieHandler = urllib2.HTTPCookieProcessor(cj)

    # urllib2 setup
    # myopener = urllib2.build_opener(authHandler, cookieHandler)
    # opened = urllib2.install_opener(myopener)

    for page in pages:
        logger.info(u"Checking Page : %s" % page)

        try:
            # Request
            request = urllib2.Request(page)
            request.add_header(u"User-Agent", AGENT)

            output = unicode(urllib2.urlopen(request).read(), u"utf-8", errors=u"replace")

            # Clean out up a bit
            soup = BeautifulSoup(output)
            print(u"Title : %s " % soup.title.string)

            tags = soup.findAll(u"meta")
            # tags = soup.findAll(name=u"keywords")

            print(u"Count %d" % len(tags))

            for tag in tags:
                at = tag.attrs
                if isinstance(at, list) and len(at) > 1:
                    for k, v in at:
                        print(u"%s[%s]" % (k, v))
                        if k in (u"name", u"keywords"):
                            print(u"----%s[%s]" % (k, v))
                        if v in (u"keywords",):
                            print(u"++++%s[%s]" % (k, v))
                else:
                    print(u"Tag: %s" % tag)

        except Exception, msg:
            print(u"    Exception .. %s" % msg)

    print os.linesep

    # Show the cookies
    # for x in cj:
    #    print("Cookie : %s" % x)
    # cj.save(COOKIEFILE)
