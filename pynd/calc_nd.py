import pandas as pd
import logging
import os
import plac

import neighborhood_density_calc as ndc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(asctime)-14s %(levelname)-8s: %(message)s',
                              "%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.handlers = []
logger.addHandler(ch)


@plac.annotations(
    features=('a character vector containing the column names'
              ' in "data" over which to calculate neighborhood'
              ' densities', 'positional'),
    input=('path to the input .csv file', 'positional'),
    outputdir=('directory into which to place results files', 'option'),
    outputname=('base name for results .csv files; files will be named'
                ' [outputname]-neighbors.csv and [outputname]-nd.csv',
                'option'),
    allowedmisses=('an integer indicating how many features'
                   ' are allowed to differ between the target word and the'
                   ' candidate word while still considering the candidate a'
                   ' neighbor', 'option', None, int),
    allowedmatches=('(default:length(features)) an integer indicating the'
                    ' maximum number of features that are allowed to'
                    ' match between the target word and the candidate'
                    ' word while still considering the candidate a neighbor',
                    'option', None, int),
    deduplicated=('do not duplicate target/neighbor pairs  A->B B->A', 'flag'),
    sample=('if supplied, length of a random subsample of the input dataframe'
            ' (to speed things up for testing purposes)', 'option',
            None, int))
def main(features, input, outputdir="~/Documents", outputname='result',
         allowedmisses=0, allowedmatches=None, deduplicated=False,
         sample=None):
    """Calculates minimal pair neighbors and saves results as csv files

    A convenience wrapper to :py:func:`pynd.neighborhood_density_calc.MinimalPairND`

    Args:
        features (list of str): a character vector containing the column names
            in "data" over which to calculate neighborhood densities
        input (str): path to the input .csv file
        outputdir (str): directory into which to write results .csv files.
            Will be created if it does not exist.
        outputname (str): base name for results .csv files; files will be
            named [outputname]-neighbors.csv and [outputname]-nd.csv
        allowedmisses (int): an integer indicating how many features
            are allowed to differ between the target word and the candidate
            word while still considering the candidate a neighbor
        allowedmatches (int): (default:length(features)) an integer indicating
            the maximum number of features that are allowed to match between
            the target word and the candidate word while still considering
            the candidate a neighbor
        deduplicated (bool): do not duplicate target/neighbor pairs  A->B B->A
        sample (int): if supplied, length of a random subsample of the input
            dataframe (to speed things up for testing purposes)
    
    """
    features = list(features)
    if not allowedmatches:
        allowedmatches = len(features)

    msg = ('input: {inp} outputdir: {outdir}, outputname: {outname},'
           + ' features: {feat}, allowedmisses: {miss}'
           + ' allowedmatches: {match}, deduplicated: {dedup}, sample : {samp}')
    msg = msg.format(inp=input, outdir=outputdir, outname=outputname,
                     feat=features, miss=allowedmisses,
                     match=allowedmatches, dedup=deduplicated, samp=sample)
    logger.info(msg)

    a = pd.read_csv(input)
    if sample:
        a = a.sample(sample)
    result = ndc.MinimalPairND(data=a, features=features, allowed_misses=allowedmisses,
                               allowed_matches=allowedmatches,
                               mirror_neighbors=not deduplicated)
    neighbor_out_path = os.path.join(outputdir, outputname + "-neighbors.csv")
    result['neighbors'].to_csv(neighbor_out_path, na_rep='NA', index=False)
    logger.info("Wrote file %s" % neighbor_out_path)

    nd_out_path = os.path.join(outputdir, outputname + "-nd.csv")
    result['nd'].to_csv(nd_out_path, na_rep='NA', index=False)
    logger.info("wrote file %s" % nd_out_path)

    return(None)


if __name__ == '__main__':
    import plac
    plac.call(main)
