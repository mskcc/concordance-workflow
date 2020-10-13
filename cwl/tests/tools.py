"""
Helper functions for running tests
"""
import os
import json
import subprocess as sp
from settings import CWL_DIR, CWL_ARGS, DATA_SETS, CONPAIR_MARKERS_BED, REF_FASTA

def run_command(args):
    """
    Helper function to run a shell command easier

    Parameters
    ----------
    args: list
        a list of shell args to execute
    """
    process = sp.Popen(args, stdout = sp.PIPE, stderr = sp.PIPE, universal_newlines = True)
    proc_stdout, proc_stderr = process.communicate()
    returncode = process.returncode
    proc_stdout = proc_stdout.strip()
    proc_stderr = proc_stderr.strip()
    return(returncode, proc_stdout, proc_stderr)

def run_cwl(testcase, tmpdir, input_json, cwl_file, CWL_ARGS = CWL_ARGS):
    input_json_file = os.path.join(tmpdir, "input.json")
    with open(input_json_file, "w") as json_out:
        json.dump(input_json, json_out)

    output_dir = os.path.join(tmpdir, "output")
    tmp_dir = os.path.join(tmpdir, "tmp")
    cache_dir = os.path.join(tmpdir, "cache")

    command = [
        "cwl-runner",
        *CWL_ARGS,
        "--outdir", output_dir,
        "--tmpdir-prefix", tmp_dir,
        "--cachedir", cache_dir,
        cwl_file, input_json_file
        ]
    returncode, proc_stdout, proc_stderr = run_command(command)

    if returncode != 0:
        print(proc_stderr)

    testcase.assertEqual(returncode, 0)

    output_json = json.loads(proc_stdout)
    return(output_json, output_dir)

def num_lines(filepath):
    num = 0
    with open(filepath) as f:
        for line in f:
            num += 1
    return(num)

def num_fields(filepath, delimiter = '\t'):
    with open(filepath) as f:
        line = next(f)
    parts = line.split(delimiter)
    return(len(parts))
