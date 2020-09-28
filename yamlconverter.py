#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
yamlconverter.py

Convert YAML files to JSON and vice versa
"""


import argparse
import json
import os
import sys
import yaml

#
# Constants
#

SCRIPT_NAME = 'YAML converter'
VERSION = '1.0'
LICENSE = 'LICENSE.txt'

JSON_EXTENSION = '.json'
YAML_EXTENSION = '.yaml'


#
# Functions
#


def __get_arguments():
    """Parse command line arguments"""
    argument_parser = argparse.ArgumentParser(
        description='Convert YAML to JSON files and vice versa')
    argument_parser.add_argument('-f', '--force-overwrite',
                                 action='store_true',
                                 help='Overwrite existing files')
    argument_parser.add_argument('source_file',
                                 help='The file to convert')
    return argument_parser.parse_args()


def main(arguments):
    """Main script function"""
    file_stub, file_extension = os.path.splitext(arguments.source_file)
    if file_extension in (YAML_EXTENSION, '.yml'):
        target_file_extension = JSON_EXTENSION
    elif file_extension == JSON_EXTENSION:
        target_file_extension = YAML_EXTENSION
    else:
        raise ValueError(
            'File extension {0!r} not supported'.format(file_extension))
    #
    target_file_name = file_stub + target_file_extension
    if os.path.exists(target_file_name) and not arguments.force_overwrite:
        raise ValueError(
            'Target file {0!r} exists, use -f to overwrite'.format(
                target_file_name))
    #
    if target_file_extension == JSON_EXTENSION:
        # Load YAML, write JSON
        with open(arguments.source_file,
                  mode='rt',
                  encoding='utf-8') as input_file:
            data = yaml.safe_load(input_file)
        #
        with open(target_file_name,
                  mode='wt',
                  encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=2)
        #
    elif target_file_extension == YAML_EXTENSION:
        # Load YAML, write JSON
        with open(arguments.source_file,
                  mode='rt',
                  encoding='utf-8') as input_file:
            data = json.load(input_file)
        #
        with open(target_file_name,
                  mode='wt',
                  encoding='utf-8') as output_file:
            yaml.dump(data, output_file, default_flow_style=False)
        #
    #
    return 0


if __name__ == '__main__':
    sys.exit(main(__get_arguments()))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
