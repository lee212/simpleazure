# Prototype
from IPython.parallel import Client

class IPythonAPI:

    def __init__(self):
        self.c = Client()

if __name__ == "__main__":
    i = IPythonAPI()
    i.c.ids
    # set([0, 1, 2, 3])
    i.c[:].apply_sync(lambda : "Hello, World") 
    # Expect
    # [ 'Hello, World', 'Hello, World', 'Hello, World', 'Hello, World' ]
