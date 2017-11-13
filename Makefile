LATEXFOLDER = LatexTest
TARGET = dummy
PYTHON = /usr/bin/python2
CURRDIR = $(shell pwd)
SRCTEX = $(shell find $(LATEXFOLDER)/ -name "*.tex")
SRCAUX = $(shell find $(LATEXFOLDER)/ -name "*.aux")
SRCPDF = $(shell find $(LATEXFOLDER)/tikzpictures -name "*.pdf")
SRCTIKZ = $(shell find $(LATEXFOLDER)/tikz -name "*.tikz")
SRCTSTN = $(shell find $(CURRDIR)/touchstoneinput -name "*.s[1-9]p")	# works only up 9 Ports
# SRCPIC = $(shell find $(LATEXFOLDER)/pictures -name "*.jpg" -or -name "*.png")

all:
	make exampletikz
	make tsn2tikz
	make $(TARGET).pdf
	#make graphs	
	make $(TARGET).pdf
	make $(TARGET).pdf
	xdg-open $(CURRDIR)/$(LATEXFOLDER)/dummy.pdf &

help:
	@echo "Description:"
	@echo "'make' will compile full sourcechain for the output PDF"
	@echo "'make tsn2tikz' will create the Tikz files from Touchstone"

$(TARGET).pdf: $(SRCTEX) $(SRCTIKZ) $(SRCPDF) $(SRCPIC) $(SRCAUX)
	cd $(CURRDIR)/$(LATEXFOLDER) && pdflatex -shell-escape -interaction=nonstopmode -synctex=1 $(TARGET).tex


# Build example Tikz file from makeprojecttikz.py
exampletikz:
	$(PYTHON) -u $(CURRDIR)/src/basefiles/TikzExport.py


# Build all Tikz files according to makeprojecttikz.py
tsn2tikz: $(SRCTSTN)
	$(PYTHON) -u $(CURRDIR)/src/makeprojecttikz.py $(CURRDIR)/touchstoneinput $(CURRDIR)/LatexTest/tikz

# only with package option
# \tikzexternalize[prefix=tikzpictures/,mode=list and make]
# on linux machines
graphs: $(SRCTIKZ)
	cd $(CURRDIR)/$(LATEXFOLDER) && make -j 8 -f $(TARGET).makefile

.PHONY: clean tikzclear warn
clean: 
	rm -f *.toc *.out *.aux *.log *.mtc* *.maf *~ *.backup *.lof *.blg *.auxlock *.fdb_latexmk *.synctex.gz *.bbl *.makefile *.fls *.figlist

tikzclear:
	cd $(CURRDIR)/$(LATEXFOLDER)/tikz && rm *.tikz
	cd $(CURRDIR)/$(LATEXFOLDER)/tikzpictures && rm *.log *.dpth *.md5 *.pdf *.dep

warn:
	grep "LaTeX Warning" $(CURRDIR)/$(LATEXFOLDER)/*.log
