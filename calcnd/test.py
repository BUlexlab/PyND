import os

import calc_nd as cnd


THIS_DIR = os.path.dirname(os.path.realpath(__file__))


input = os.path.join(THIS_DIR, "..", "data", "signdata (33).csv")
outputdir = "~/naomi/output"
allowed_misses = 0
allowed_matches = None
mirror_neighbors = True

outputname = ["NotHandshapeFeatures", "HandshapeFeatures"]
features = [["SignType 2.0",
             "MajorLocation 2.0",
             "MinorLocation 2.0",
             "SecondMinorLocation",
             "Movement 2.0",
             "Contact"],
            ["SelectedFingers 2.0",
             "Flexion 2.0",
             "FlexionChange",
             "Spread",
             "SpreadChange"]
            ]

for name, feat in zip(outputname, features):
    cnd.main(input=input, outputdir=outputdir, outputname=name,
             allowedmisses=allowed_misses, allowedmatches=allowed_matches,
             deduplicated=not mirror_neighbors, features=feat)
