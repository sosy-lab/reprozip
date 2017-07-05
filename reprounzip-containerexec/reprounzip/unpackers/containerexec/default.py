# Copyright (C) 2014-2017 New York University
# This file is part of ReproZip which is released under the Revised BSD License
# See file LICENSE for full license details.

"""Contexec plugin for reprounzip."""

# prepare for Python 3
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
from reprounzip.unpackers.common import target_must_exist, add_environment_options


def containerexec_create(args):
    """Unpacks the experiment in a folder.

    Only the files that are not part of a package are copied (unless they are
    missing from the system and were packed).

    In addition, input files are put in a tar.gz (so they can be put back after
    an upload) and the configuration file is extracted.
    """
    print('debug: directory_create')


@target_must_exist
def containerexec_upload(args):
    """Replaces an input file in the sandbox.
    """
    print('debug: containerexec_upload')


@target_must_exist
def containerexec_run(args):
    """Runs the experiment in the sandbox.
    """
    print('debug: containerexec_run')


@target_must_exist
def containerexec_download(args):
    """Gets an output file out of the sandbox.
    """
    print('debug: containerexec_download')


@target_must_exist
def containerexec_destroy(args):
    """Destroys both the sandbox and directory through Containerexec.
    """
    print('debug: containerexec_destroy')


def setup(parser, **kwargs):
    """Unpacks the files in a directory and runs the experiment in an isolated environment

    setup           creates the directory (needs the pack filename)
    upload          replaces input files in the directory
                    (without arguments, lists input files)
    run             runs the experiment in the isolated environment
    download        gets output files from the machine
                    (without arguments, lists output files)
    destroy         removes the unpacked directory

    For example:

        $ reprounzip containerexec setup mypackage.rpz somepath
        $ reprounzip containerexec run somepath/
        $ reprounzip containerexec download somepath/ results:/home/user/results.txt
        $ reprounzip containerexec destroy somepath

    Upload specifications are either:
      :input_id             restores the original input file from the pack
      filename:input_id     replaces the input file with the specified local
                            file

    Download specifications are either:
      output_id:            print the output file to stdout
      output_id:filename    extracts the output file to the corresponding local
                            path
    """
    subparsers = parser.add_subparsers(title="actions",
                                       metavar='', help=argparse.SUPPRESS)

    def add_opt_general(opts):
        opts.add_argument('target', nargs=1, help="Experiment directory")

    # setup
    parser_setup = subparsers.add_parser('setup')
    parser_setup.add_argument('pack', nargs=1, help="Pack to extract")
    # Note: add_opt_general is called later so that 'pack' is before 'target'
    add_opt_general(parser_setup)
    parser_setup.set_defaults(func=containerexec_create)

    # upload
    parser_upload = subparsers.add_parser('upload')
    add_opt_general(parser_upload)
    parser_upload.add_argument('file', nargs=argparse.ZERO_OR_MORE,
                               help="<path>:<input_file_name")
    parser_upload.set_defaults(func=containerexec_upload)

    # run
    parser_run = subparsers.add_parser('run')
    add_opt_general(parser_run)
    parser_run.add_argument('run', default=None, nargs=argparse.OPTIONAL)
    parser_run.add_argument('--cmdline', nargs=argparse.REMAINDER,
                            help="Command line to run")
    add_environment_options(parser_run)
    parser_run.set_defaults(func=containerexec_run)

    # download
    parser_download = subparsers.add_parser('download')
    add_opt_general(parser_download)
    parser_download.add_argument('file', nargs=argparse.ZERO_OR_MORE,
                                 help="<output_file_name>[:<path>]")
    parser_download.add_argument('--all', action='store_true',
                                 help="Download all output files to the "
                                      "current directory")
    parser_download.set_defaults(func=containerexec_download)

    # destroy
    parser_destroy = subparsers.add_parser('destroy')
    add_opt_general(parser_destroy)
    parser_destroy.set_defaults(func=containerexec_destroy)
