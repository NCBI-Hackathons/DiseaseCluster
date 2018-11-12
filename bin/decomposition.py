#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# VIM: let g:pyindent_open_paren=2 g:pyindent_continue=2
# -*- coding: utf-8 -*-

import sklearn as sk
from os.path import join
import pandas as pd
import umap
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns; sns.set()
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib.colors import ListedColormap

def parse_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description='Decompose it!')
    parser.add_argument(
        '--expression',
        required=True,
        help='Column names and types in TSV format'
    )
    parser.add_argument(
        '--project',
        required=True,
        help='File with tissue assignments'
    )
    parser.add_argument(
        '--tissue_map',
        type=FileType('r'),
        required=True,
        help='File with tissue assignments'
    )
    parser.add_argument(
        '--image_prefix',
        required=True,
        help='Image file prefix'
    )
    parser.add_argument(
        '--threeD',
        action='store_true',
        default=False,
        help='Whether to plot 3 components'
    )
    parser.add_argument(
        '--color',
        choices=['tissue', 'project'],
        default='tissue',
        help='How shall we color?'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--umap_nn',
        type=int,
        help='Number of nearest neighbors for umap'
    )
    group.add_argument(
        '--pca',
        help='Which PCA type to use'
    )

    return parser.parse_args()

def plot_3d(projected, img_prefix):
    fig = plt.figure()
    fig.set_size_inches(10,6)
    ax = fig.add_subplot(111, projection='3d')
    labels = list(set(projected['color']))
    colors = sns.color_palette("husl", len(labels))
    color_dict = dict(zip(labels, colors))
    my_cmap = ListedColormap(colors)
    color_column = [ color_dict[label] for label in projected['color'] ]
    ax.scatter(   
            projected['comp 0'],
            projected['comp 1'],
            projected['comp 2'],
            c = color_column,
            cmap = my_cmap
    )       
    #cbar = plt.colorbar(ax1)
    cax, _ = mpl.colorbar.make_axes(ax)
    cbar = mpl.colorbar.ColorbarBase(cax, cmap=my_cmap )
    cbar.set_ticks(list(range(len(labels))))
    cbar.set_ticklabels(labels)
    ax.set_zlabel('component 3')
    return ax

def plot_projection(projected, img_prefix, threeD):
    if threeD:
        ax = plot_3d(projected, img_prefix)
    else:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.scatterplot(ax=ax, data = projected, x = 'comp 0', y = 'comp 1', hue='color')
    ax.set_xlabel('component 1')
    ax.set_ylabel('component 2')
    plt.savefig(img_prefix+'.png', dpi=300)
    plt.clf()

def plot_explained_variance(explained_variance, img_prefix):
    plt.scatter(range(len(explained_variance)), explained_variance, edgecolor='none', alpha=0.5)
    plt.xlabel('variance')
    plt.ylabel('component')
    plt.savefig(img_prefix+'.explained_var.png')
    plt.clf()

def pca_stuff(data, outname, pca_name, threeD, color):
    decomps = {
        'PCA':sk.decomposition.PCA(),
        'KernelPCA':sk.decomposition.KernelPCA(),
        'SparsePCA':sk.decomposition.SparsePCA()
    }
    pca = decomps[pca_name]
    projected = pca.fit_transform(data)
    columns=['comp '+str(i) for i in range(projected.shape[1])]
    df = pd.DataFrame(data=projected, columns=columns)
    df['color']=color
    plot_projection(df, outname, threeD)
    plot_explained_variance(pca.explained_variance_ratio_, outname)
    return df
 
def umap_stuff(data, outname, nn, threeD, color):
    ncomps = 3 if threeD else 2
    embedding = umap.UMAP(n_neighbors=nn, min_dist=0.0, metric='correlation', n_components=ncomps)
    projected = embedding.fit_transform(data)
    columns=['comp '+str(i) for i in range(projected.shape[1])]
    df = pd.DataFrame(data=projected, columns=columns)
    df['color']=color
    plot_projection(df, outname, threeD)
    return df

def parse_projects(project_fh):
    data = pd.read_table( project_fh, index_col=0 )
    return dict(zip(data['Sample ID'], data['Project ID'])) 

def parse_tissue_map(tissue_fh):
    tissue_map = {}
    for t in tissue_fh:
        k,sep,v = t.strip().partition('\t')
        tissue_map[k]=v
    return tissue_map

def main():
    args = parse_args()
    data = pd.read_table( args.expression, index_col=0 ).transpose()
    data.apply(np.log1p)
    projects = parse_projects(args.project)
    tissues = parse_tissue_map(args.tissue_map)
    projects = [projects[i] for i in data.index]
    tissues = [tissues[i] for i in projects]
    colors = tissues if args.color == 'tissue' else projects
    if args.pca:
        outname='.'.join([args.image_prefix,args.pca])
        df = pca_stuff(data, outname, args.pca, args.threeD, colors) 
    else:
        outname='.'.join([args.image_prefix,'umap',str(args.umap_nn)])
        df = umap_stuff(data, outname, args.umap_nn, args.threeD, colors)
    df = df.drop(columns=['color'])
    df['project'] = projects
    df['tissue'] = tissues
    df.to_csv(outname+'.tsv', sep='\t')

if __name__ == '__main__':
    main()
