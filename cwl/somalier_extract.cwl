cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['somalier', 'extract']
# "${params.somalier_bin}" extract \
# --sites "${sites}" \
# -f "${params.ref_fasta}" \
# "${bam}"

requirements:
  DockerRequirement:
    dockerPull: brentp/somalier:v0.2.12

inputs:
  sites: # SOMALIER_SITES
    type: File
    inputBinding:
      position: 1
      prefix: '--sites'
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
    inputBinding:
      position: 2
      prefix: '-f'
  bam_file:
    type: File
    secondaryFiles:
      - ^.bai
    inputBinding:
      position: 3

outputs:
  output_file:
    type: File
    outputBinding:
      glob: "*.somalier" # NOTE: output filename uses the RG read group labels from the .bam file!
