# touchstone2tikz
Python Framework for Latex-Tikz-File-Creation from Touchstone Files

## Overview

This Github repository contains Python scripts to read Touchstone files and convert them to Latex compileable Tikz files.

The touchstone reading is done via <a href=http://scikit-rf.readthedocs.io/en/latest/index.html>scikit-rf</a>, because it provides useful additional functionallity, for example deembedding or concatenation of networks.

An example Latex document is provided to compile the created Tikz-Files.

## File organisation

The project is hierachically structured in the folder:
<pre>
*touchstone2tikz*
 |
 |- *Makefile*	Type make to create all Tikzpictures and create a PDF-file
 |
 |- *touchstoneinput*	Location for the source Touchstone files
 |	|- *fullpic*	Files in this folder are converted to Tikzplots with full S-Matrix
 |	|- *singlepic* Each file is processed itself into multiple Tikzplots
 |	|- *singlecomppic*	Comparisons are named like the Subfolders in the Plot
 |	|	|- *comp1*	Comparison plot of one S-Parameter over all contained Files
 |	|	|- *comp2*	Comparison plot of one S-Parameter over all contained Files
 |	|	|- *compX*	You can have as many comparisons going as you create subfolders
 |	|- *multcomppic*	Comparisons are named like the Subfolders in the Plot
 |		|- *comp1*	Comparison plot of multiple S-Parameters over all contained Files
 |		|- *comp2*	Comparison plot of multiple S-Parameters over all contained Files
 |		|- *compX*	You can have as many comparisons going as you create subfolders
 |
 |- *src*	Contains the Python scripts
 |	|- *makeprojecttikz.py*	Main Python script to call, don't edit
 |	|- *README.py*	Intro for Doxygen Documentation
 |	|- *basefiles*	Main files for the Tikz generation from arbitrary Data
 |	|	|- *TikzExport.py*	Definitions of all Templates and of Class for Tikz file creation
 |	|	|- *ClassDataStructs.py*	Provides Classes for Data handling
 |	|	|- *tikzhelpers.py*	Provides helperfunctions
 |	|- *designscripts*	Scripts to control appearance of curves, legend...
 |	|	|- *spara_db_2tikz.py*	fullpic and singlepic design
 |	|	|- *comp_spara_db_2tikz.py*	singlecomppic design
 |	|	|- *comp_mult_spara_db_2tikz.py*	multcomppic design
 |	|- *configscripts*	Scripts with Requirement and Plot creation control, adjust to your needs
 |	|	|- *completetouchstone2tikz.py*	Create S-Matrix plot from files in fullpic
 |	|	|- *singletouchstone2tikz.py*	Create single S-Param plots from files in singlepic
 |	|	|- *comptouchstone2tikz.py*	Create comparison plot with single S-Param from files in subfolders of singlecomppic
 |	|	|- *multcomptouchstone2tikz.py*	Create comparison plot with multiple S-Param from files in subfolders of multcomppic
 |
 |- *LatexTest*	Dummy Latex document to compile the created Tikz plots
 	|- *dummy.tex*	Latex document source
 	|- *dummy.pdf*	Latex output pdf, created by running make
 	|- *tikz*	Folder for Tikz files and files to include those into the document
 	|- *tikzpictures*	Folder for PDFs created by tikzexternalize
</pre>

## Calling sequence

<pre>
Start -> Makefile 5- pdflatex
			0|
	makeprojecttikz.py
			|
	-----------------------------------------------------------------------------------------
	1|								2|							3|							4|
completetouchstone2tikz.py 	singletouchstone2tikz.py 	comptouchstone2tikz.py 	multcomptouchstone2tikz.py
	|								|							|							|
	---------------------------------							|							|
					|											|							|
				spara_db_2tikz.py 					comp_spara_db_2tikz.py 			comp_mult_spara_db_2tikz.py
					|											|							|
					-------------------------------------------------------------------------
													|
											TikzExport.py
</pre>

## Usage

Currently the configscripts are optimized for a three port like a wilkinison divider.
So initially you have to change the requirements and S-Parameters to be plotted in the configscripts.

Only completetouchstone2tikz.py is configured completely general and can be used out of the box for every Touchstonefile.

When you're done adapting the scripts to your needs, just sort your touchstone files into the touchstoneinput folder and type make in a terminal window in the projectfolder.

## Improve this Framework

If you have suggestions or improvements for the code, feel free to open an incident, or direktly fork the repository and create a pull request. Every constructive feedback is greatly appreciated!
