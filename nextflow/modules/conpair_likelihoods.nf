process conpair_likelihoods {
    // make a Python Pickle of the genotype likelihoods for faster loading in Conpair
    if (params.store_dir == true) {
        storeDir "${params.output_dir}/likelihoods/${params.markers_name}"
    } else {
        publishDir "${params.output_dir}/likelihoods", mode: 'copy'
    }


    input:
    tuple path(pileup), path(markers) // params.conpair_markers_txt

    output:
    path "${output_file}", emit: likelihoods

    script:
    output_file = "${pileup}".replaceFirst(/.pileup$/, ".pickle")
    """
    make_genotype_likelihoods.py \
    --pileup "${pileup}" \
    --markers "${markers}"
    """
}
