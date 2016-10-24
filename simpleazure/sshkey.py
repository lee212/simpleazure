import os

class SSHKey(object):

    pvkey = None
    pubkey = None
    pubkey_path = None
    pvkey_path = None

    default_path = { 
            'pvkey': "~/.ssh/id_rsa",
            'pubkey': "~/.ssh/id_rsa.pub" 
            }

    def __init__(self, path=None):
        self.set_pubkey(path)

    def set_pubkey(self, path=None):
        try:
            path = os.path.expanduser(path or self.default_path['pubkey'])
            with open(path, "r") as f:
                self.pubkey = f.read()
                f.close()
                self.pubkey_path = path
                return True
        except Exception as e:
            # debug / log 
            # print (e)
            return False
