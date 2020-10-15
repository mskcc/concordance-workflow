#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the put_in_dir.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile
from settings import CWL_DIR, CWL_ARGS
from tools import run_cwl

cwl_file = os.path.join(CWL_DIR, 'put_in_dir.cwl')

class TestPutInDir(unittest.TestCase):
    def test_put_two_files_in_dir(self):
        """
        Test that two files are put in the dir correctly
        """
        with TemporaryDirectory() as tmpdir, NamedTemporaryFile() as file1, NamedTemporaryFile() as file2:
            # set path to the dir which this CWL should to output to
            output_dir = os.path.join(tmpdir, "output")

            # create input data
            input_json = {
                "output_directory_name": output_dir,
                "files": [
                    {
                      "class": "File",
                      "path": file1.name
                    },
                    {
                      "class": "File",
                      "path": file2.name
                    }
                ]
            }

            # write input data
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            # make sure the output is a dir
            self.assertTrue("directory" in output_json)
            # make sure there's only one element output
            self.assertEqual(len(output_json), 1)
            # make sure the dir exists
            self.assertTrue(os.path.exists( output_json['directory']['path'] ))
            self.assertTrue(os.path.isdir( output_json['directory']['path'] ))
            self.assertEqual(output_dir, output_json['directory']['path'])
            # make sure both files were output to the dir
            self.assertEqual(len(os.listdir(output_json['directory']['path'])), 2)
            self.assertTrue(os.path.basename(file1.name)in os.listdir(output_json['directory']['path']) )
            self.assertTrue(os.path.basename(file2.name)in os.listdir(output_json['directory']['path']) )

    def test_put_one_file1_in_dir(self):
        """
        Test that one file is put in the dir correctly
        """
        with TemporaryDirectory() as tmpdir, NamedTemporaryFile() as file1:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "output_directory_name": output_dir,
                "files": [
                    {
                      "class": "File",
                      "path": file1.name
                    },
                ]
            }
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

            output_json, output_dir = run_cwl(
                testcase = self,
                tmpdir = tmpdir,
                input_json = input_json,
                cwl_file = cwl_file)

            # make sure the dir exists
            self.assertTrue(os.path.exists( output_json['directory']['path'] ))
            self.assertTrue(os.path.isdir( output_json['directory']['path'] ))
            self.assertEqual(output_dir, output_json['directory']['path'])
            # make sure both files were output to the dir
            self.assertEqual(len(os.listdir(output_json['directory']['path'])), 1)
            self.assertTrue(os.path.basename(file1.name)in os.listdir(output_json['directory']['path']) )


if __name__ == "__main__":
    unittest.main()
