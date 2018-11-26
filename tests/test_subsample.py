import os
import pandas as pd
import tempfile

from calcnd.utils import subsample

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_subsample():
    with tempfile.TemporaryDirectory() as tmpdir:
        subsample(os.path.join(THIS_DIR, "test_data", "signdata (33).csv"),
                  os.path.join(tmpdir, "out.csv"), 100)
        d = pd.read_csv(os.path.join(tmpdir, "out.csv"))
    n_rows = len(d.index)
    assert n_rows == 100
