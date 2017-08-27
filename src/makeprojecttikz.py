#!/usr/bin/python2
# -*- coding: utf-8

## @package makeprojecttikz
#
# Script to (re)create all tikz plots
# from the .s*p files in #sourcedir
# and comparison plots with all .s*p files
# in subfolders of #sourcedir.
#
# Resulting .tikz files are exported to #resultdir.
#
# @date Created on 27.04.2017\n
# Last edited on 27.08.2017
#
# @author lukasl93

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'basefiles'))
from tikzhelpers import clearImportFile
sys.path.append(os.path.join(os.path.dirname(__file__), 'configscripts'))
from singletouchstone2tikz import touchstone2tikz
from completetouchstone2tikz import fulltouchstone2tikz
from comptouchstone2tikz import comparisons2tikz
from multcomptouchstone2tikz import multcomparisons2tikz


# Source directory with .s*p files
sourcedir = os.path.join(os.path.dirname(__file__),
                         '..', 'touchstoneinput')

# Result directory for tikz files
resultdir = os.path.join(os.path.dirname(__file__),
                         '..', 'LatexTest', 'tikz')

# Support command line arguments for input and output directory
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 3:
    sourcedir = sys.argv[1]
    resultdir = sys.argv[2]
else:
    print("Usage: python2 makeprojectikz.py <sourcedir> <resultdir>")

singlesubdirs = [
    o for o in os.listdir(os.path.join(sourcedir, 'singlecomppic'))
    if os.path.isdir(os.path.join(sourcedir, 'singlecomppic', o))
]

multsubdirs = [
    o for o in os.listdir(os.path.join(sourcedir, 'multcomppic'))
    if os.path.isdir(os.path.join(sourcedir, 'multcomppic', o))
]

clearImportFile(os.path.join(resultdir, 'completepictures.tex'))
clearImportFile(os.path.join(resultdir, 'importallpictures.tex'))
clearImportFile(os.path.join(resultdir, 'importcomppictures.tex'))
clearImportFile(os.path.join(resultdir, 'importmultcomppictures.tex'))

# Create Tikz plots containing full S-Matrix
fulltouchstone2tikz(os.path.join(sourcedir, 'fullpic'), resultdir)

# Create Tikz plots based on one Touchstone file
touchstone2tikz(os.path.join(sourcedir, 'singlepic'), resultdir)

# Create Tikz plots based on one Touchstone file
touchstone2tikz(os.path.join(sourcedir, 'singlepic'), resultdir)

# Create Tikz plots containing comparisions of multiple
# Touchstone files
for d in singlesubdirs:
    # Call the main function provided by this package
    comparisons2tikz(os.path.join(sourcedir, 'singlecomppic', d),
                     resultdir, d)

# Create Tikz plots containing comparisions of multiple
# Touchstone files and multiple S-Paramesters
for d in multsubdirs:
    # Call the main function provided by this package
    multcomparisons2tikz(os.path.join(sourcedir, 'multcomppic', d),
                         resultdir, d)
