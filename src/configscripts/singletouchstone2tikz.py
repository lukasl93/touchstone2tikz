#!/usr/bin/python2
# -*- coding: utf-8

## @package singletouchstone2tikz
#
# Script to export Matching, Coupling and Isolation plots
# for every .s*p files in #sourcedir.
#
# Resulting .tikz files are exported to #resultdir.
#
# Based on scikit-rf (skrf) http://scikit-rf-web.readthedocs.io/ \n
# Documentation at http://scikit-rf.readthedocs.io/en/latest/index.html
#
# @date Created on 27.04.2017\n
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
from ClassDataStructs import ClassRequirements
from tikzhelpers import createImportFile, clearImportFile


## Create Tikz files
# @param sourcedir Search for Touchstone files in this directory
# @param resultdir Export resulting Tikz files to this directory
def touchstone2tikz(sourcedir, resultdir):
    # Define all Requirements for the Project
    requirement11 = ClassRequirements(r'Requirements $S_{11}$', 'max', '')
    requirement11.set_data(0.4, 6, -20)

    requirement22 = ClassRequirements(r'Requirements $S_{22}$ and $S_{33}$',
                                      'max', '', '0,0,0')
    requirement22.set_data(0.4, 6, -15)

    requirement32 = ClassRequirements(r'Requirements Isolation ($S_{32}$)',
                                      'max', '')
    requirement32.set_data(0.4, 6, -20)

    requirement21 = ClassRequirements(
        r'Requirements Coupling ($S_{21}$ and $S_{31}$)',
        'is', '', reqscale=0.2)
    requirement21.set_data(0.4, 6, -6)

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
            netw, 'GHz', [(1, 1), (2, 2), (3, 3)],
            [' - Matching Port 1', ' - Matching Port 2', ' - Matching Port 3'],
            requirements=[requirement11, requirement22],
            filename=os.path.join(resultdir, netw.name + '_ANP.tikz'))
        teximport += importtemplate.substitute({
            'tikzfilename': netw.name + '_ANP',
            'desc': netw.name.replace('_', ' ') + ' - Matching'})
        spara_db_2tikz(
            netw, 'GHz', [(2, 1), (3, 1)],
            [' - Coupling Port 1 to 2', ' - Coupling Port 1 to 3'],
            requirements=requirement21,
            filename=os.path.join(resultdir, netw.name + '_KOP.tikz'))
        teximport += importtemplate.substitute({
            'tikzfilename': netw.name + '_KOP',
            'desc': netw.name.replace('_', ' ') + ' - Coupling'})
        spara_db_2tikz(
            netw, 'GHz', [(3, 2)], [' - Isolation between Port 2 and 3'],
            requirements=requirement32,
            filename=os.path.join(resultdir, netw.name + '_ISO.tikz'))
        teximport += importtemplate.substitute({
            'tikzfilename': netw.name + '_ISO',
            'desc': netw.name.replace('_', ' ') + ' - Isolation'})
        teximport += '\n'

    createImportFile(os.path.join(resultdir, 'importallpictures.tex'),
                     teximport)
    print('Done!')


## Class for multi threading support
class threadtouchstone2tikz(threading.Thread):
    def __init__(self, sourcedir, resultdir):
        threading.Thread.__init__(self)
        self.sourcedir = sourcedir
        self.resultdir = resultdir

    def run(self):
        touchstone2tikz(self.sourcedir, self.resultdir)


## @cond Prevents doxygen from scanning the following
if __name__ == '__main__':
    # Source directory with .s*p files
    sourcedir = os.path.join(os.path.dirname(__file__), '..',
                             '..', 'touchstoneinput', 'singlepic')

    # Result directory for tikz files
    resultdir = os.path.join(os.path.dirname(__file__),
                             '..', '..', 'LatexTest', 'tikz')

    # Support command line arguments for input and output directory
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        sourcedir = sys.argv[1]
        resultdir = sys.argv[2]
    else:
        print("Usage: python2 singletouchstone2tikz.py <sourcedir> <resultdir>")

    clearImportFile(os.path.join(resultdir, 'importallpictures.tex'))

    # Call the main function provided by this package
    touchstone2tikz(sourcedir, resultdir)

## @endcond Prevents doxygen from scanning the code above
