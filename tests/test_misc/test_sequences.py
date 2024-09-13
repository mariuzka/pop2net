import pytest

import pop2net as p2n


@pytest.fixture
def simple_location_list():
    model = p2n.Model()
    return p2n.LocationList(
        model,
        [
            p2n.Location(model),
            p2n.Location(model),
        ],
    )


def test_n_locations_create():
    model = p2n.Model()
    locations = p2n.LocationList(model, 2, p2n.Location)
    assert len(locations) == 2


def test_location_list_len(simple_location_list):
    assert len(simple_location_list) == 2


# def test_agentlist_raises_error_on_bad_input():
#     model = p2n.Model()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         p2n.AgentList(model, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_bad_input():
#     model = p2n.Model()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         p2n.LocationList(model, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_missing_model():
#     with pytest.raises(TypeError):
#         p2n.LocationList([1,2])
