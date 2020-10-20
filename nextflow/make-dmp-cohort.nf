// workflow for retrieving the DMP cohort .bam files and pre-processing them
// needs to run as user voyager; make sure to chmod -R g+rw . the entire pwd
// $ ./nextflow  run -resume make-dmp-cohort.nf --token <token> --store_dir true
nextflow.enable.dsl=2

params.url = "https://silo:6886/api/v1/files/?sample__type=N&limit=1000"
params.token = null // user must supply this
// params.store_dir = true // this must be supplied from command line to override the nextflow.config value
params.output_dir = "dmp-cohort"

markers_name = new File(params.conpair_markers_bed).getName()
params.markers_name = "${markers_name}"
sites_name = new File(params.somalier_sites).getName()
params.sites_name = "${sites_name}"

log.info("----------------")
log.info("workflow params:")
log.info("${params}")
log.info("----------------")

include { gatk_pileup } from './modules/gatk_pileup.nf'
include { samtools_index } from './modules/samtools_index.nf'
include { conpair_likelihoods } from './modules/conpair_likelihoods.nf'
include { somalier_extract } from './modules/somalier_extract.nf'

conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")
somalier_sites = Channel.fromPath("${params.somalier_sites}")

process get_bam_paths {
    // query the API for the DMP bam file paths, save them to a file
    storeDir "${params.output_dir}"

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
    bam_paths_txt | splitCsv |  map { it[0] } | map{ bam ->
        def bai = "${bam}".replaceFirst(/.bam$/, ".bai")
        return [ file("${bam}"), file("${bai}") ]
        } | set { dmp_bams_bais }
    // NOTE: SOME OF THE DMP BAMS DO NOT HAVE ADJACENT BAI FILES !!!!
    // NEED TO INDEX THEM INSTEAD.....

    // // need to re-index because some indexes are missing
    // bam_paths_txt | splitCsv |  map { it[0] } | set { dmp_bams }
    // samtools_index(dmp_bams) | set { dmp_bams_bais }
    // NOTE NOTE: just ignore errors caused by invalid .bai file instead...

    // Conpair
    gatk_pileup(dmp_bams_bais) | combine(conpair_markers_txt) | conpair_likelihoods

    //
    // gatk_pileup(input_items) | combine(conpair_markers_txt) | conpair_likelihoods

    // // somalier
    dmp_bams_bais.combine(somalier_sites) | somalier_extract

}
