// workflow for retrieving the DMP cohort .bam files and pre-processing them
// needs to run as user voyager; make sure to chmod -R g+rw . the entire pwd
nextflow.enable.dsl=2

params.url = "https://silo:6886/api/v1/files/?sample__type=N&limit=1000"
params.token = null // user must supply this
params.store_dir = true
params.output_dir = "dmp-cohort"

def markers_name = new File(params.conpair_markers_bed).getName()

include { gatk_pileup } from './modules/gatk_pileup.nf'
include { samtools_index } from './modules/samtools_index.nf'

conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")

process get_bam_paths {
    // query the API for the DMP bam file paths, save them to a file
    output:
    path "${output_file}", emit: bam_paths
    script:
    output_file = "paths.txt"
    """
    get_paginated_query.py \
    "${params.url}" \
    "${params.token}" \
    path > "${output_file}"
    """
}

workflow {
    // get a list of all the DMP bam file paths
    get_bam_paths()
    get_bam_paths.out.bam_paths | set { bam_paths_txt }

    // add the adjacent .bai file
    // bam_paths | splitCsv |  map { it[0] } | map{ bam ->
    //     def bai = "${bam}".replaceFirst(/.bam$/, ".bai")
    //     return [ file("${bam}"), file("${bai}") ]
    //     } | set { bam_bai_files }
    // NOTE: SOME OF THE DMP BAMS DO NOT HAVE ADJACENT BAI FILES !!!!
    // NEED TO INDEX THEM INSTEAD.....

    bam_paths_txt | splitCsv |  map { it[0] } | set { dmp_bams }

    samtools_index(dmp_bams) | gatk_pileup | combine(conpair_markers_txt)

}
