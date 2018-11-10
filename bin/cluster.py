#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-

import sklearn
from os.path import join

def parse_fpkm(directory, file_name):
    for line in open(join(directory,filename)):
        tid, expression = line.strip().partition('\t')

def parse_manifest(gdc_manifest):
    from csv import DictReader
    for row in DictReader(gdc_manifest):
        directory, filename = ...
        ids_expression = parse_fpkm()

def filter_expression_data(data):
    pass

def cluster(data):

def parse_args():
    import argparse, FileType
    parser.add_argument(
        '--gdc_manifest',
        type=FileType('r'),
        required=True,
        help='Column names and types in TSV format'
    )
    parser.add_argument(
        '--out_file',
        type=FileType('w'),
        required=True,
        help='Column names and types in TSV format'
    )
    return parser.parse()

def main():
    args = parse_args()
    data = parse(args.gdc_manifest)
    data = filter_expression_data(data)
    clusters = cluster(data)

if __name__ == '__main__':
    main()
