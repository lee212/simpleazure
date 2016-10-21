FROM jupyter/base-notebook

MAINTAINER Hyungro Lee <hyungro.lee@hotmail.com>

USER root

# Compiler
RUN apt-get update && apt-get install git python-pip python-dev libffi-dev libssl-dev -y


# Simple Azure from Github repository
RUN  git clone https://github.com/lee212/simpleazure.git && \
     cd simpleazure && \
     pip install -U requests && \
     pip install -r requirements.txt && \
     python setup.py install
