#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
    print "  python start.py element:demo:fixtures"
    print "  python start.py tornado:start --verbose -d"
    print 
    print "3. Open a browser and go to http://127.0.0.1:5000"
    print ""
    print "--"
    print "Python Element - Thomas Rabaix <thomas.rabaix@gmail.com>"

