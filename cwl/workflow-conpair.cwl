#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

inputs:
  tumor_bam: # should have an adjacent .bai file, e.g. sample.bam, sample.bai
    type: File
    secondaryFiles:
      - ^.bai
  normal_genotypes: # GATK .pileup files or Conpair likelihoods .pickle files for all the normals in the cohort
    type: File[]
  markers_bed:
    type: File
  markers_txt:
    type: File
  ref_fasta:
    type: File
    secondaryFiles:
      - .amb
      - .ann
      - .bwt
      - .pac
      - .sa
      - .fai
      - ^.dict

requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}

steps:
  pileup:
    run: gatk_pileup.cwl
    in:
      bam_file: tumor_bam
      ref_fasta: ref_fasta
      regions_bed: markers_bed
      output_filename:
        valueFrom: ${ return inputs.bam_file.basename.replace(".bam", ".pileup") }
    out:
      [ output_file ]

  likelihoods:
    run: conpair_likelihoods.cwl
    in:
      pileup: pileup/output_file
      markers: markers_txt
    out:
      [ output_file ]

  make_cohort_dir:
    run: put_in_dir.cwl
    in:
      files: normal_genotypes
      output_directory_name:
        valueFrom: ${ return "normals"; }
    out:
      [ directory ]

  concordance:
    run: conpair_concordance.cwl
    in:
      tumor_file: likelihoods/output_file
      cohort_dir: make_cohort_dir/directory
      markers: markers_txt
    out:
      [ concordance_tsv ]

outputs:
  concordance_tsv:
    type: File
    outputSource: concordance/concordance_tsv
