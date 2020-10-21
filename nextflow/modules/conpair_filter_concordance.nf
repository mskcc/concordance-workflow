process conpair_filter_concordance {
    // keep only high concordance values
    publishDir "${params.output_dir}/", mode: 'copy'

    input:
    path(concordance_tsv)

    output:
    path "${output_file}", emit: filtered_concordance

    script:
    output_file = "${concordance_tsv}".replaceFirst(/.tsv$/, ".filtered.tsv")
    """
    # save headers
    head -1 "${concordance_tsv}" > "${output_file}"

    # get all rows with concordance >0.50 (1st col); skip non-numeric values (1st col), skip rows where num_markers_used < 10 (2nd col)
    tail -n +2 "${concordance_tsv}" | \
    awk '{ if(\$1+0 == \$1) print \$0 }' | \
    awk '{if(\$2 > 10) print \$0 }' | \
    awk '{if(\$1 > 0.50) print \$0 }' >> "${output_file}"
    """
}
