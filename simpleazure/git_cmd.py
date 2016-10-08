import sh
from sh import git
from . import config
import os

class GitCmd(object):

    def __init__(self, path):
        self.path = path
        basename = os.path.basename(path).split(".")[0]
        self.local_path = os.path.join(config.DEFAULT_PATH, basename)
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
        dirnames = [ d for d in os.listdir(self.local_path) if
                not os.path.isfile(os.path.join(self.local_path, d))]
        if '.github' in dirnames:
            print dirnames
            del(dirnames[dirnames.index('.github')])

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
            if os.path.isdir(os.path.join(self.local_path, ".git")):
                return True
        return False
