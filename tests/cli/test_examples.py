"""This test uses 'examples' folder to test CLI behaviour."""

import os
import glob
import subprocess
import json

import pytest


@pytest.fixture
def EXAMPLES_DIR(PROJECT_ROOT):
    return os.path.join(PROJECT_ROOT, 'examples')


@pytest.mark.parametrize('update_path_by', [
    'cwd', 'cli_arg'
])
def test_examples(cli_popen_args, EXAMPLES_DIR, update_path_by):
    exampele_files = dict(
        (
            # fname -> full path
            os.path.basename(full_path),
            full_path
        )
        for full_path in glob.glob(os.path.join(EXAMPLES_DIR, '*.json'))
    )

    # Call the example via the CLI (but only if -output exists. Otherwise just fail.)
    for fname in exampele_files.keys():
        expected_out_fname = "{}-output.json".format(os.path.splitext(fname)[0])
        if (expected_out_fname not in exampele_files):
            assert fname.endswith('-output.json'), "Only output files are allowed not to have their outputs"
            continue

        call_args = cli_popen_args.copy()
        call_args['args'] += (exampele_files[fname], )
        if update_path_by == 'cwd':
            call_args['cwd'] = EXAMPLES_DIR
        elif update_path_by == 'cli_arg':
            # cwd somewhere meaningless so the relative path lookups fail
            call_args['cwd'] = os.path.abspath(os.sep) # This is FS root
            call_args['args'] += ('--search-dirs', EXAMPLES_DIR)
        else:
            raise NotImplementedError(update_path_by)

        out_json = subprocess.check_call(**call_args)
        with open(exampele_files[expected_out_fname], 'r') as fin:
            expected_out = json.load(fin)
        assert out_json == expected_out
