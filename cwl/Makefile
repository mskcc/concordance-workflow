export SHELL:=/bin/bash
.ONESHELL:
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit
# export PATH:=$(CURDIR)/bin:$(PATH)
UNAME:=$(shell uname)



SOMALIER_SIF:=somalier_v0.2.12.sif
$(SOMALIER_SIF):
	unset SINGULARITY_CACHEDIR && \
	module load singularity/3.3.0 && \
	singularity pull --force --name "$(SINGULARITY_SIF)" docker://brentp/somalier:v0.2.12
singularity-pull-somalier: $(SOMALIER_SIF)

# NOTE: you cannot use a filename with a ':' as a Makefile target
SINGULARITY_SIF:=mskcc_conpair:dev.sif
singularity-pull-Conpair:
	if [ ! -e "$(SINGULARITY_SIF)" ]; then
	unset SINGULARITY_CACHEDIR && \
	module load singularity/3.3.0 && \
	singularity pull --force --name "$(SINGULARITY_SIF)" docker://mskcc/conpair:dev
	fi

GATK_SIF:=gatk3_3.8-1.sif
$(GATK_SIF):
	unset SINGULARITY_CACHEDIR && \
	module load singularity/3.3.0 && \
	singularity pull --name "$(GATK_SIF)" --force docker://broadinstitute/gatk3:3.8-1
singularity-pull-GATK: $(GATK_SIF)

install: singularity-pull-somalier singularity-pull-Conpair singularity-pull-GATK

bash:
	module load singularity/3.3.0
	bash

test:
	module load singularity/3.3.0 && \
	module load python/3.7.1 && \
	module load cwl/cwltool && \
	for i in tests/test_*.py; do echo $$i; $$i; done
