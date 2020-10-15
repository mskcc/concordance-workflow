cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['run.py', 'concordance']
# run.py concordance \
# "${tumor_pileup}" "${normals_dir}/*" \
# --markers "${markers}" \ # params.conpair_markers_txt
# --output-file "${output_file}" \
# --threads "${task.cpus}" \

requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: mskcc/conpair:dev
  ResourceRequirement:
    coresMin: 8

inputs:
  tumor_file: # GATK .pileup or likelihoods .pickle
    type: File
  cohort_dir: # dir of GATK .pileup or likelihoods .pickle files
    type: Directory
  markers:  # conpair_markers_txt
    type: File
  threads:
    type: ['null', string]
    default: '8'

arguments:
  - valueFrom: $(inputs.tumor_file)
  - valueFrom: ${ return inputs.cohort_dir.path + '/*' } # This is supposed to be a quoted glob string e.g. 'normals/*', to avoid glob expansion in the shell and let Conpair run.py expand the glob internally to avoid kernel command length limits, but having trouble getting quotes to come out right, seems to get extra quotes if any are applied, not sure if glob is actually being passed as a literal string or if the glob is still getting expanded on the shell
  - valueFrom: $(inputs.markers)
    prefix: "--markers"
    position: 3
  - valueFrom: $(inputs.threads)
    prefix: "--threads"
    position: 4
  - valueFrom: ${ return inputs.tumor_file.basename + '.concordance.tsv' }
    prefix: "--output-file"
    position: 5

outputs:
  concordance_tsv:
    type: File
    outputBinding:
      glob: ${ return inputs.tumor_file.basename + '.concordance.tsv' }
