import pandas as pd
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s - %(asctime)-14s %(levelname)-8s: %(message)s',
                              "%m-%d %H:%M:%S")

ch.setFormatter(formatter)

logger.handlers = []  # in case module is reload()'ed, start with no handlers
logger.addHandler(ch)


def MinimalPairND(data, features, allowed_misses=0, allowed_matches=None,
                  mirror_neighbors=True):
    """Calculate minimal pair neighbors.

    Args:
        data (pandas.DataFrame): a dataframe containing a column
            called EntryID, and columns with names matching the elements of
            'features'
        features (list of str): a character vector containing the column names in
             "data" over which to calculate neighborhood densities
        allowed_misses (int): an integer indicating how many features
             are allowed to differ between the target word and the
             candidate word while still considering the candidate a
             neighbor
        allowed_matches (int): (default:length(features)) an integer
            indicating the maximum number of features that are allowed to
            match between the target word and the candidate word while still
            considering the candidate a neighbor
        mirror_neighbors (bool): (default: True) If True, Mirror the neighbors
            DataFrame such that every A-B pair appears as both
            A(target)-B(neighbor) and B(target)-A(neighbor). If False, the pair
            will appear only once in neighbors

    Returns:
        dict containing elements:
        nd (pandas.DataFrame: the input DataFrame with an additional column,
            'Neighborhood Density', the computed neighborhood density
            for each row in the input dataframe

        neighbors (pandas.DataFrame): a data.frame containing the found
            neighbors (data frame has four columns, "target", "neighbor",
            "num.matched.features", and "matched.features")

    """
    start_time = time.monotonic()
    if allowed_misses > len(features)-1 or allowed_misses < 0:
        raise ValueError("allowed.misses must be less than or equal to"
                         + " (length(features) - 1),"
                         + " and must not be less than 0")

    if allowed_matches is None:
        allowed_matches = len(features)
    elif allowed_matches < 1 or allowed_matches > len(features):
        raise ValueError("allowed.matches must be greater than one"
                         + "and cannot exceed length(features)")

    missing_features = [
        x for x in features if x not in list(data.columns.values)]
    if missing_features:
        msg = "Feature(s) {} not in DataFrame data".format(missing_features)
        raise ValueError(msg)

    logger.debug("len(data.index): %d" % len(data.index))
    logger.debug("len(features): %d" % len(features))

    logger.debug("features: %s " % features)

    nbr_target = []
    nbr_neighbor = []
    nbr_num_match_features = []
    nbr_match_features = []
    out_df = data.copy()
    out_df['Neighborhood Density'] = 0

    # outer loop will be stepping through words (source word)
    it_start_time = time.monotonic()
    it_start_iter = 0
    for i in range(0, len(data.index)):
        num_neighbors = 0
        msg = 'starting word {} of {}, "{}"'
        msg = msg.format(i+1, len(data.index),
                         data.iloc[i, data.columns.get_loc("EntryID")])
        if i == 0:
            logger.info(msg)
        elif (i+1) % 10 == 0:
            frac_complete = i/len(data.index)
            et = time.monotonic() - it_start_time
            try:
                rate = (i - it_start_iter)/et
            except ZeroDivisionError:
                rate = float("inf")
            etc = (len(data.index)-i) * 1/rate

            # hrs = math.floor(etc/60**2)
            # mins = math.floor((etc - hrs*60**2)/60)
            # secs = etc - (hrs * 60**2) - (mins * 60)

            # msg2 = (".. {complete:.1%} complete, {rate:.2f} words/sec."
            #         + " Est. {hrs}:{mins:02.0f}:{secs:02.0f}"
            #         + " (H:MM:SS) remaining.")
            # msg2 = msg2.format(complete=frac_complete, rate=rate,
            #                    hrs=hrs, mins=mins, secs=secs)

            msg2 = (".. {complete:.1%} complete, {rate:.2f} words/sec."
                    + " Est. {etc}"
                    + " (H:MM:SS.ms) remaining.")
            msg2 = msg2.format(complete=frac_complete, rate=rate,
                               etc=formatHMS(etc))
            logger.info(msg2)
            logger.info(msg)
            it_start_time = time.monotonic()
            it_start_iter = i
        else:
            logger.debug(msg)
        # second level loop will also be stepping through words (candidate word)
        # for j in range(0, len(data.index)):
        for j in range(i, len(data.index)):
            if (i != j):  # TODO: change starting index to i+1 and remove this conditional
                matches = 0
                matched_features = ""
                # third-level loop will step through features,
                # counting the number of features of the candidate
                # word that match the source word. If the matches
                # equal or exceed (len(features) - allowed_misses),
                # put the candidate word into the list of neighbors
                for k in range(0, len(features)):
                    if (pd.notna(data.iloc[i, data.columns.get_loc(features[k])]) and
                        pd.notna(data.iloc[j, data.columns.get_loc(features[k])])):
                        if (data.iloc[i, data.columns.get_loc(features[k])] ==
                                data.iloc[j, data.columns.get_loc(features[k])]):
                            msg = "Matched {source} to {target} on feature {feature}"
                            msg = msg.format(source=data.iloc[i, data.columns.get_loc("EntryID")],
                                             target=data.iloc[j, data.columns.get_loc("EntryID")],
                                             feature=features[k])
                            logger.debug(msg)
                            matches = matches + 1
                            if matched_features == "":
                                matched_features = features[k]
                            else:
                                matched_features = ", ".join([matched_features,
                                                              features[k]])
                if (matches >= (len(features) - allowed_misses) and
                        matches <= allowed_matches):
                    logger.debug("adding match to neighbors")
                    nbr_target.append(data.iloc[i, data.columns.get_loc("EntryID")])
                    nbr_neighbor.append(data.iloc[j, data.columns.get_loc("EntryID")])
                    nbr_num_match_features.append(matches)
                    nbr_match_features.append(matched_features)
                    logger.debug("incrementing neighborhood density"
                                 + "for both members of the pair")
                    out_df.iloc[i, out_df.columns.get_loc("Neighborhood Density")] += 1
                    out_df.iloc[j, out_df.columns.get_loc("Neighborhood Density")] += 1
        # back to i loop
    data_dict = {'target': nbr_target,
                 'neighbor': nbr_neighbor,
                 'num_matched_features': nbr_num_match_features,
                 'matched_features': nbr_match_features}

    neighbors = pd.DataFrame(data_dict)
    elapsed_time = time.monotonic() - start_time
    msg = "completed {words} words in {et} (H:MM:SS.ms) ({rate:.2f} word/sec)".format(
        words=len(data.index),
        et=formatHMS(elapsed_time),
        rate=len(data.index)/elapsed_time)
    logger.info(msg)

    if mirror_neighbors:
        logger.info("mirroring neighbors DataFrame...")
        neighbors = mirrorNeighbors(neighbors)
        logger.info("...done.")

    return({'nd': out_df,
            'neighbors': neighbors})


def listNeighbors(df, target):
    res = df.loc[lambda d: (d.target == target) | (d.neighbor == target), :]
    with pd.option_context("display.max_columns", 6):
        print(res)
    return(None)


def mirrorNeighbors(df):
    """Mirrors a neighbors DataFrame from MinimalPairND

    Mirror the neighbors DataFrame such that every A-B pair appears as
    both A(target)-B(neighbor) and B(target)-A(neighbor)

    Args:
        df (pandas.DataFrame): a neighbors DataFrame from MinimalPairND()

    Returns:
        A pandas.DataFrame with twice as many rows as the input df, 
        sorted by target, then neighbor
    """
    fd = df.copy()

    fd.loc[:, 'target'] = df.loc[:, 'neighbor']
    fd.loc[:, 'neighbor'] = df.loc[:, 'target']

    result = pd.concat([df, fd])
    result = result.sort_values(by=['target', 'neighbor'])
    return(result)


def formatHMS(s):
    """formats a duration in seconds into H:MM:SS.ms
    """
    hours, remainder = divmod(s, 60**2)
    minutes, seconds = divmod(remainder, 60)
    return("{:.0f}:{:02.0f}:{:05.2f}".format(hours, minutes, seconds))
