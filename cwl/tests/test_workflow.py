#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the workflow.cwl file
"""
import shutil
import os
import csv
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import run_cwl, num_lines, num_fields
from settings import CWL_DIR, DATA_SETS, CWL_ARGS, REF_FASTA, SOMALIER_SITES, CONPAIR_MARKERS_BED, CONPAIR_MARKERS_TXT

cwl_file = os.path.join(CWL_DIR, 'workflow.cwl')

class TestWorkflowCWL(unittest.TestCase):
    def test_workflow1(self):
        input_json = {
            "tumor_bam": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample23.bam"),
                "class": "File"
            },
            "ref_fasta": {
                "path": REF_FASTA,
                "class": "File"
            },
            "conpair_markers_bed": {
                "path": CONPAIR_MARKERS_BED,
                "class": "File"
            },
            "conpair_markers_txt": {
                "path": CONPAIR_MARKERS_TXT,
                "class": "File"
            },
            "somalier_sites": {
                "path": SOMALIER_SITES,
                "class": "File"
            },
            "conpair_normal_genotypes": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['LIKELIHOODS_DIR'], "Sample24.pickle"),
                    "class": "File"
                }
            ],
            "somalier_normal_genotypes": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['GENOTYPES_DIR'], "Sample24.somalier"),
                    "class": "File"
                }
            ]
        }
        with TemporaryDirectory() as tmpdir:
            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            expected_output = {
                'conpair_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "Sample23.pickle.concordance.tsv"),
                    'basename': "Sample23.pickle.concordance.tsv",
                    'class': 'File',
                    # 'checksum': 'sha1$e7f75336ea679447df581c4e2edc7339bae9a186', # dont use the checksum or size because the file contains the filepaths and those change each time
                    # 'size': 279,
                    'path': os.path.join(output_dir, "Sample23.pickle.concordance.tsv")
                    },
                'somalier_html': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.html"),
                    'basename': "somalier.html",
                    'class': 'File',
                    'checksum': 'sha1$d78cc873ba6219ab57d5d76836eed8212cd96ce6',
                    'size': 22950,
                    'path': os.path.join(output_dir, "somalier.html")
                    },
                'somalier_pairs_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.pairs.tsv"),
                    'basename': "somalier.pairs.tsv",
                    'class': 'File',
                    'checksum': 'sha1$fdb140d0db51b0ede23208210ae59d03e496c5f6',
                    'size': 244,
                    'path': os.path.join(output_dir, "somalier.pairs.tsv")
                    },
                'somalier_samples_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.samples.tsv"),
                    'basename': "somalier.samples.tsv",
                    'class': 'File',
                    'checksum': 'sha1$c98bd07ac5a3a90c1386438171fa1113a06a14e8',
                    'size': 468,
                    'path': os.path.join(output_dir, "somalier.samples.tsv")
                    },
                }
            output_json['conpair_tsv'].pop('checksum')
            output_json['conpair_tsv'].pop('size')

            self.assertDictEqual(output_json, expected_output)

            #
            # Validate Conpair output
            #
            concordance_file = os.path.join(output_dir, "Sample23.pickle.concordance.tsv")
            with open(concordance_file) as f:
                reader = csv.DictReader(f, delimiter = '\t')
                rows  = [ row for row in reader ]

            expected_rows = [
            {
                'concordance': '0.9885297184567258',
                'num_markers_used': '959',
                'num_total_markers': '1024',
                'tumor': 'Sample23',
                'normal': 'Sample24',
                # 'tumor_pileup': '/var/lib/cwl/stg35428a9e-1166-4a1f-87ad-70697da56267/Sample23.pickle',
                # 'normal_pileup': '/var/lib/cwl/stgc3f9e453-b2d4-4085-95df-07686d22f8ff/normals/Sample24.pickle'
                }
            ]

            # remove the file paths from the results because they always change
            rows[0].pop('tumor_pileup')
            rows[0].pop('normal_pileup')

            self.assertEqual(rows, expected_rows)

            #
            # Validate Somalier output
            #
            pairs_tsv = os.path.join(output_dir, "somalier.pairs.tsv")
            self.assertEqual(num_lines(pairs_tsv), 2)
            self.assertEqual(num_fields(pairs_tsv), 17)
            with open(pairs_tsv) as f:
                reader = csv.DictReader(f, delimiter = '\t')
                rows = [ row for row in reader ]
            expected_rows = [
            {'#sample_a': 'Sample23', 'sample_b': 'Sample24', 'relatedness': '1.000', 'ibs0': '0', 'ibs2': '627', 'hom_concordance': '0.870', 'hets_a': '403', 'hets_b': '370', 'hets_ab': '694', 'shared_hets': '347', 'hom_alts_a': '207', 'hom_alts_b': '146', 'shared_hom_alts': '127', 'n': '627', 'x_ibs0': '0', 'x_ibs2': '17', 'expected_relatedness': '-1.0'}
            ]
            self.assertEqual(rows, expected_rows)

            samples_tsv = os.path.join(output_dir, "somalier.samples.tsv")
            self.assertEqual(num_lines(samples_tsv), 3)
            self.assertEqual(num_fields(samples_tsv), 25)
            with open(samples_tsv) as f:
                reader = csv.DictReader(f, delimiter = '\t')
                rows = [ row for row in reader ]
            expected_rows = [
            {'#family_id': 'Sample23', 'sample_id': 'Sample23', 'paternal_id': '-9', 'maternal_id': '-9', 'sex': '-9', 'phenotype': '-9', 'original_pedigree_sex': '-9', 'gt_depth_mean': '31.5', 'gt_depth_sd': '21.3', 'depth_mean': '30.8', 'depth_sd': '21.5', 'ab_mean': '0.44', 'ab_std': '0.41', 'n_hom_ref': '258', 'n_het': '403', 'n_hom_alt': '207', 'n_unknown': '122', 'p_middling_ab': '0.048', 'X_depth_mean': '16.28', 'X_n': '25', 'X_hom_ref': '7', 'X_het': '1', 'X_hom_alt': '17', 'Y_depth_mean': '0.00', 'Y_n': '0'},
            {'#family_id': 'Sample24', 'sample_id': 'Sample24', 'paternal_id': '-9', 'maternal_id': '-9', 'sex': '-9', 'phenotype': '-9', 'original_pedigree_sex': '-9', 'gt_depth_mean': '25.8', 'gt_depth_sd': '13.8', 'depth_mean': '24.8', 'depth_sd': '14.2', 'ab_mean': '0.43', 'ab_std': '0.44', 'n_hom_ref': '174', 'n_het': '370', 'n_hom_alt': '146', 'n_unknown': '300', 'p_middling_ab': '0.147', 'X_depth_mean': '15.44', 'X_n': '18', 'X_hom_ref': '7', 'X_het': '1', 'X_hom_alt': '10', 'Y_depth_mean': '0.00', 'Y_n': '0'}
            ]
            self.assertEqual(rows, expected_rows)



if __name__ == "__main__":
    unittest.main()
