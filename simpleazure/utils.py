# -*- coding: utf-8 -*-

"""
utils
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a Python library for Windows Azure Virtual Machines.

 :copyright: TBD
 :license: TBD

"""

import os
import random
from haikunator import Haikunator

def ensure_dir_exists(directory):
    try:
        if not os.path.exists(directory):
                os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
           raise

# Reference: http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
def generate_password(length=8, lower=True, upper=True, number=True):
    lletters = "abcdefghijklmnopqrstuvwxyz"
    uletters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # This doesn't guarantee both lower and upper cases will show up
    alphabet = lletters + uletters
    digit = "0123456789"
    mypw = ""

    def _random_character(texts):
        return texts[random.randrange(len(texts))]

    if not lower:
        alphabet = uletters
    elif not upper:
        alphabet = lletters

    for i in range(length):
        # last half length will be filled with numbers
        if number and i >= (length / 2):
            mypw = mypw + _random_character(digit)
        else:
            mypw = mypw + _random_character(alphabet)
    return mypw

def get_rand_name():
    h = Haikunator()
    return h.haikunate()
