# This is the code that visits the warehouse.
import sys
import Pyro4
import Pyro4.util
from person import Person

if __name__ == u"__main__":
    try:
        sys.excepthook = Pyro4.util.excepthook

        # warehouse = Pyro4.Proxy(u"PYRO:obj_37f0c85cb9b34499900ec562f2258b3c@localhost:54249")
        warehouse = Pyro4.Proxy(u"PYRONAME:example.warehouse")

        janet = Person(u"Janet")
        henry = Person(u"Henry")
        janet.visit(warehouse)
        henry.visit(warehouse)

    except ValueError, msg:
        pass
