#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

inputs:
  tumor_bam: # should have an adjacent .bai file, e.g. sample.bam, sample.bai
    type: File
    secondaryFiles:
      - ^.bai
  conpair_normal_genotypes: # GATK .pileup files or Conpair likelihoods .pickle files for all the normals in the cohort
    type: File[]
  somalier_normal_genotypes:
    type: File[]
  conpair_markers_bed:
    type: File
  conpair_markers_txt:
    type: File
  somalier_sites:
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
  SubworkflowFeatureRequirement: {}

steps:
  conpair_workflow:
    run: workflow-conpair.cwl
    in:
      tumor_bam: tumor_bam
      normal_genotypes: conpair_normal_genotypes
      markers_bed: conpair_markers_bed
      markers_txt: conpair_markers_txt
      ref_fasta: ref_fasta
    out:
      [ concordance_tsv ]

  somalier_workflow:
    run: workflow-somalier.cwl
    in:
      tumor_bam: tumor_bam
      normal_genotypes: somalier_normal_genotypes
      sites: somalier_sites
      ref_fasta: ref_fasta
    out:
      [somalier_html, somalier_pairs_tsv, somalier_samples_tsv]

outputs:
  conpair_tsv:
    type: File
    outputSource: conpair_workflow/concordance_tsv
  somalier_html:
    type: File
    outputSource: somalier_workflow/somalier_html
  somalier_pairs_tsv:
    type: File
    outputSource: somalier_workflow/somalier_pairs_tsv
  somalier_samples_tsv:
    type: File
    outputSource: somalier_workflow/somalier_samples_tsv
