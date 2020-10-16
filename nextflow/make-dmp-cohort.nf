// workflow for retrieving the DMP cohort .bam files and pre-processing them
nextflow.enable.dsl=2

params.url = "https://silo:6886/api/v1/files/?sample__type=N&limit=1000"
params.token = null // user must supply this

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
    get_bam_paths.out.bam_paths | set { bam_paths }
    bam_paths | splitCsv | view
}
