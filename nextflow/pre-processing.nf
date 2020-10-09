// workflow for pre-processing .bam file(s) for use as a reference cohort in the main concordance workflow
nextflow.enable.dsl=2

params.input = "input" // directory or file of input .bams
params.output_dir = "pre-processing_output"
File input_filepath = new File("${params.input}");
boolean input_exists = input_filepath.exists();
boolean isDirectory = input_filepath.isDirectory(); // Check if it's a directory
boolean isFile = input_filepath.isFile();      // Check if it's a regular file

include { conpair_likelihoods } from './modules/conpair_likelihoods.nf'
include { gatk_pileup } from './modules/gatk_pileup.nf'
include { somalier_extract } from './modules/somalier_extract.nf'

log.info("----------------")
log.info("workflow params:")
log.info("${params}")
log.info("----------------")

if(! input_exists){
    log.error("No such file or directory: ${params.input}")
    exit 1
}

if(isDirectory){
    input_items = Channel.fromFilePairs("${params.input}/*{.bam,.bai}").map{ sampleID, items ->
        def bai = items[0]
        def bam = items[1]
        return([bam, bai])
    }
}
if(isFile){
    input_items = Channel.fromPath("${params.input}").map{ bam ->
        def bai = "${bam}".replaceFirst(/.bam$/, ".bai") // search for 'sample.bai'

        // if it doesnt exist, look for 'sample.bam.bai'
        if(! new File("${bai}").exists()){
            bai = "${bam}.bai"
            if(! new File("${bai}").exists()){
                log.error("No such file or directory: ${bai}")
                exit 1
            }
        }
        return([bam, bai])
    }
}
conpair_markers_txt = Channel.fromPath("${params.conpair_markers_txt}")
somalier_sites = Channel.fromPath("${params.somalier_sites}")

workflow {
    // Conpair
    gatk_pileup(input_items) | combine(conpair_markers_txt) | conpair_likelihoods
    // somalier
    input_items.combine(somalier_sites) | somalier_extract
}
