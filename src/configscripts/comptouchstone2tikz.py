#!/usr/bin/python2
# -*- coding: utf-8

## @package comptouchstone2tikz
#
# Script to export Matching, Coupling and Isolation comparison plots
# with curves from all .s*p files in #sourcedir.
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
from glob import glob
from string import Template
import skrf as rf
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basefiles'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'designscripts'))

from comp_spara_db_2tikz import comp_spara_db_2tikz
from ClassDataStructs import ClassRequirements
from tikzhelpers import createImportFile, clearImportFile


## Function to create comparison tikz plots
# @param sourcedir Directory with .s*p Touchstone files to be compared
# @param resultdir Directory to place the resulting .tikz files in
# @param compname Label of the comparison, is used in the tikzfile naming
def comparisons2tikz(sourcedir, resultdir, compname=''):

    ## Define all Requirements for the Project
    requirement11 = ClassRequirements(r'Requirements Matching ($S_{11}$)',
                                      'max', '')
    requirement11.set_data(0.4, 6, -20)

    requirement22 = ClassRequirements(r'Requirements Matching ($S_{22}$)',
                                      'max', '')
    requirement22.set_data(0.4, 6, -15)

    requirement33 = ClassRequirements(r'Requirements Matching ($S_{33}$)',
                                      'max', '')
    requirement33.set_data(0.4, 6, -15)

    requirement32 = ClassRequirements(r'Requirements Isolation ($S_{32}$)',
                                      'max', '')
    requirement32.set_data(0.4, 6, -20)

    requirement21 = ClassRequirements(r'Requirements Coupling ($S_{21}$)',
                                      'is', '', reqscale=0.2)
    requirement21.set_data(0.4, 6, -6)

    requirement31 = ClassRequirements(r'Requirements Coupling ($S_{31}$)',
                                      'is', '', reqscale=0.2)
    requirement31.set_data(0.4, 6, -6)


    # Create a tex file to plot all created pictures when included
    importtemplate = Template(r'\instikz{$tikzfilename}{$desc}' + '\n')
    teximport = ''

    touchstone_list = glob(os.path.join(sourcedir, "*.s*p"))

    if not touchstone_list:
        print('No touchstone files foand in ' + sourcedir + '! Skipping...')
        return

    # Full list of networks
    networks = []
    networkdesc = []

    for touchstone in touchstone_list:
        # read Touchstone files
        netw = rf.Network(touchstone)
        print('Now reading: ' + netw.name + ' ...')
        networks.append(netw)
        networkdesc.append(' - ' + netw.name.replace('_', ' '))

    # export tikz files
    print('Now creating Tikzplot for Matching S11 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (1, 1), networkdesc, requirements=requirement11,
        filename=os.path.join(resultdir, compname + 'Comparison_ANP11.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_ANP11',
        'desc': 'Comparison of the Matching at Port 1 ($S_{11}$)'})

    print('Now creating Tikzplot for Matching S22 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (2, 2), networkdesc, requirements=requirement22,
        filename=os.path.join(resultdir, compname + 'Comparison_ANP22.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_ANP22',
        'desc': 'Comparison of the Matching at Port 2 ($S_{22}$)'})

    print('Now creating Tikzplot for Matching S33 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (3, 3), networkdesc, requirements=requirement33,
        filename=os.path.join(resultdir, compname + 'Comparison_ANP33.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_ANP33',
        'desc': 'Comparison of the Matching at Port 3 ($S_{33}$)'})

    print('Now creating Tikzplot for Coupling S21 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (2, 1), networkdesc, requirements=requirement21,
        filename=os.path.join(resultdir, compname + 'Comparison_KOP21.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_KOP21',
        'desc': 'Comparison of the Coupling between Port 1 and 2 ($S_{21}$)'})

    print('Now creating Tikzplot for Coupling S31 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (3, 1), networkdesc, requirements=requirement31,
        filename=os.path.join(resultdir, compname + 'Comparison_KOP31.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_KOP31',
        'desc': 'Comparison of the Coupling between Port 1 and 3 ($S_{31}$)'})

    print('Now creating Tikzplot for Isolation S32 ...')
    comp_spara_db_2tikz(
        networks, 'GHz', (3, 2), networkdesc, requirements=requirement32,
        filename=os.path.join(resultdir, compname + 'Comparison_ISO32.tikz'))
    teximport += importtemplate.substitute({
        'tikzfilename': compname + 'Comparison_ISO32',
        'desc': 'Comparison of the Isolation between Port 2 and 3 ($S_{32}$)'})

    teximport += '\n'

    createImportFile(os.path.join(resultdir, 'importcomppictures.tex'),
                     teximport)
    print('Done!')


## @cond Prevents doxygen from scanning the following
if __name__ == '__main__':
    # Source directory with .s*p files
    sourcedir = os.path.join(os.path.dirname(__file__), '..',
                             '..', 'touchstoneinput', 'singlecomppic')

    # Result directory for tikz files
    resultdir = os.path.join(os.path.dirname(__file__),
                             '..', '..', 'LatexTest', 'tikz')

    compname = 'Test'

    # Support command line arguments for input and output directory
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        sourcedir = sys.argv[1]
        resultdir = sys.argv[2]
    elif len(sys.argv) == 4:
        sourcedir = sys.argv[1]
        resultdir = sys.argv[2]
        compname = sys.argv[3]
    else:
        print("Usage: python2 comptouchstone2tikz.py <sourcedir> <resultdir> (<compname>)")

    clearImportFile(os.path.join(resultdir, 'importcomppictures.tex'))

    # Call the main function provided by this package
    comparisons2tikz(sourcedir, resultdir, compname)
## @endcond Prevents doxygen from scanning the code above