SHELL:=/bin/bash
.ONESHELL:
UNAME:=$(shell uname)
PATH:=$(CURDIR)/conda/bin:$(PATH)

ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-py39_4.12.0-MacOSX-x86_64.sh
# CONDASH:=Miniconda3-py39_4.12.0-MacOSX-arm64.sh
endif

ifeq ($(UNAME), Linux)
# CONDASH:=Miniconda3-py37_4.12.0-Linux-x86_64.sh
CONDASH:=Miniconda3-py39_4.12.0-Linux-x86_64.sh
endif

CONDAURL:=https://repo.anaconda.com/miniconda/$(CONDASH)

unexport PYTHONPATH
unexport PYTHONHOME
conda:
	@echo ">>> Setting up conda..."
	wget "$(CONDAURL)" && \
	bash "$(CONDASH)" -b -p conda && \
	rm -f "$(CONDASH)"


# - https://www.nextflow.io/docs/latest/dsl2.html
# - https://nf-co.re/ ; https://nf-co.re/docs/usage/introduction

# https://nf-co.re/tools/#installation
install: conda
	source conda/bin/activate && \
	conda create --name nf-core -y -c bioconda -c conda-forge nf-core=2.5.1 nextflow=22.04.5 && \
	conda activate nf-core && \
	which nf-core && which nextflow && \
	printf ">>> activate with:\nsource conda/bin/activate\nconda activate nf-core\n"
# conda env export --from-history > env.yml
# conda deactivate


# https://nf-co.re/tools/#creating-a-new-pipeline
# $ nf-core create --name concordance -d "concordance workflow" -a "Stephen Kelly"