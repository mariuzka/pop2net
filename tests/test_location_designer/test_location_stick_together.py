import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    assert len(env.actors) == 4
    assert len(env.locations) == 2

    for location in env.locations:
        assert len(location.actors) == 2

    for actor in env.actors:
        assert actor.neighbors(location_labels=["Classroom"])[0].class_id == actor.class_id

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="class_id")


# stick together with uneven actor-location "seats"
def test_2():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2, 1]}
    )

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="class_id")

    assert len(env.actors) == 5
    assert len(env.locations) == 2

    expected_loc_lens = [2, 3]
    for location in env.locations:
        assert len(location.actors) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.actors))]

    for actor in env.actors:
        assert all(nghbr.class_id == actor.class_id for nghbr in actor.neighbors())


# stick_together with split
def test_3():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "class_id": [1, 1, 1, 2, 2, 2],
            "friends": [1, 2, 1, 2, 1, 2],
        }
    )

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def split(self, actor):
            return actor.class_id

        def stick_together(self, actor):
            return actor.friends

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="class_id")

    assert len(env.actors) == 6
    assert len(env.locations) == 4

    expected_loc_lens = [1, 1, 2, 2]
    for location in env.locations:
        assert len(location.actors) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.actors))]

    for actor in env.actors:
        assert all(nghbr.class_id == actor.class_id for nghbr in actor.neighbors())


def test_4():
    # A test with many stick_together-values

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    df = pd.DataFrame(
        {"group": [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 3, 2, 3, 4, 5, 6, 6, 6, 6, 6, 10, 23, 10, 1, 1, 1]}
    )

    # location without stick_together()
    class TestLocation(p2n.LocationDesigner):
        n_locations = 5

    creator.create_actors(df=df)
    creator.create_locations(
        location_designers=[TestLocation],
        delete_magic_actor_attributes=False,
    )

    assert len(env.locations) == 5
    assert len(env.actors) == 26

    # assert that not all members of a group are in the same location
    assert not all(
        actor_i.TestLocation == actor_j.TestLocation
        for actor_i in env.actors
        for actor_j in env.actors
        if actor_i.group == actor_j.group
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    inspector = p2n.NetworkInspector(env=env)

    # location with stick_together()
    class TestLocation(p2n.LocationDesigner):
        n_locations = 5

        def stick_together(self, actor):
            return actor.group

    creator.create_actors(df=df)
    creator.create_locations(
        location_designers=[TestLocation],
        delete_magic_actor_attributes=False,
    )

    assert len(env.locations) == 5
    assert len(env.actors) == 26

    # assert that all members of a group are in the same location
    assert all(
        actor_i.TestLocation == actor_j.TestLocation
        for actor_i in env.actors
        for actor_j in env.actors
        if actor_i.group == actor_j.group
    )

    inspector.plot_actor_network(actor_attrs=["group"])
