#!/usr/bin/python2
# -*- coding: utf-8 -*-

## @package tikzhelpers
# Provides a couple of helper functions
#
# @date Created on 21.05.2017\n
#      Last edited 27.08.2017 by lukasl93
#
# @author lukasl93

import os


## Dictionary to calculate data in the given unit from Hz
def get_frequnits():
    return {
        'Hz': 1,
        'kHz': 1e3,
        'MHz': 1e6,
        'GHz': 1e9,
        'THz': 1e12
    }


## calculate the mean value of the numbers list
# @param numbers Number list
# @return mean value of numbers
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


## Create a pathstring from ClassData2D list
# @param data ClassData2D list
# @return Tikz pathstring for Requirement type indicators
def get_path_data_string(data):
    returnstring = '(' + str(data[0].xvalue) + ',' + str(data[0].yvalue) + ')'
    for i in range(1, len(data), 1):
        returnstring += \
            '--(' + str(data[i].xvalue) + ',' + str(data[i].yvalue) + ')'
    return returnstring


def createImportFile(filename, content):
    if not os.path.isabs(filename):
        importfile = open(
            os.path.join(os.path.dirname(__file__), filename), 'a')
    elif os.path.isabs(filename):
        if os.path.isdir(os.path.dirname(filename)):
            importfile = open(filename, 'a')
        else:
            raise IOError('Path not existent. Please create the Folders and run again!\nPath: ' + filename)
    else:
        raise ValueError('Variable filename contains no valid type, value or whatever!')
    importfile.write(content)
    importfile.close()


def clearImportFile(filename):
    if not os.path.isabs(filename):
        importfile = open(
            os.path.join(os.path.dirname(__file__), filename), 'w')
    elif os.path.isabs(filename):
        if os.path.isdir(os.path.dirname(filename)):
            importfile = open(filename, 'w')
        else:
            raise IOError('Path not existent. Please create the Folders and run again!\nPath: ' + filename)
    else:
        raise ValueError('Variable filename contains no valid type, value or whatever!')
    importfile.write('')
    importfile.close()
