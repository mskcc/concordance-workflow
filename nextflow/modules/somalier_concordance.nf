process somalier_concordance {
    // concordance analysis for somalier
    publishDir "${params.output_dir}/concordance", mode: 'copy'

    input:
    tuple path(sample_genotype), path(comparison_genotypes_dir)

    output:
    tuple path("${output_groups}"), path("${output_html}"), path("${output_pairs}"), path("${output_samples}")

    script:
    output_prefix = "${sample_genotype}".replaceFirst(/.somalier$/, "")
    output_groups = "${output_prefix}.groups.tsv"
    output_html = "${output_prefix}.html"
    output_pairs = "${output_prefix}.pairs.tsv"
    output_samples = "${output_prefix}.samples.tsv"
    """
    somalier relate \
    --output-prefix "${output_prefix}" \
    "${sample_genotype}" \
    "${comparison_genotypes_dir}/*.somalier"
    """
}
// somalier relate -g sample_pairing.csv sketch_files/*.somalier
// "${params.somalier_bin}"
