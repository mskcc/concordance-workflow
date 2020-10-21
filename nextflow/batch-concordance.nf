// workflow for running tumor concordance for a set of tumors against a set of normals
nextflow.enable.dsl=2

params.tumor_list = "tumor_list.txt" // file with list of input tumor .bam files, one per line
params.output_dir = "output-batch"
params.conpair_cohort = "normals_conpair" // file or directory of files to run the comparison against
params.somalier_cohort = "normals_somalier" // file or directory of files to run the comparison against

include { tumor_concordance } from './tumor-concordance.nf'

workflow {
    // main workflow
    log.info("----------------")
    log.info("batch-concordance workflow params:")
    log.info("${params}")
    log.info("----------------")

    //
    // Check the Conpair and Somalier cohort items to see if they are single files or dir of files
    //
    conpair_cohort_obj = new File("${params.conpair_cohort}");
    conpair_cohort_exists = conpair_cohort_obj.exists();
    conpair_cohort_isDir = conpair_cohort_obj.isDirectory();
    conpair_cohort_isFile = conpair_cohort_obj.isFile();

    if(! conpair_cohort_exists){
        log.error("No such file or directory: ${params.conpair_cohort}")
        exit 1
    }
    if(conpair_cohort_isDir){
        conpair_normals = Channel.fromPath("${params.conpair_cohort}/*{.pileup,.pickle}").collect()
    }
    if(conpair_cohort_isFile){
        conpair_normals = Channel.fromPath("${params.conpair_cohort}")
    }

    somalier_cohort_obj = new File("${params.somalier_cohort}");
    somalier_cohort_exists = somalier_cohort_obj.exists();
    somalier_cohort_isDir = somalier_cohort_obj.isDirectory();
    somalier_cohort_isFile = somalier_cohort_obj.isFile();

    if(! somalier_cohort_exists){
        log.error("No such file or directory: ${params.somalier_cohort}")
        exit 1
    }
    if(somalier_cohort_isDir){
        somalier_normals = Channel.fromPath("${params.somalier_cohort}/*.somalier").collect()
    }
    if(somalier_cohort_isFile){
        somalier_normals = Channel.fromPath("${params.somalier_cohort}")
    }

    conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")
    somalier_sites = Channel.fromPath("${params.somalier_sites}")

    tumor_list_file = Channel.fromPath("${params.tumor_list}")

    // add the adjacent .bai file
    tumor_list_file | splitCsv | map { it[0] } | map{ bam ->
        def bai = "${bam}".replaceFirst(/.bam$/, ".bai")
        return [ file("${bam}"), file("${bai}") ]
        } | set { samples_bams_bais }

    // run the workflow on all the samples
    tumor_concordance(samples_bams_bais, conpair_normals, somalier_normals, conpair_markers_txt, somalier_sites)

    // aggregate some file outputs
    tumor_concordance.out.conpair_tsv.collectFile(name: 'conpair_concordance.tsv', storeDir: "${params.output_dir}", keepHeader: true)
    tumor_concordance.out.somalier_groups.collectFile(name: 'somalier_groups.tsv', storeDir: "${params.output_dir}")
    tumor_concordance.out.somalier_pairs.collectFile(name: 'somalier_pairs.tsv', storeDir: "${params.output_dir}", keepHeader: true)
    tumor_concordance.out.somalier_samples.collectFile(name: 'somalier_samples.tsv', storeDir: "${params.output_dir}", keepHeader: true)

}
