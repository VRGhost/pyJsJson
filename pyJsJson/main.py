import argparse
import os
import sys
import contextlib
import json
import logging

import pyJsJson

logger = logging.getLogger(__name__)


def get_arg_parser():
    parser = argparse.ArgumentParser(description='Render JSON using a JSON template')
    parser.add_argument('input', help='Input JSON to be rendered')
    parser.add_argument('--search-dirs', default=(), nargs='*', help='Extra directories to be included into the search path')
    parser.add_argument('--output', default='-', help='Output file ("-" for stdout)')
    return parser


def main(args):
    pyJsJson.util.logging.configureCliLogging()
    logger.info('**** STARTED ****')
    args = get_arg_parser().parse_args(args)

    input_fname = os.path.abspath(args.input)
    search_dirs = list(args.search_dirs)
    search_dirs.insert(
        0,
        os.path.dirname(input_fname)
    )

    ds = pyJsJson.dataSource.DataSource()
    searcher = ds.searchDirs(search_dirs)

    expand = pyJsJson.expand.JsonExpand(ds, searcher)
    expand.loadCommands(pyJsJson.commands.DEFAULT_COMMANDS)

    out = expand.expandData(
        searcher.loadJsonFile(input_fname)
    )

    with contextlib.ExitStack() as stack:
        if args.output == '-':
            outf = sys.stdout
        else:
            outf = open(args.output, 'w')
            stack.enter_context(outf) # ensure that the file will be closed

        json.dump(out, outf, indent=4, sort_keys=True)
