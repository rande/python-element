# vim: set fileencoding=utf-8 :

import os.path, sys, glob
import unittest

base = sys.path[0] + '/../..'
sys.path.insert(0, base + "/vendor/ioc")
sys.path.insert(0, base + "/vendor/shirka")
sys.path.insert(0, base + "/vendor/element")


def add_tests(suite, loader, path):

    for path in glob.glob(path):
        try:
            path = path.replace("/",".")[:-3]

            __import__(path)
            mod = sys.modules[path]

            suite.addTests(loader.loadTestsFromModule(mod))
        except ImportError, e:
            print path, e
            pass


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    add_tests(suite, loader, "tests/*.py")
    add_tests(suite, loader, "tests/*/*.py")

    return suite

if __name__ == "__main__":
    unittest.main()