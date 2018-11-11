#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-

import sklearn as sk
from os.path import join
import pandas as pd
import umap
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def parse_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description='Decompose it!')
    parser.add_argument(
        '--table',
        type=FileType('r'),
        required=True,
        help='Column names and types in TSV format'
    )
    parser.add_argument(
        '--out_file',
        type=FileType('w'),
        required=True,
        help='TSV format'
    )
    parser.add_argument(
        '--image_prefix',
        required=True,
        help='Image file prefix'
    )
    return parser.parse_args()

def plot_projection(projected, target, img_prefix):
    plt.scatter(projected[:, 0], projected[:, 1],
            c=target, edgecolor='none', alpha=0.5,
            cmap=plt.cm.get_cmap('nipy_spectral', 10))
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    plt.colorbar();
    plt.savefig(img_prefix+'.png')
    plt.clf()

def pca_stuff(data, target, img_prefix):
    pca = sk.decomposition.PCA(2)
    projected = pca.fit_transform(data)
    plot_projection(projected, target, img_prefix+'.pca')
 
def umap_stuff(data, target, img_prefix):
    embedding = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='correlation')
    projected = embedding.fit_transform(data)
    plot_projection(projected, target, img_prefix+'.umap')

def main():
    args = parse_args()
    #data = pd.DataFrame( args.in_file, sep='\t', header=0 )
    from sklearn.datasets import load_digits
    digits = load_digits()
    data = digits.data
    target = digits.target

    pca_stuff(data, target, args.image_prefix) 
    umap_stuff(data, target, args.image_prefix)

if __name__ == '__main__':
    main()
