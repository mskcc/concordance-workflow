"""
Put settings to use for the tests in here for easier access
"""
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CWL_DIR = os.path.realpath(os.path.join("..", "cwl"))

# common args to be included in all cwltool invocations
CWL_ARGS = [
    "--preserve-environment", "PATH",
    "--preserve-environment", "SINGULARITY_CACHEDIR",
    "--singularity"
]

# location on the filesystem for static fixtures
FIXTURES_DIR = os.environ.get('FIXTURES_DIR', '/juno/work/ci/concordance-workflow/fixtures')
SOMALIER_SITES = '/juno/work/ci/concordance-workflow/markers/FP_tiling_genotypes_for_Somalier.txt'
CONPAIR_MARKERS_BED = '/juno/work/ci/concordance-workflow/markers/IMPACT468/FP_tiling_genotypes_for_Conpair.bed'
CONPAIR_MARKERS_TXT = '/juno/work/ci/concordance-workflow/markers/IMPACT468/FP_tiling_genotypes_for_Conpair.txt'
REF_FASTA = '/juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta'
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.dict
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.amb
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.ann
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.bwt
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.dict
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.fai
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.index
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.pac
# /juno/work/ci/resources/genomes/GRCh37/fasta/b37.fasta.sa

DATA_SETS = {
    "Proj_08390_G": {
        "BAM_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "bam"),
        "PILEUP_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "pileup"),
        "LIKELIHOODS_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "likelihoods"), # Conpair pileup likelihoods .pickle files
        "GENOTYPES_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "extracted_genotype") # Somalier extracted genotype files
    }
}
