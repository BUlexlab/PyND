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
