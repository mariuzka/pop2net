import pytest

from popy.data_fakers import soep


@pytest.fixture(scope="session")
def soep10():
    return soep(size=10, seed=10)


@pytest.fixture(scope="session")
def soep100():
    return soep(size=100, seed=100)


@pytest.fixture(scope="session")
def soep1000():
    return soep(size=1000, seed=1000)


@pytest.fixture(scope="session")
def soep10_000():
    return soep(size=10_000, seed=10_000)
