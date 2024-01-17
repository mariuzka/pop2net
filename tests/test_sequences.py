import popy
import pytest

@pytest.fixture()
def simple_location_list():
    model = popy.Model()
    return popy.LocationList(
        model,
        [
            popy.Location(model),
            popy.Location(model),
        ],
    )


def test_n_locations_create():
    model = popy.Model()
    locations = popy.LocationList(model, 2, popy.Location)
    assert len(locations) == 2


def test_location_list_len(simple_location_list):
    assert len(simple_location_list) == 2
