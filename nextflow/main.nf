// main workflow for comparing one bam against another set of concordance files
nextflow.enable.dsl=2

params.bam = "sample.bam"
params.bai = 'sample.bam.bai'
params.compare_against = "normals" // file or directory of files to run the comparison against
params.output_dir = "output"

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

// get all the items passed for comparison
def compare_path = "${params.compare_against}"
File compare_filepath = new File(compare_path);
boolean compare_exists = compare_filepath.exists();
boolean isDirectory = compare_filepath.isDirectory(); // Check if it's a directory
boolean isFile = compare_filepath.isFile();      // Check if it's a regular file

if(! compare_exists){
    log.error("No such file or directory: ${compare_path}")
    exit 1
}

if(isDirectory){
    compare_items = Channel.fromPath("${compare_path}/*{.somalier,.pileup,.pickle}").collect()
}
if(isFile){
    compare_items = Channel.fromPath("${compare_path}")
}

sample_bam_bai = Channel.from([ file("${params.bam}"), file("${params.bai}") ]).collect()
conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")
somalier_sites = Channel.fromPath("${params.somalier_sites}")

workflow {
    stage_normals(compare_items)

    // Conpair
    gatk_pileup(sample_bam_bai) | combine(conpair_markers_txt) | conpair_likelihoods | combine(stage_normals.out.conpair_dir) | combine(conpair_markers_txt) | conpair_concordance

    // somalier
    sample_bam_bai.combine(somalier_sites) | somalier_extract | combine(stage_normals.out.somalier_dir) | somalier_concordance
}
