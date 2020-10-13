#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the somalier_extract.cwl file
"""
import shutil
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import run_cwl
from settings import CWL_DIR, DATA_SETS, SOMALIER_SITES, REF_FASTA

cwl_file = os.path.join(CWL_DIR, 'somalier_extract.cwl')

class TestSomalierExtractCWL(unittest.TestCase):
    def test_extrace1(self):
        """
        """
        self.maxDiff = None
        input_json = {
            "bam_file": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample23.bam"),
                "class": "File"
            },
            "ref_fasta": {
                "path": REF_FASTA,
                "class": "File"
            },
            "sites": {
                "path": SOMALIER_SITES,
                "class": "File"
            }
        }
        with TemporaryDirectory() as tmpdir:
            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, "Sample23.somalier"),
                    'basename': "Sample23.somalier",
                    'class': 'File',
                    'checksum': 'sha1$159fa91beded446440962f211b3fa771e5764559',
                    'size': 12292,
                    'path': os.path.join(output_dir, "Sample23.somalier")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            # pileup_path = os.path.join(output_dir, "Sample23.somalier")
            # shutil.copyfile(pileup_path, "Sample23.somalier")

    def test_extrace2(self):
        """
        """
        self.maxDiff = None
        input_json = {
            "bam_file": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample24.bam"),
                "class": "File"
            },
            "ref_fasta": {
                "path": REF_FASTA,
                "class": "File"
            },
            "sites": {
                "path": SOMALIER_SITES,
                "class": "File"
            }
        }
        with TemporaryDirectory() as tmpdir:
            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, "Sample24.somalier"),
                    'basename': "Sample24.somalier",
                    'class': 'File',
                    'checksum': 'sha1$e912f8368502325be0bae87e8b6205ff627ec8d8',
                    'size': 12292,
                    'path': os.path.join(output_dir, "Sample24.somalier")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            # pileup_path = os.path.join(output_dir, "Sample24.somalier")
            # shutil.copyfile(pileup_path, "Sample24.somalier")


if __name__ == "__main__":
    unittest.main()
