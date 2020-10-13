#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the gatk_pileup.cwl file
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from tools import num_lines, run_cwl
from settings import CWL_DIR, CWL_ARGS, DATA_SETS, CONPAIR_MARKERS_BED, REF_FASTA

cwl_file = os.path.join(CWL_DIR, 'gatk_pileup.cwl')

class TestSnpPileupCWL(unittest.TestCase):
    def test_snp_pileup1(self):
        """
        """
        self.maxDiff = None
        input_json = {
            "bam_file": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample23.rg.md.abra.printreads.bam"),
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
                    'checksum': 'sha1$71f0e0972c0c649590fe73caddae63506e8b8a80',
                    'size': 124590,
                    'path': os.path.join(output_dir, "Sample23.pileup")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            pileup_path = os.path.join(output_dir, "Sample23.pileup")
            # shutil.copyfile(pileup_path, "Sample23.pileup")
            lines = num_lines(pileup_path)
            self.assertEqual(lines, 1025)

    def test_snp_pileup2(self):
        """
        """
        self.maxDiff = None
        input_json = {
            "bam_file": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample24.rg.md.abra.printreads.bam"),
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
                    'checksum': 'sha1$bbd785957a7afb85363e6e7ae5b7540ea717fb90',
                    'size': 109059,
                    'path': os.path.join(output_dir, "Sample24.pileup")
                    }
                }

            self.assertDictEqual(output_json, expected_output)
            pileup_path = os.path.join(output_dir, "Sample24.pileup")
            # shutil.copyfile(pileup_path, "Sample24.pileup")
            lines = num_lines(pileup_path)
            self.assertEqual(lines, 1024)


if __name__ == "__main__":
    unittest.main()
