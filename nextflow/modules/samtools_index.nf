process samtools_index {
    if (params.store_dir == true) {
        storeDir "${params.output_dir}/index", pattern: "*.bai"
    } else {
        publishDir "${params.output_dir}/index", mode: 'copy', pattern: "*.bai"
    }

    input:
    path(bam)

    output:
    tuple path("${bam}"), path("${bai}")

    script:
    bai = "${bam}.bai"
    """
    samtools index ${bam}
    """
}
