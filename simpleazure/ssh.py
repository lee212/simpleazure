from fabric.api import run, env

class SSH:
    def setup(self, host=None, pkey=None):
        env.host_string = host
        env.key_filename = pkey

    def shell(self):
        run('bash')

if __name__ == "__main__":
    #TEST
    a = SSH()
    a.setup(host="azureuser@myvm-81fd6840ae.cloudapp.net",
            pkey="/home/azureuser/.azure/.ssh/myPrivateKey.key")
    a.shell()
