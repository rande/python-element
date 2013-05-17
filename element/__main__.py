import shutil, argparse, sys, os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False, prog="python -m element") 
    parser.add_argument('destination', help="the destination folder")
    
    # the first entry contains the current script location
    argv = sys.argv.pop(0)

    options = parser.parse_args(sys.argv)

    source = "%s/standalone/skeleton" % os.path.dirname(os.path.realpath(__file__))

    print "Python Element ~ Quick Setup"
    print ""
    print "1. Installing code "
    print "  - from: `%s` " % source
    print "  -   to: `%s` ... " % options.destination
    
    shutil.copytree(source, options.destination)

    print 
    print "2. You can now run the small demo project:"
    print "  cd %s" % options.destination
    print "  python start.py flask:start --host=127.0.0.1 --port=80"
    print 
    print "3. Open a browser and go to http://127.0.0.1"
    print ""
    print "--"
    print "Python Element - Thomas Rabaix <thomas.rabaix@gmail.com>"

