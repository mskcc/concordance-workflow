#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  tumor_bam: # should have an adjacent .bai file, e.g. sample.bam, sample.bai
    type: File
    secondaryFiles:
      - ^.bai
  normal_genotypes: # somalier extract .somalier files for all normals in the cohort
    type: File[]
  sites:
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
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}

steps:
  extract_tumor_genotype:
    run: somalier_extract.cwl
    in:
      bam_file: tumor_bam
      ref_fasta: ref_fasta
      sites: sites
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

  cohort_concordance:
    run: somalier_concordance.cwl
    in:
      tumor_genotype_file: extract_tumor_genotype/output_file
      cohort_genotype_dir: make_cohort_dir/directory
    out:
      [ html, pairs_tsv, samples_tsv]


outputs:
  somalier_html:
    type: File
    outputSource: cohort_concordance/html
  somalier_pairs_tsv:
    type: File
    outputSource: cohort_concordance/pairs_tsv
  somalier_samples_tsv:
    type: File
    outputSource: cohort_concordance/samples_tsv
