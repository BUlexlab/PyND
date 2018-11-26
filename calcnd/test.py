import pandas as pd
import os
import importlib


import neighborhood_density_calc as ndc
importlib.reload(ndc)

input_dir = "~/Downloads"
a = pd.read_csv(os.path.join(input_dir, "signdata (28).csv"))
a = a.sample(n=500)
result = ndc.MinimalPairND(a,
                           ["SignType 2.0", "MinorLocation 2.0", "SecondMinorLocation",
                            "Movement 2.0", "Contact", "SelectedFingers 2.0",
                            "Flexion 2.0", "FlexionChange", "Spread", "SpreadChange"],
                           allowed_misses=9, allowed_matches=10, mirror_neighbors=True)

# with pd.option_context("display.max_columns", 6):
#     print(result['neighbors'])


# with pd.option_context("display.max_columns", 6):
#     print(result['neighbors'].loc[lambda df: (df.target == '1_dollar') |
#                                   (df.neighbor == '1_dollar'), :])

pd.set_option('display.max_columns', None)
