import sh
from . import config
import os

class GithubCLI(object):

    def __init__(self, path=None):
        if path:
            self.clone(path)

    '''
         git directory
         get azuredeploy
         azure parameters
         metadata
         nested
         scripts
         etc
    '''
    def get_list(self, path=None):
        if not self.cloned:
            print ("fatal: clone first")
            return
        if not path:
            path = self.local_path
        try:
            dirnames = [ d for d in os.listdir(path) if
                    not os.path.isfile(os.path.join(path, d))]
        except Exception as e:
            dirnames = []
        # TODO: Delete (azure quickstart templates only)
        if '.github' in dirnames:
            del(dirnames[dirnames.index('.github')])

        return dirnames

    def get_file(self, path):
        if not self.cloned:
            print ("fatal: clone first")
            return
        try:
            with open(os.path.join(self.local_path, path)) as f:
                content = f.read()
        except IOError as e:
            with open(path, "r") as f:
                content = f.read()
        except Exception as e:
            print ("fatal: {0}".format(e))
            return
                
        return content

    def set_repo(self, path):
        self.path = path
        self.name = os.path.basename(path).split(".")[0]
        self.local_path = os.path.join(config.DEFAULT_PATH, self.name)

    def clone(self, path=None):
        path = path or self.path
        self.set_repo(path)
        # IF exists, git pull
        if self.is_cloned():
            sh.cd(self.local_path)
            try:
                sh.git.pull(_out="/dev/null", _err="/dev/null")
            except Exception as e:
                print (e)
        else:
            try:
                sh.git.clone(path, self.local_path, _out="/dev/null", _err="/dev/null")
            except Exception as e:
                print (e)

    def is_cloned(self):
        if os.path.isdir(self.local_path):
            if os.path.isdir(os.path.join(self.local_path, ".git")):
                self.cloned = True
                return True
        return False
