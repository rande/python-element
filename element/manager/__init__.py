# vim: set fileencoding=utf-8 :

import re
import hashlib
from uuid import uuid4

uuid_pattern = re.compile('^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{8}$')

def is_uuid(nid):
    """
    check if the provided value is a valid uuid value
    the format must be something like this: fca0ea55-c21b-186e-fe6924a5
    """
    return uuid_pattern.match(nid)

def get_uuid(nid):
    hash = hashlib.sha256(nid).hexdigest()

    return "%s-%s-%s-%s" % (hash[0:8], hash[8:12], hash[12:16], hash[16:24])

def generate_uuid():
    return str(uuid4())

class InvalidTreeState(Exception):
    pass

class InvalidDataFormat(Exception):
    pass
