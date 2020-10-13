cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['java', '-Xmx12g', '-jar', '/usr/GenomeAnalysisTK.jar', '-T', 'Pileup', '-rf', 'DuplicateRead', '-rf', 'BadCigar', '--filter_reads_with_N_cigar', '--filter_mismatching_base_and_quals', '-verbose']
# /usr/GenomeAnalysisTK.jar # <- this is the location inside the offical Docker container

requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk3:3.8-1

inputs:
  bam_file:
    type: File
    secondaryFiles:
      - ^.bai
    inputBinding:
      position: 1
      prefix: '-I'
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
      prefix: '-R'
  regions_bed: # conpair_markers_bed
    type: File
    inputBinding:
      position: 3
      prefix: '-L'
  output_filename:
    type: string
    inputBinding:
      position: 4
      prefix: '-o'

outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)

# // errorStrategy 'ignore' // see known errors listed below
# //  ##### ERROR MESSAGE: SAM/BAM file SAMFileReader{....bam} is malformed: read starts with deletion. Cigar: 1D74M. Although the SAM spec technically permits such reads, this is often indicative of malformed files. If you are sure you want to use this file, re-run your analysis with the extra option: -rf BadCigar
# // ##### ERROR MESSAGE: SAM/BAM file SAMFileReader{...duplex.bam} appears to be using the wrong encoding for quality scores: we encountered an extremely high quality score of 87; please see the GATK --help documentation for options related to this error
