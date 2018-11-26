import os

import calc_nd as cnd


THIS_DIR = os.path.dirname(os.path.realpath(__file__))


input = os.path.join(THIS_DIR, "..", "data", "signdata (33).csv")
outputdir = "~/naomi/output"
allowed_misses = 3
allowed_matches = 10
mirror_neighbors = True

features = ["SignType 2.0", "MinorLocation 2.0", "SecondMinorLocation",
            "Movement 2.0", "Contact", "SelectedFingers 2.0",
            "Flexion 2.0", "FlexionChange", "Spread", "SpreadChange"]

cnd.main(input=input, outputdir=outputdir, allowedmisses=allowed_misses,
         allowedmatches=allowed_matches, deduplicated=not mirror_neighbors,
         features=features)
