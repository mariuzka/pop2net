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

# def test_agentlist_raises_error_on_bad_input():
#     model = popy.Model()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         popy.AgentList(model, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_bad_input():
#     model = popy.Model()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         popy.LocationList(model, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_missing_model():
#     with pytest.raises(TypeError):
#         popy.LocationList([1,2])
