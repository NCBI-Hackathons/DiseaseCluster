import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

tcga_path = './data/tcga/'
sample_sheet = pd.read_table(tcga_path + 'metadata/full_transcriptome_sample_sheet.txt')

#Function for removing decimals off ENSG gene names
cut_decimal  = np.vectorize(lambda x : x.split('.')[0])

def prep_single_sample_metadata(sample_metadata):
    """
    Function For Parsing Single Row in Metadata
    """
    fileID = sample_metadata['File ID']
    fileName = sample_metadata['File Name']
    caseID = sample_metadata['Sample ID']
    return {'directory': fileID, 'fileName':fileName, 'barcode':caseID}


def parse_single_sample(sample_dict, protein_coding_genes):
    """
    Function for Reading in single sample and parsing it
    """
    data_path = tcga_path + '/transcriptomics/'
    sample_data = pd.read_table(data_path + sample_dict['directory'] + '/' + sample_dict['fileName'], header=None, index_col=0)[1]
    
    sample_data.index = cut_decimal(sample_data.index)
    
    sample_data /= sample_data.sum()
    sample_data *= 10e6
    
    sample_data.name = sample_dict['barcode']
    sample_data = sample_data[protein_coding_genes].dropna()
    
    return sample_data


#Read in protein coding gene list
protein_coding_genes = np.genfromtxt('./data/protein_coding_genes.txt',dtype=str)
protein_coding_genes = cut_decimal(protein_coding_genes)

df = pd.DataFrame()
for row in sample_sheet.index:
    sample_dict = prep_single_sample_metadata(sample_sheet.loc[row,:])
    df[sample_dict['barcode']] = parse_single_sample(sample_dict, protein_coding_genes)

df.to_csv('./data/tcga/merged_tcga_data.txt.gz', sep='\t', compression='gzip')


