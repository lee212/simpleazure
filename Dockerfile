FROM ubuntu:14.04

MAINTAINER Hyungro Lee <hyungro.lee@hotmail.com>

# Compiler
RUN apt-get update && apt-get install git python-pip python-dev libffi-dev -y

# Simple Azure from Github repository
RUN  git clone https://github.com/lee212/simpleazure.git && \
     cd simpleazure && \
     pip install -r requirements.txt && \
     python setup.py install
