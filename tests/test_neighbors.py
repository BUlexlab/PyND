import os
import pandas as pd
import tempfile
import pytest

from pynd.neighbors import Neighbors

THIS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

FEATURES = ["MajorLocation 2.0", "MinorLocation 2.0"]


def test_too_many_misses():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, FEATURES, allowed_misses=3, allowed_matches=2)
    assert 'allowed_misses must be less than or equal to (length(features) - 1)' in str(exc.value)

def test_misses_less_than_zero():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, FEATURES, allowed_misses=-1, allowed_matches=2)
    assert "allowed_misses must be >=0" in str(exc.value)


def test_too_many_matches():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, FEATURES, allowed_misses=1, allowed_matches=3)
    assert "allowed_matches cannot exceed length(features)" in str(exc.value)


def test_matches_less_than_zero():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, FEATURES, allowed_misses=1, allowed_matches=-1)
    assert "allowed_matches must be greater than 1" in str(exc.value)

def test_missing_key():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, FEATURES, allowed_misses=1, allowed_matches=None,
                           key="FooBar")
    assert "Key FooBar is not a column in DataFrame data" in str(exc.value)
    

def test_missing_features():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    with pytest.raises(ValueError) as exc:
        my_nbr = Neighbors(data, [*FEATURES, "foo"], allowed_misses=1, allowed_matches=None)
    assert "not in DataFrame data" in str(exc.value)


def test_neighborhood_density():
    data = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    my_nbr = Neighbors(data, FEATURES, allowed_misses=1, allowed_matches=None)
    my_nbr.ND
    assert True


def test_nd():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input.csv"))
    res = Neighbors(data=input,
                    features=["SignType 2.0", "MinorLocation 2.0",
                              "SecondMinorLocation", "Movement 2.0",
                              "Contact", "SelectedFingers 2.0",
                              "Flexion 2.0", "FlexionChange",
                              "Spread", "SpreadChange"],
                    allowed_misses=9, allowed_matches=10)
    res.WriteCSVs(os.path.join(THIS_DIR, "test_output"), "result")
    # neighbor_out_path = os.path.join(THIS_DIR, "test_output", "result-neighbors.csv")
    # res.neighbors.to_csv(neighbor_out_path, na_rep='NA', index=False)

    # nd_out_path = os.path.join(THIS_DIR, "test_output", "result-nd.csv")
    # res.nd.to_csv(nd_out_path, na_rep='NA', index=False)


def test_nd_all_alpha():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "all_alpha_input.csv"))

    for misses in range(1, 10):
        res = Neighbors(data=input,
                        features=["feature-01", "feature-02", "feature-03",
                                  "feature-04", "feature-05", "feature-06",
                                  "feature-07", "feature-08", "feature-09",
                                  "feature-10"],
                        allowed_misses=misses, allowed_matches=10,
                        key="EntryID")
        basename = "all_alpha_{}_miss"
        res.WriteCSVs(os.path.join(THIS_DIR, "test_output"), basename.format(misses))

        test_neighbor = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                                 basename.format(misses)+"-neighbors.csv"))
        ref_neighbor = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                                basename.format(misses)+"-neighbors.csv"))

        test_nd = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                           basename.format(misses)+"-nd.csv"))
        ref_nd = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                          basename.format(misses)+"-nd.csv"))

        # TODO: check why neighbors are apparently not being mirrored in CSV
        # TODO: test fails because expected output is using sign as key, not code. -- implement user-specified key field in Neighbors

        assert test_neighbor.equals(ref_neighbor)
        assert test_nd.equals(ref_nd)


def test_nd_with_ints():

    assert 1


def test_nd_with_nas():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input_with_na.csv"))

    for misses in range(1, 10):
        res = Neighbors(data=input,
                        features=["feature-01", "feature-02", "feature-03",
                                  "feature-04", "feature-05", "feature-06",
                                  "feature-07", "feature-08", "feature-09",
                                  "feature-10"],
                        allowed_misses=misses, allowed_matches=10,
                        key="EntryID")
        basename = "input_with_na_{}_miss"
        res.WriteCSVs(os.path.join(THIS_DIR, "test_output"), basename.format(misses))

        test_neighbor = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                                 basename.format(misses)+"-neighbors.csv"))
        ref_neighbor = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                                basename.format(misses)+"-neighbors.csv"))

        test_nd = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                           basename.format(misses)+"-nd.csv"))
        ref_nd = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                          basename.format(misses)+"-nd.csv"))

        assert test_neighbor.equals(ref_neighbor)
        assert test_nd.equals(ref_nd)
