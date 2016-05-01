import os
import pickle

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

if __name__ == u"__main__":
    pass