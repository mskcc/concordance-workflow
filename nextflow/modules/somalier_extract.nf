process somalier_extract {
    // Generate somalier extracted genotype file needed for concordance
    // NOTE: somalier automatically names the file based on the bam file RG read group labels, NOT the filename...
    publishDir "${params.output_dir}/extracted_genotype", mode: 'copy'

    input:
    tuple path(bam), path(bai), path(sites)

    output:
    path "*.somalier", emit: extracted_genotype

    script:
    """
    "${params.somalier_bin}" extract \
    --sites "${sites}" \
    -f "${params.ref_fasta}" \
    "${bam}"
    """
}
