#!/usr/bin/python2
# -*- coding: utf-8 -*-

## @package completetouchstone2tikz
#
# Script to export complete S-Parameter plot
# for every .s*p files in #sourcedir.
#
# Resulting .tikz files are exported to #resultdir.
#
# Based on scikit-rf (skrf) http://scikit-rf-web.readthedocs.io/ \n
# Documentation at http://scikit-rf.readthedocs.io/en/latest/index.html
#
# @date Created on 19.05.2017\n
# Last edited on 27.08.2017
#
# @author lukasl93

import os
import sys
import threading
from glob import glob
from string import Template
import skrf as rf
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basefiles'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'designscripts'))

from spara_db_2tikz import spara_db_2tikz
from tikzhelpers import createImportFile, clearImportFile


def fulltouchstone2tikz(sourcedir, resultdir):
    # Create a tex file to plot all created pictures when included
    importtemplate = Template(r'\instikz{$tikzfilename}{$desc}' + '\n')
    teximport = ''

    touchstone_list = glob(os.path.join(sourcedir, "*.s*p"))

    if not touchstone_list:
        print('No touchstone files found in ' + sourcedir + '! Skipping...')
        return

    for touchstone in touchstone_list:
        # read Touchstone files
        netw = rf.Network(touchstone)
        print('Now processing: ' + netw.name + ' ...')

        # export tikz files
        spara_db_2tikz(
            netw, 'GHz',
            filename=os.path.join(resultdir, netw.name + '_ALL.tikz'))
        teximport += importtemplate.substitute({
            'tikzfilename': netw.name + '_ALL',
            'desc': netw.name.replace('_', ' ') + ' - All S-Parameters'})
        teximport += '\n'

    createImportFile(os.path.join(resultdir, 'completepictures.tex'), teximport)
    print('Done!')


## Class for multi threading support
class threadfulltouchstone2tikz(threading.Thread):
    def __init__(self, sourcedir, resultdir):
        threading.Thread.__init__(self)
        self.sourcedir = sourcedir
        self.resultdir = resultdir

    def run(self):
        fulltouchstone2tikz(self.sourcedir, self.resultdir)


## @cond Prevents doxygen from scanning the following
if __name__ == '__main__':
    ## Source directory with .s*p files
    sourcedir = os.path.join(os.path.dirname(__file__), '..',
                             '..', 'touchstoneinput', 'fullpic')

    ## Result directory for tikz files
    resultdir = os.path.join(os.path.dirname(__file__),
                             '..', '..', 'LatexTest', 'tikz')

    # Support command line arguments for input and output directory
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        sourcedir = sys.argv[1]
        resultdir = sys.argv[2]
    else:
        print("Usage: python2 completetouchstone2tikz.py <sourcedir> <resultdir>")

    clearImportFile(os.path.join(resultdir, 'completepictures.tex'))

    # Call the main function provided by this package
    fulltouchstone2tikz(sourcedir, resultdir)

## @endcond Prevents doxygen from scanning the code above
