#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the conpair_likelihoods.cwl file
"""
import shutil
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import run_cwl
from settings import CWL_DIR, DATA_SETS, CONPAIR_MARKERS_TXT, REF_FASTA

cwl_file = os.path.join(CWL_DIR, 'conpair_likelihoods.cwl')

class TestLikelihoodsCWL(unittest.TestCase):
    def test_likelihoods1(self):
        """
        """
        self.maxDiff = None
        input_json = {
            "pileup": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['PILEUP_DIR'], "Sample23.pileup"),
                "class": "File"
            },
            "markers": {
                "path": CONPAIR_MARKERS_TXT,
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
                    'location': 'file://' + os.path.join(output_dir, "Sample23.pickle"),
                    'basename': "Sample23.pickle",
                    'class': 'File',
                    'checksum': 'sha1$71f0e0972c0c649590fe73caddae63506e8b8a80',
                    'size': 124590,
                    'path': os.path.join(output_dir, "Sample23.pickle")
                    }
                }
            self.assertDictEqual(output_json, expected_output)
            pileup_path = os.path.join(output_dir, "Sample23.pickle")
            shutil.copyfile(pileup_path, "Sample23.pickle")


if __name__ == "__main__":
    unittest.main()
