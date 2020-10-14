cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['somalier', 'relate']

requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: brentp/somalier:v0.2.12

inputs:
  tumor_genotype_file:
    type: File
  cohort_genotype_dir:
    type: Directory

arguments:
  - valueFrom: $(inputs.tumor_genotype_file)
  - valueFrom: ${ return inputs.cohort_genotype_dir.path + '/*' } # This is supposed to be a quoted glob string e.g. 'normals/*', to avoid glob expansion in the shell and let Somalier expand the glob internally to avoid kernel command length limits, but having trouble getting quotes to come out right, seems to get extra quotes if any are applied, not sure if glob is actually being passed to Somalier as a literal string or if the glob is still getting expanded on the shell

outputs:
  html:
    type: File
    outputBinding:
      glob: "somalier.html"
  pairs_tsv:
    type: File
    outputBinding:
      glob: "somalier.pairs.tsv"
  samples_tsv:
    type: File
    outputBinding:
      glob: "somalier.samples.tsv"
