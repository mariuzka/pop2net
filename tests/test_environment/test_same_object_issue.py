import pytest

import pop2net as p2n


def test_1_actor():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()

    env.add_actors([actor1, actor2])
    with pytest.raises(ValueError) as exc:
        actor1.get_actor_weight(actor1)
    assert str(exc.value) == "Entity 1 and entity 2 are identical."


def test_2_actor_creator():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(n=2)
    with pytest.raises(ValueError) as exc:
        env.actors[0].get_actor_weight(env.actors[0])
    assert str(exc.value) == "Entity 1 and entity 2 are identical."


def test_3_location():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()
    env.add_actors([actor1, actor2])
    env.add_location(location1)
    location1.add_actors([actor1, actor2])
    with pytest.raises(ValueError) as exc:
        env.locations_between_actors(actor1, actor1)
    assert str(exc.value) == "Entity 1 and entity 2 are identical."


def test_4_location_creator():
    class Location1(p2n.LocationDesigner):
        pass

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(n=2)
    creator.create_locations(location_designers=[Location1])
    with pytest.raises(ValueError) as exc:
        env.locations_between_actors(env.actors[0], env.actors[0])
    assert str(exc.value) == "Entity 1 and entity 2 are identical."


def test_5_shared_loc():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()
    env.add_actors([actor1, actor2])
    env.add_location(location1)
    location1.add_actors([actor1, actor2])
    with pytest.raises(ValueError) as exc:
        env.actors[0].shared_locations(env.actors[0])
    assert str(exc.value) == "Entity 1 and entity 2 are identical."


def test_6_shared_loc_creator():
    class Location1(p2n.LocationDesigner):
        pass

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(n=2)
    creator.create_locations(location_designers=[Location1])
    with pytest.raises(ValueError) as exc:
        env.actors[0].shared_locations(env.actors[0])
    assert str(exc.value) == "Entity 1 and entity 2 are identical."
