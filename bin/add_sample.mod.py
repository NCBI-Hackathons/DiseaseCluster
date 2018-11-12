import pandas as pd
import numpy as np
import scipy.spatial as spatial
import scipy.stats as stats

def parse_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description='Find overlap between new dataset and reference')
    parser.add_argument(
        '--reference',
        required=True,
        help='TCGA reference expression dataset'
    )
    parser.add_argument(
        '--dataset',
        required=True,
        help='New dataset compared with TCGA'
    )
    parser.add_argument(
        '--kn',
        required=False,
        type=int,
        default=15,
        help='Number of nearest neighbors, default is 15'
    )

    return parser.parse_args()

def read_new(fn, reference_data):
    
    #Read new data in genes as rows and samples as columns
    df = pd.read_table(fn, index_col=0)
    
    assert df.index.intersection(reference_data.index).shape[0] != 0, \
        'Genes don\'t overlap between reference and new dataset, can\'t compare'
    return df
    
    
def find_nearest(reference_data,new_data, k = 5):
    """
    find k nearest neighbors to new sample data
    """
    
    assert k > 0, 'k needs to be greater than 0'
    assert type(k) == int, 'k needs to be an integer'
    
    if new_data.ndim == 1: #Need new data to be in 2 dimensions to do distance comparison
        print('test')
        new_data = new.values[:,np.newaxis]
    
    rank_distance = stats.rankdata(spatial.distance.cdist(reference_data.values.T, new_data.T))
    return pd.Series(rank_distance <= k, index=reference_data.columns)


## test code

#Full TCGA dataset, would be smart to put in a faster file format
#reference_data = pd.read_table('../data/tcga/merged_tcga_data.txt.gz', index_col=0)
#New FN sholud be inputed from somewhere else....
#new_data = read_new(new_fn)
#k_nearest = find_nearest(reference_data, new_data)



def main():
    args = parse_args()
    reference = args.reference
    dataset = args.dataset
    kn = args.kn
    # parse reference
    reference_data = pd.read_table(reference, index_col = 0)
    # parse new dataset
    new_data = read_new(dataset, reference_data)
    # calculate k-nearest
    k_nearest = find_nearest(reference_data, new_data, kn)
    return(k_nearest)

if __name__ == '__main__':
    main()
