cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['make_genotype_likelihoods.py']

requirements:
  # InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: mskcc/conpair:dev

inputs:
  pileup:
    type: File
    inputBinding:
      position: 1
      prefix: '--pileup'
  markers: # conpair_markers_txt
    type: File
    inputBinding:
      position: 2
      prefix: '--markers'

# outputs: []

outputs:
  output_file:
    type: File
    outputBinding:
      glob:
        valueFrom: ${ return inputs.pileup.basename.replace(".pileup", ".pickle") }
#       outputEval: ${ path = require('path'); filename = path.parse(inputs.pileup).name; return filename }
        # valueFrom: ${ path = require('path'); filename = path.parse(inputs.pileup).name; return filename }
      # glob: $(inputs.pileup).pickle
      # const path = require('path');
