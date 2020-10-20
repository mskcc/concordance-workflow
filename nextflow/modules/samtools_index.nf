process samtools_index {
    if (params.store_dir == true) {
        storeDir "${params.output_dir}/index" //, pattern: "*.bai" <- this does not work...
    } else {
        publishDir "${params.output_dir}/index", mode: 'copy', pattern: "*.bai"
    }
    errorStrategy 'ignore' // samtools index: "-N.bam" is in a format that cannot be usefully indexed // corrupted file

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
