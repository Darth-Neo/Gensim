#!/usr/bin/envpython
# from __future__ import print_function
import Pyro4
import person


class Warehouse(object):
    def __init__(self):
        self.contents = [u"chair", u"bike", u"flashlight", u"laptop", u"couch"]

    def list_contents(self):
        return self.contents

    def take(self, name, item):
        self.contents.remove(item)
        print(u"%s took the %s." % (name, item))

    def store(self, name, item):
        self.contents.append(item)
        print(u"%s stored the %s." % (name, item))


def main():
    warehouse = Warehouse()
    Pyro4.Daemon.serveSimple({warehouse: u"example.warehouse"}, ns=True)


if __name__ == u"__main__":
    main()
