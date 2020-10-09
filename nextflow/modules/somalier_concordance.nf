process somalier_concordance {
    // concordance analysis for somalier
    publishDir "${params.output_dir}/concordance", mode: 'copy'

    input:
    tuple path(sample_genotype), path(comparison_genotypes_dir)

    output:
    path "somalier*"

    script:
    """
    "${params.somalier_bin}" relate "${sample_genotype}" "${comparison_genotypes_dir}/*.somalier"
    """
}
// somalier relate -g sample_pairing.csv sketch_files/*.somalier
