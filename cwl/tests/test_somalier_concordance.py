#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the somalier_concordance.cwl file
"""
import shutil
import os
import csv
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import run_cwl, num_lines, num_fields
from settings import CWL_DIR, DATA_SETS, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'somalier_concordance.cwl')

class TestSomalierConcordanceCWL(unittest.TestCase):
    def test_concordance1(self):
        self.maxDiff = None
        with TemporaryDirectory() as tmpdir:
            # copy over a Normal genotype file to the temporary dir
            normals_dir_path = os.path.join(tmpdir, "normals")
            os.mkdir(normals_dir_path)
            shutil.copyfile(os.path.join(DATA_SETS['Proj_08390_G']['GENOTYPES_DIR'], "Sample24.somalier"), os.path.join(normals_dir_path, "Sample24.somalier"))

            input_json = {
                "tumor_genotype_file": {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['GENOTYPES_DIR'], "Sample23.somalier"),
                    "class": "File"
                },
                "cohort_genotype_dir": {
                    "path": normals_dir_path,
                    "class": "Directory"
                }
            }

            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                CWL_ARGS = CWL_ARGS,
                cwl_file = cwl_file,
                print_stdout = False,
                print_command = False,
                check_returncode = True)

            expected_output = {
                'html': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.html"),
                    'basename': "somalier.html",
                    'class': 'File',
                    'checksum': 'sha1$d78cc873ba6219ab57d5d76836eed8212cd96ce6',
                    'size': 22950,
                    'path': os.path.join(output_dir, "somalier.html")
                    },
                'pairs_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.pairs.tsv"),
                    'basename': "somalier.pairs.tsv",
                    'class': 'File',
                    'checksum': 'sha1$fdb140d0db51b0ede23208210ae59d03e496c5f6',
                    'size': 244,
                    'path': os.path.join(output_dir, "somalier.pairs.tsv")
                    },
                'samples_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "somalier.samples.tsv"),
                    'basename': "somalier.samples.tsv",
                    'class': 'File',
                    'checksum': 'sha1$c98bd07ac5a3a90c1386438171fa1113a06a14e8',
                    'size': 468,
                    'path': os.path.join(output_dir, "somalier.samples.tsv")
                    },
                }

            self.assertDictEqual(output_json, expected_output)

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
