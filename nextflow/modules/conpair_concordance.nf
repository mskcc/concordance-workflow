process conpair_concordance {
    publishDir "${params.output_dir}/concordance", mode: 'copy'

    input:
    tuple path(tumor_pileup), path(normals_dir), path(markers) // params.conpair_markers_txt

    output:
    path "${output_file}", emit: concordance_vals

    script:
    output_file = "${tumor_pileup}.concordance.tsv"
    """
    run.py concordance \
    "${tumor_pileup}" "${normals_dir}/*" \
    --markers "${markers}" \
    --output-file "${output_file}" \
    --threads "${task.cpus}" \
    """
}
