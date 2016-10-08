from sh import
from . import config
import os

class GitCmd(object):

    def __init__(self, path):
        self.path = path
        basename = os.path.basename(path)
        self.local_path = config.DEFAULT_PATH + "/" + basename
        self.clone()
'''
     git directory
     get azuredeploy
     azure parameters
     metadata
     nested
     scripts
     etc
'''
    def get_list(self):
        dirnames = [ d for d in os.path.listdir(self.path) if
                not os.path.isfile(os.path.join(path, f))]
        if '.github' in dirnames:
            del(dirnames['.github'])

        return dirnames

    def get_file(self):
        pass

    def clone(self, path=None):
        path = path or self.path
        # IF exists, git pull
        if self.check_if_exist():
            sh.cd(self.local_path)
            sh.git.pull()
        else:
            sh.git.clone(path, self.local_path)

    def check_if_exist(self):
        if os.path.isdir(self.local_path):
            if os.path.isdir(self.local_path + "/.git"):
                return True
        return False
