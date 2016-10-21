# python 3+
#FROM jupyter/base-notebook 
# python 2.7
FROM jupyter/scipy-notebook

MAINTAINER Hyungro Lee <hyungro.lee@hotmail.com>

USER root

# Compiler
RUN apt-get update && apt-get install git python-pip python-dev libffi-dev libssl-dev -y

# Simple Azure from Github repository
RUN  git clone https://github.com/lee212/simpleazure.git && \
     cd simpleazure && \
     pip2 install -r requirements.txt && \
     $CONDA_DIR/envs/python2/bin/python setup.py install

#'jovyan' from base-notebook docker image. it is a unprivileged user `jovyan` (uid=1000,
#configurable, see options) in group `users` (gid=100) with ownership over
#`/home/jovyan` and `/opt/conda`
USER $NB_USER


