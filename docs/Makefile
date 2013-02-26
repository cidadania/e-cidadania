# Makefile for Sphinx documentation
#

PYTHON = python

.PHONY: all clean html latex latexpdf

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4paper
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees/$(LANG) $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

SPHINX_DEPENDENCIES = en/Makefile

#%/Makefile : en/Makefile
#   $(PYTHON) -c "import shutil; shutil.copyfile('$<, '$@')"

# Take in mind that the english is the last to build. This is for readthedocs.org
# to get the english docs instead of spanish or galician.

help:
	@echo "Please use \`make <target>' where <target> is one of the supported formats by e-cidadania:"
	@echo   
	@echo "  html         Make the HTML version of the documentation"
	@echo "  latex        Make the LaTeX version of the documentation"
	@echo "  latexpdf     Create the PDF version of the documentation using pdflatex"
	@echo
	@echo "This Makefile will generate the documentation for the three official languages of e-cidadania: Spanish, English and Galician."
	@echo "If you want to build just one of them please use the Makefile inside the language directory."
	@echo

html: $(SPHINX_DEPENDENCIES)
	cd en && make html LANG=en
	cd es && make html LANG=es
	cd gl && make html LANG=gl
	
latex: $(SPHINX_DEPENDENCIES)
	cd gl && make latex LANG=gl
	cd es && make latex LANG=es
	cd en && make latex LANG=en

latexpdf: $(SPHINX_DEPENDENCIES)
	cd es && make latexpdf LANG=es
	cd en && make latexpdf LANG=en
	cd gl && make latexpdf LANG=gl

clean:
	rm -rf $(BUILDDIR) 
	@echo "The build directory has been removed."
