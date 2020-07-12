import pandas as pd
import click


"""
python format_signature_table.py --synapse sigProfiler_SBS_signatures_2019_05_22.csv --deconstruct sigProfiler_SBS_deconstructsigs.tsv
"""


@click.command()
@click.option('--synapse', type=click.Path())
@click.option('--deconstruct', type=click.Path())
def convert(synapse, deconstruct):
    df = pd.read_csv(synapse, sep=',')
    df['encoding'] = df.apply(lambda x: x['SubType'][0] + '[' + x['Type'] + ']' + x['SubType'][-1], axis=1)
    contexts = list(df['encoding'].values)
    df.drop(columns=['Type', 'SubType', 'encoding'], inplace=True)
    df = df.transpose()
    df.columns = contexts
    df.to_csv(deconstruct, sep='\t')


if __name__ == '__main__':
    convert()