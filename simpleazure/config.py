# -*- coding: utf-8 -*-

"""
config.Config
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""
import os
import yaml
from . import utils

DEFAULT_AZURE_CONFIG_PATH = os.environ["HOME"] + '/.azure'
CLUSTER_DIR = '/cluster'

def config_path():
    return DEFAULT_AZURE_CONFIG_PATH

def azure_path():
    return config_path()

def cluster_path():
    return config_path() + CLUSTER_DIR

def set_cluster_conf(name, data):
    utils.ensure_dir_exists(cluster_path())
    yaml_name = name + ".yaml"
    f = open(cluster_path() + "/" + yaml_name, "w")
    yaml.dump(data, f)
    f.close()

def get_cluster_conf(name):
    utils.ensure_dir_exists(cluster_path())
    yaml_name = name + ".yaml"
    f = open(cluster_path() + "/" + yaml_name)
    data = yaml.load(f)
    f.close
    return data
