FROM ubuntu:14.04

MAINTAINER Hyungro Lee <hyungro.lee@hotmail.com>

# prerequisites for simpleazure
RUN apt-get update && apt-get install git python-pip python-dev libffi-dev libssl-dev -y

# npm for azure xplat cli
RUN apt-get install nodejs-legacy npm -y

# azure-cli
RUN npm install -g azure-cli

# Simple Azure from Github repository
RUN  git clone https://github.com/lee212/simpleazure.git && \
     cd simpleazure && \
     pip install -U requests && \
     pip install -r requirements.txt && \
     python setup.py install
