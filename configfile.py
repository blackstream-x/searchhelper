#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
configfile.py

handle YAML and JSON configuration files for searchhelper
"""


import argparse
import json
import os
import sys

try:
    import yaml
    YAML_SUPPORTED = True
except ImportError:
    YAML_SUPPORTED = False
#

#
# Constants
#

SCRIPT_NAME = 'configfile'
VERSION = '0.8.4-alpha'
LICENSE = 'LICENSE.txt'

JSON_EXTENSION = '.json'
YAML_EXTENSION = '.yaml'

MODE_READ = 'rt'
MODE_WRITE = 'wt'
ENCODING = 'utf-8'


#
# Functions
#


def load_yaml(file_name):
    """Load a YAML file"""
    if YAML_SUPPORTED:
        with open(file_name,
                  mode=MODE_READ,
                  encoding=ENCODING) as input_file:
            return yaml.safe_load(input_file)
        #
    else:
        raise NotImplementedError
    #


def dump_to_yaml(data, file_name):
    """Dump data to a YAML file"""
    if YAML_SUPPORTED:
        with open(file_name,
                  mode=MODE_WRITE,
                  encoding=ENCODING) as output_file:
            yaml.dump(data, output_file, default_flow_style=False)
        #
    else:
        raise NotImplementedError
    #


def load_json(file_name):
    """Load a JSON file"""
    with open(file_name,
              mode=MODE_READ,
              encoding=ENCODING) as input_file:
        return json.load(input_file)
    #


def dump_to_json(data, file_name):
    """Dump data to a JSON file"""
    with open(file_name,
              mode=MODE_WRITE,
              encoding=ENCODING) as output_file:
        json.dump(data, output_file, indent=2)
    #


def load_file(file_name):
    """Load a YAML or JSON file,
    dispatch to the matching load function
    """
    file_stub, file_extension = os.path.splitext(file_name)
    if file_extension in (YAML_EXTENSION, '.yml'):
        return load_yaml(file_name)
    #
    if file_extension == JSON_EXTENSION:
        return load_json(file_name)
    #
    raise ValueError(
        'File extension {0!r} not supported'.format(file_extension))


def dump_to_file(data, file_name):
    """Dump data to a YAML or JSON file,
    dispatch to the matching dump function
    """
    file_stub, file_extension = os.path.splitext(file_name)
    if file_extension in (YAML_EXTENSION, '.yml'):
        dump_to_yaml(data, file_name)
    elif file_extension == JSON_EXTENSION:
        dump_to_json(data, file_name)
    else:
        raise ValueError(
            'File extension {0!r} not supported'.format(file_extension))
    #


def compare_data(first_file_name, second_file_name):
    """Compare data in the files by dumping both to a JSON string
    and comparing the strings
    """
    first_json_representation = json.dumps(
        load_file(first_file_name),
        indent=2)
    second_json_representation = json.dumps(
        load_file(second_file_name),
        indent=2)
    return first_json_representation == second_json_representation


def __get_arguments():
    """Parse command line arguments"""
    # TODO: This does not match anymore
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
    # TODO
    #
    return 0


if __name__ == '__main__':
    sys.exit(main(__get_arguments()))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
