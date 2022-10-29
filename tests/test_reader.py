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


def test_sample_by_str_col(soep100):
    soep100.pid = soep100.pid.astype(str)
    reader = DataReader(soep100, seed=5)
    sample = reader.sample(by="pid", size=10, with_replacement=False)
    assert sample.pid.nunique() == 10


@pytest.mark.parametrize("size", [10, 50, 99, 100])
def test_sample_no_replacement(soep100, size):
    reader = DataReader(soep100, seed=5)
    sample = reader.sample(by="pid", size=size, with_replacement=False)
    assert sample.pid.nunique() == size


def test_sample_no_replacement_grouped_edgecase(soep100):
    reader = DataReader(soep100, seed=5)
    sample = reader.sample(by="hid", size=99, with_replacement=False)
    assert len(sample) == 99
    assert sample.hid.nunique() < 99


def test_sample_no_replacement_too_many(soep100):
    reader = DataReader(soep100, seed=5)
    with pytest.raises(ValueError):
        reader.sample(by="pid", size=101, with_replacement=False)


def test_sample_with_replacement_too_many(soep100):
    reader = DataReader(soep100, seed=5)
    sample = reader.sample(by="pid", size=101, with_replacement=True)
    assert len(sample) == 101
