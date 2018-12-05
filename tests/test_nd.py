import os
import pandas as pd
import tempfile

from pynd.neighborhood_density_calc_EntryID import MinimalPairND

THIS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__))
    )


def test_nd():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    res = MinimalPairND(data=input,
                        features=["SignType 2.0", "MinorLocation 2.0",
                                  "SecondMinorLocation", "Movement 2.0",
                                  "Contact", "SelectedFingers 2.0",
                                  "Flexion 2.0", "FlexionChange",
                                  "Spread", "SpreadChange"],
                        allowed_misses=9, allowed_matches=10, mirror_neighbors=True)
    neighbor_out_path = os.path.join(THIS_DIR, "test_output", "result-neighbors.csv")
    res['neighbors'].to_csv(neighbor_out_path, na_rep='NA', index=False)

    nd_out_path = os.path.join(THIS_DIR, "test_output", "result-nd.csv")
    res['nd'].to_csv(nd_out_path, na_rep='NA', index=False)

def test_nd_all_alpha():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "all_alpha_input.csv"))

    for misses in range(1, 10):
        res = MinimalPairND(data=input,
                            features=["feature-01", "feature-02", "feature-03",
                                      "feature-04", "feature-05", "feature-06",
                                      "feature-07", "feature-08", "feature-09",
                                      "feature-10"],
                            allowed_misses=misses, allowed_matches=10, mirror_neighbors=True)
        filename = "all_alpha_{}_miss-{}.csv"
        neighbor_out_path = os.path.join(THIS_DIR, "test_output", filename.format(misses, 'neighbors'))
        res['neighbors'].to_csv(neighbor_out_path, na_rep='NA', index=False)

        nd_out_path = os.path.join(THIS_DIR, "test_output", filename.format(misses, 'nd'))
        res['nd'].to_csv(nd_out_path, na_rep='NA', index=False)

        test_neighbor = pd.read_csv(neighbor_out_path)
        ref_neighbor = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                                filename.format(misses, 'neighbors')))
        test_nd = pd.read_csv(nd_out_path)
        ref_nd = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                          filename.format(misses, 'nd')))
        assert test_neighbor.equals(ref_neighbor)
        assert test_nd.equals(ref_nd)


def test_nd_with_ints():
    
    assert 1


def test_nd_with_nas():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input_with_na.csv"))

    for misses in range(1, 10):
        res = MinimalPairND(data=input,
                            features=["feature-01", "feature-02", "feature-03",
                                      "feature-04", "feature-05", "feature-06",
                                      "feature-07", "feature-08", "feature-09",
                                      "feature-10"],
                            allowed_misses=misses, allowed_matches=10, mirror_neighbors=True)
        filename = "input_with_na_{}_miss-{}.csv"
        neighbor_out_path = os.path.join(THIS_DIR, "test_output", filename.format(misses, 'neighbors'))
        res['neighbors'].to_csv(neighbor_out_path, na_rep='NA', index=False)

        nd_out_path = os.path.join(THIS_DIR, "test_output", filename.format(misses, 'nd'))
        res['nd'].to_csv(nd_out_path, na_rep='NA', index=False)

        test_neighbor = pd.read_csv(neighbor_out_path)
        ref_neighbor = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                                filename.format(misses, 'neighbors')))
        test_nd = pd.read_csv(nd_out_path)
        ref_nd = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                          filename.format(misses, 'nd')))
        assert test_neighbor.equals(ref_neighbor)
        assert test_nd.equals(ref_nd)
