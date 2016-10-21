import os
from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg

class SimpleAzureInstall(bdist_egg):
    def run(self):
        bdist_egg.run(self)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#reqs = [line.strip() for line in open('requirements.txt')]
setup(
        name = "simpleazure",
        version = "0.0.6",
        author = "Hyungro Lee",
        author_email = "hroe.lee@gmail.com",
        description = ("Python Library for Windows Azure"),
        license = "GPLv3",
        keywords = "SimpleAzure, Azure, Template deployment",
        url = "https://github.com/lee212/simpleazure",
        packages = [
            'simpleazure',
            'simpleazure/ext',
            'simpleazure/template',
            ],
        install_requires = [
            "azure==2.0.0rc6",
            "pyaml",
            "fabric",
            "haikunator", # random name generator
            "sh",
            "cython", # for pandas
            "pandas" # will be replaced
            ], 
        # reqs is removed and pip install -r requirements.txt added
        # because 'import azure' wrongly imported from azure-nspkg package
        dependency_links = ['https://github.com/Azure/azure-sdk-for-python.git'],
        long_description = read('README.rst'),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Scientific/Engineering",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            ],
        entry_points='''
            [console_scripts]
            ''',

        cmdclass={'bdist_egg': SimpleAzureInstall},  # override bdist_egg
        )

