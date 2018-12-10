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
    my_nbr.WriteCSVs(os.path.join(THIS_DIR, "test_output"), "output")
    test_neighbor = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                             "output-neighbors.csv"))
    ref_neighbor = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                            "output-neighbors.csv"))

    test_nd = pd.read_csv(os.path.join(THIS_DIR, "test_output",
                                       "output-nd.csv"))
    ref_nd = pd.read_csv(os.path.join(THIS_DIR, "expected_test_output",
                                      "output-nd.csv"))

    assert test_neighbor.equals(ref_neighbor)
    assert test_nd.equals(ref_nd)


def test_nd_with_blanks_and_ints():
    input = pd.read_csv(os.path.join(THIS_DIR, "test_data", "input_with_blanks_and_ints.csv"))
    for misses in range(0, 4):
        res = Neighbors(data=input,
                        features=["feature-01", "feature-02", "feature-03",
                                  "feature-04"],
                        allowed_misses=misses, allowed_matches=4,
                        key="Code")
        basename = "input_with_blanks_and_ints_{}_miss"
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

