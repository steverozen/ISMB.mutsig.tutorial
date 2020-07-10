import click
import pandas as pd

import matplotlib.pyplot as plt
from seaborn import clustermap, light_palette

import scipy.cluster.hierarchy as hierarchy
from scipy.spatial.distance import pdist
from scipy.stats import entropy

"""
Python dependencies with conda:
conda create -n signatures-env python=3.7 pandas click matplotlib seaborn scipy
conda activate signatures-env
"""

sig_labels = ['SBS1', 'SBS2', 'SBS5', 'SBS7a', 'SBS7b', 'SBS7c', 'SBS7d', 'SBS13', 'SBS17a', 'SBS17b', 'SBS38']


def js(x, y):
    """Jensen-Shannon divergence
    """

    m = 0.5 * (x + y)
    return 0.5 * (entropy(x, m) + entropy(y, m))


@click.command()
@click.option('--input', type=click.Path(), help='path to weights file')
@click.option('--metric', type=str)
@click.option('--output', type=click.Path(), help='path to image output')
def clustering(input, metric, output):

    weights = pd.read_csv(input, sep='\t')
    weights['burden_rank'] = weights['mutation_count'].rank(method='max')
    color_list = light_palette('orangered', len(weights)).as_hex()
    colors = [color_list[int(i - 1)] for i in weights['burden_rank']]

    weights = weights[sig_labels]
    X = weights[[col for col in weights.columns if col.startswith('SBS')]].values

    if metric == 'cosine':
        Y = pdist(X, metric=js)
    elif metric == 'jensen-shannon':
        Y = pdist(X, metric='cosine')

    linkage = hierarchy.linkage(Y, method='ward')

    g = clustermap(X.T, col_linkage=linkage, row_cluster=False, figsize=(20, 10),
                   yticklabels=sig_labels,
                   xticklabels=False,
                   col_colors=colors,
                   cmap="YlGnBu")

    g.ax_heatmap.set_ylabel('Signatures')

    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
    plt.title(metric)
    plt.savefig(output, dpi=300, bbox_inches='tight')


if __name__ == '__main__':

    """
    Within conda environment, run this command-line:
    python clustering.py --input data/melanoma_weights.tsv \
                         --metric jensen-shannon \
                         --output data/cluster-samples-jensen-shannon.png
    """

    clustering()
