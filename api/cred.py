import json
from getpass import getpass

def make_title(name):
    return ' '.join([p[0].upper() + p[1:] for p in name.split('_')])

CRED = None
def get_cred(name):
    global CRED
    if CRED is None:
        try:
            CRED = json.load(open('cred.json'))
        except (IOError, ValueError):
            CRED = {}
    if name not in CRED:
        if 'password' in name.lower():
            CRED[name] = getpass("%s: " % make_title(name))
        else:
            CRED[name] = raw_input("%s: " % make_title(name))
        json.dump(CRED, open('cred.json', 'w'))
    return CRED[name]
