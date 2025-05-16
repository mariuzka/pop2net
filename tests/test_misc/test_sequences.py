import pytest

import pop2net as p2n


@pytest.fixture
def simple_location_list():
    env = p2n.Environment()
    return p2n.LocationList(
        env,
        [
            p2n.Location(env),
            p2n.Location(env),
        ],
    )


def test_n_locations_create():
    env = p2n.Environment()
    locations = p2n.LocationList(env, 2, p2n.Location)
    assert len(locations) == 2


def test_location_list_len(simple_location_list):
    assert len(simple_location_list) == 2


# def test_actorlist_raises_error_on_bad_input():
#     env = p2n.Environment()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         p2n.ActorList(env, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_bad_input():
#     env = p2n.Environment()
#     with pytest.raises(ValueError, match=r"invalid objs"):
#         p2n.LocationList(env, objs=[1,2,3,4])

# def test_locationlist_raises_error_on_missing_env():
#     with pytest.raises(TypeError):
#         p2n.LocationList([1,2])
