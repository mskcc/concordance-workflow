process stage_normals {
    input:
    file(input_files: '*')

    output:
    path "${conpair_dir}", emit: conpair_dir
    path "${somalier_dir}", emit: somalier_dir

    script:
    conpair_dir = "conpair_normals"
    somalier_dir = "somalier_normals"
    """
    mkdir "${conpair_dir}"
    mkdir "${somalier_dir}"

    mv *.pickle "${conpair_dir}/" || :
    mv *.pileup "${conpair_dir}/" || :
    mv *.somalier "${somalier_dir}/" || :
    """
}
