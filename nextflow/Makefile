export SHELL:=/bin/bash
.ONESHELL:
export PATH:=$(CURDIR):$(PATH)
export NXF_VER:=20.07.1
./nextflow:
	if module avail java/jdk1.8.0_202 1&>/dev/null; then module load java/jdk1.8.0_202; fi
	curl -fsSL get.nextflow.io | bash
install: ./nextflow

run:
	if module avail java/jdk1.8.0_202 1&>/dev/null; then module load java/jdk1.8.0_202; fi
	./nextflow run tumor-concordance.nf --conpair_cohort normals_conpair --somalier_cohort normals_somalier --bam sample.bam

run-batch:
	if module avail java/jdk1.8.0_202 1&>/dev/null; then module load java/jdk1.8.0_202; fi
	./nextflow run -resume batch-concordance.nf --conpair_cohort normals_conpair --somalier_cohort normals_somalier --tumor_list tumor_list.txt

bash:
	if module avail java/jdk1.8.0_202 1&>/dev/null; then module load java/jdk1.8.0_202; fi
	bash

clean:
	rm -f .nextflow.log.*
	rm -f *.html.*
	rm -f trace.txt.*

clean-all: clean
	rm -f .nextflow.log*
	rm -f *.html
	rm -f trace.txt*
	rm -rf work
	rm -rf output
