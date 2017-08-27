## @mainpage
# @author lukasl93
# @date Created on 28.03.2017\n
# Last edited on 09.05.2017
# [pgfplot]: http://ftp.uni-erlangen.de/ctan/graphics/pgf/contrib/pgfplots/doc/pgfplots.pdf "Latex pgfplot documentation"
# [scikit_tut]: http://scikit-rf.readthedocs.io/en/latest/tutorials/Introduction.html "scikit-rf Python 2 Package Introduction"
# [scikit_inst]: http://scikit-rf.readthedocs.io/en/latest/tutorials/Installation.html "scikit-rf Python 2 Package Installation"
# [din461]: https://de.wikipedia.org/wiki/DIN_461 "DIN 461"
#
# @section sec_intro Introduction
# The creation of uniform documentation is the main goal of this project.\n
# Therefore this project offers a tool
# to create [DIN 461][din461] conform plots
# in the format used by the [Latex pgfplot package][pgfplot].
#
#
# Theoretically all kinds of line data plots can be created by the
# #TikzExport::ClassTikzExport.
#
# The additional #TikzExport::ClassSpara2Tikz provides two functions to create
# S-Parameterplots from Touchstone files.\n
# For maximum flexibility the Scikit-RF package was used for the data import.\n
# Therefore also all the advanced functions of Scikit-RF like:
#  - deembedding
#  - network concatenation
#  - and much more
#
# are available.
# For detailed information see the [full documentation][scikit_tut]
#
#
# @section sec_req Requirements
# The code must be run with Python 2.7,
# because Scikit-RF is not compatible with 3.6.\n
# Scikit-RF must be installed like described [here][scikit_inst].
#
#
# @section sec_use Usage
# A minimal Example for the usage of #TikzExport::ClassTikzExport can be found
# in the file at the end of #TikzExport::ClassTikzExport.\n
# For #TikzExport::ClassSpara2Tikz the usage is shown in the Examples section.
#
# To use the test scripts from the Examples section,
# just copy your Touchstone files
# to 'touchstoneinput', then run the testscripts.\n
# The created files are located at 'LatexTest/tikz'
#
# Under 'LatexTest' a dummy document is located
# to compile all the created pictures,
# if you haven't changed the default directory settings of the test scripts.\n
# You have to compile the file with:\n
# pdflatex.exe -synctex=1 -interaction=nonstopmode -shell-escape Dummydokument_Tikzbilder.tex \n
# Under Linux just skip the .exe.
#
# @section sec_contact Contact the Author
# The author worked
# on his Masterthesis while creating this tool.\n
#
# Please contact through the issue board in Github.
# https://github.com/lukasl93/touchstone2tikz
#
#
## @example singletouchstone2tikz.py
# This script reads all the .s*p files in the touchstoneinput Directory
# and creates Matching, Coupling and Isolation plots or each of them.
# It is optimized for a three port coupler like a wilkinson.\n
# Adapt this script to your needs.
#
## @example comptouchstone2tikz.py
# This script reads all the .s*p files in the touchstoneinput Directory
# and creates one Matching, Coupling and Isolation plot comparing all of them.
# It is optimized for a three port coupler like a wilkinson.\n
# Adapt this script to your needs.
pass
