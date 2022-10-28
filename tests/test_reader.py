import pytest

from src.reader import DataReader


def test_reader_small(soep100):
    reader = DataReader(soep100, seed=5)
    assert soep100.equals(reader.df)


@pytest.mark.parametrize("size", [10, 11, 137, 473, 5321])
@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_sample_size(size, soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    reader = DataReader(soep, seed=5)
    sample = reader.sample(by="hid", size=size, weights=None)
    assert len(sample) == size
