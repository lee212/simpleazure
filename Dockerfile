FROM ubuntu:14.04

MAINTAINER Hyungro Lee <hroe.lee@gmail.com>

# Compiler
RUN apt-get update 

# Simple Azure from Github repository
RUN  git clone https://github.com/lee212/simpleazure.git && \
     cd simpleazure && \
     pip install -r requirements.txt && \
     python setup.py install
