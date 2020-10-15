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
from settings import CWL_DIR, DATA_SETS, CWL_ARGS, CONPAIR_MARKERS_TXT

cwl_file = os.path.join(CWL_DIR, 'conpair_concordance.cwl')

class TestSomalierConcordanceCWL(unittest.TestCase):
    def test_conpair_concordance1(self):
        self.maxDiff = None
        with TemporaryDirectory() as tmpdir:
            # copy over a Normal genotype file to the temporary dir
            normals_dir_path = os.path.join(tmpdir, "normals")
            os.mkdir(normals_dir_path)
            shutil.copyfile(os.path.join(DATA_SETS['Proj_08390_G']['LIKELIHOODS_DIR'], "Sample24.pickle"), os.path.join(normals_dir_path, "Sample24.pickle"))

            input_json = {
                "tumor_file": {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['LIKELIHOODS_DIR'], "Sample23.pickle"),
                    "class": "File"
                },
                "cohort_dir": {
                    "path": normals_dir_path,
                    "class": "Directory"
                },
                "markers": {
                    "path": CONPAIR_MARKERS_TXT,
                    "class": "File"
                }
            }

            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            expected_output = {
                'concordance_tsv': {
                    'location': 'file://' + os.path.join(output_dir, "Sample23.pickle.concordance.tsv"),
                    'basename': "Sample23.pickle.concordance.tsv",
                    'class': 'File',
                    # 'checksum': 'sha1$e7f75336ea679447df581c4e2edc7339bae9a186', # dont use the checksum or size because the file contains the filepaths and those change each time
                    # 'size': 279,
                    'path': os.path.join(output_dir, "Sample23.pickle.concordance.tsv")
                    }
                }
            output_json['concordance_tsv'].pop('checksum')
            output_json['concordance_tsv'].pop('size')

            self.assertDictEqual(output_json, expected_output)

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


if __name__ == "__main__":
    unittest.main()
