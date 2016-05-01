import os
import json
from pickel_me import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def save_urls(urls, urls_file):
    try:
        logger.info(u"Saving urls : %s" % urls_file)
        cf = open(urls_file, u"wb")
        pickle.dump(urls, cf)
        cf.close()

    except IOError, msg:
        logger.error(u"%s - %s " % msg)


def load_urls(urls_file):
    urls = None

    if not os.path.exists(urls_file):
        logger.error(u"%s : Does Not Exist!" % urls_file)

    try:
        cf = open(urls_file, u"rb")
        urls = pickle.load(cf)
        logger.info(u"Loaded urls : %s" % urls_file)
        cf.close()

    except IOError, msg:
        logger.error(u"%s - %s " % msg)

    return urls


def rp(d, urls, n=0):

    n += 1

    spaces = u" " * n

    if isinstance(d, list):
        for v in d:
            if isinstance(v, dict) or isinstance(v, list):
                rp(v, urls, n)
            else:
                logger.debug(u"%s%d - %s" % (spaces, n, v))

    elif isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, list) or isinstance(v, dict):
                rp(v, urls, n)
            else:
                if k == u"url":
                    urls.append(v)
                logger.debug(u"%s%d - %s[%s]" % (spaces, n, k, v))
    else:
        logger.debug(u"%s%d - %s" % (spaces, n, d))

    return urls

if __name__ == u"__main__":
    urls = list()
    urls_file = u"bookmarks.p"
    filename = u"Bookmarks.json"

    if True:
        with open(filename, "r") as json_file:
            json_data = json.load(json_file)
            urls = rp(json_data, urls)

        save_urls(urls, urls_file)

        logger.info(u"URL Extraction Complete")

    else:
        urls = load_urls(urls_file)
        m = 0
        for x in urls:
            m += 1
            logger.info(u"URL%d - %s%s" % (m, x, os.linesep))
