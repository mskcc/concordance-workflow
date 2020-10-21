// main workflow for comparing one bam against another set of concordance files
nextflow.enable.dsl=2

params.bam = "sample.bam"
params.bai = 'sample.bam.bai'
params.output_dir = "output"
params.conpair_cohort = "normals_conpair" // file or directory of files to run the comparison against
params.somalier_cohort = "normals_somalier" // file or directory of files to run the comparison against

include { conpair_concordance } from './modules/conpair_concordance.nf'
include { conpair_likelihoods } from './modules/conpair_likelihoods.nf'
include { gatk_pileup } from './modules/gatk_pileup.nf'
include { stage_normals } from './modules/stage_normals.nf'
include { somalier_extract } from './modules/somalier_extract.nf'
include { somalier_concordance } from './modules/somalier_concordance.nf'

log.info("----------------")
log.info("workflow params:")
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



sample_bam_bai = Channel.from([ file("${params.bam}"), file("${params.bai}") ]).collect()
conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")
somalier_sites = Channel.fromPath("${params.somalier_sites}")

workflow tumor_concordance {
    // sub-workflow unit
    take:
        sample_bam_bai
        conpair_normals
        somalier_normals
        conpair_markers_txt
        somalier_sites

    main:
        // put all the normals into a single channel of two elements;
        // all_normals = [ [conpair_files, ...], [somalier_files, ...] ]
        conpair_normals_list = conpair_normals.toList()
        somalier_normals_list = somalier_normals.toList()
        conpair_normals_list.combine(somalier_normals_list).set { all_normals }

        // stage all the normals in separate directories for passing to Conpair and Somalier separately
        // this helps us to use an unevaluated glob expression for their CLI args later
        stage_normals(all_normals)

        // Conpair
        gatk_pileup(sample_bam_bai) | combine(conpair_markers_txt) | conpair_likelihoods | combine(stage_normals.out.conpair_dir) | combine(conpair_markers_txt) | conpair_concordance

        // somalier
        sample_bam_bai.combine(somalier_sites) | somalier_extract | combine(stage_normals.out.somalier_dir) | somalier_concordance
}

workflow {
    // main workflow
    tumor_concordance(sample_bam_bai, conpair_normals, somalier_normals, conpair_markers_txt, somalier_sites)
}
