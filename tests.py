# vim: set fileencoding=utf-8 :

import os.path, sys, glob
import unittest

base = sys.path[0] + '/../..'
sys.path.insert(0, base + "/vendor/ioc")
sys.path.insert(0, base + "/vendor/shirka")
sys.path.insert(0, base + "/vendor/element")

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    for path in glob.glob("tests/*.py"):
        path = path.replace("/",".")[:-3]

        try:
            __import__(path)
            mod = sys.modules[path]

            suite.addTests(loader.loadTestsFromModule(mod))
        except ImportError, e:
            print path, e
            pass

    return suite

if __name__ == "__main__":
    unittest.main()