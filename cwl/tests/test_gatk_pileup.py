#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the gatk_pileup.cwl file
"""
import os
import json
import shutil
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import num_lines, run_cwl, num_fields
from settings import CWL_DIR, CWL_ARGS, DATA_SETS, CONPAIR_MARKERS_BED, REF_FASTA

cwl_file = os.path.join(CWL_DIR, 'gatk_pileup.cwl')

class TestSnpPileupCWL(unittest.TestCase):
    def test_snp_pileup1(self):
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
            "regions_bed": {
                "path": CONPAIR_MARKERS_BED,
                "class": "File"
            },
            "output_filename": "Sample23.pileup"
        }

        with TemporaryDirectory() as tmpdir:
            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file,
                CWL_ARGS = CWL_ARGS)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, "Sample23.pileup"),
                    'basename': "Sample23.pileup",
                    'class': 'File',
                    'checksum': 'sha1$6b1070a3a78ca495218e9f6a1a828203105c96a0',
                    'size': 2759826,
                    'path': os.path.join(output_dir, "Sample23.pileup")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            pileup_path = os.path.join(output_dir, "Sample23.pileup")
            # shutil.copyfile(pileup_path, "Sample23.pileup")

            lines = num_lines(pileup_path)
            self.assertEqual(lines, 1025)

            fields = num_fields(pileup_path, delimiter = ' ')
            self.assertEqual(fields, 8)

    def test_snp_pileup2(self):
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
            "regions_bed": {
                "path": CONPAIR_MARKERS_BED,
                "class": "File"
            },
            "output_filename": "Sample24.pileup"
        }

        with TemporaryDirectory() as tmpdir:
            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file,
                CWL_ARGS = CWL_ARGS)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, "Sample24.pileup"),
                    'basename': "Sample24.pileup",
                    'class': 'File',
                    'checksum': 'sha1$a27039b65de9272e9a7b180e1b0e911c6484efbe',
                    'size': 2358580,
                    'path': os.path.join(output_dir, "Sample24.pileup")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            pileup_path = os.path.join(output_dir, "Sample24.pileup")
            # shutil.copyfile(pileup_path, "Sample24.pileup")

            lines = num_lines(pileup_path)
            self.assertEqual(lines, 1024)

            fields = num_fields(pileup_path, delimiter = ' ')
            self.assertEqual(fields, 8)


if __name__ == "__main__":
    unittest.main()
