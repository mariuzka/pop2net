from collections import Counter

import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(p2n.LocationDesigner):
        n_actors = 2

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def nest(self):
            return School

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[School, Classroom])

    assert len(env.actors) == 4
    assert len(env.locations) == 4

    for location in env.locations:
        if location.label == "School":
            assert len(location.actors) == 2
        if location.label == "Classroom":
            assert len(location.actors) == 2

    for actor in env.actors:
        assert (
            actor.neighbors(location_labels=["Classroom"])[0]
            is actor.neighbors(location_labels=["School"])[0]
        )

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()


def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "group": [1, 2, 1, 2, 1, 2, 1, 2],
            "_id": [1, 2, 3, 4, 5, 6, 7, 8],
        }
    )

    class School(p2n.LocationDesigner):
        n_actors = 4

    class Classroom(p2n.LocationDesigner):
        # n_actors = 2

        def split(self, actor):
            return actor.group

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(
        df=df,
        location_designers=[School, Classroom],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 8
    assert len(env.locations) == 4

    for location in env.locations:
        if location.label == "School":
            assert len(location.actors) == 4
            counter = Counter([actor.group for actor in location.actors])
            assert counter[1] == 2
            assert counter[2] == 2

    assert not all(
        location.actors[0].School == location.actors[-1].School
        for location in env.locations
        if location.label == "Classroom"
    )

    class School(p2n.LocationDesigner):
        n_actors = 4

    class Classroom(p2n.LocationDesigner):
        # n_actors = 2

        def split(self, actor):
            return actor.group

        def nest(self):
            return "School"

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(
        df=df,
        location_designers=[School, Classroom],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 8
    assert len(env.locations) == 6
    assert all(
        location.actors[0].School == location.actors[-1].School
        for location in env.locations
        if location.label == "Classroom"
    )

    for location in env.locations:
        if location.label == "School":
            assert len(location.actors) == 4
        if location.label == "Classroom":
            assert len(location.actors) == 2

    for location in env.locations:
        if location.label == "School":
            assert len(location.actors) == 4
            counter = Counter([actor.group for actor in location.actors])
            assert counter[1] == 2
            assert counter[2] == 2

    assert any(
        actor.neighbors(location_labels=[Classroom])
        not in actor.neighbors(location_labels=[School])
        for actor in env.actors
    )

    for location in env.locations:
        if location.label == "School":
            for actor in location.actors:
                assert all(actor.School == nghbr.School for nghbr in actor.neighbors())


def test_3():
    class City(p2n.LocationDesigner):
        n_actors = 4

    class Group(p2n.LocationDesigner):
        n_actors = 2

        def split(self, actor):
            return actor.group

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    for i in range(8):
        actor = p2n.Actor()
        actor.group = i % 2
        env.add_actor(actor)

    creator.create_locations(
        location_designers=[City, Group],
        delete_magic_actor_attributes=False,
    )

    for location in [loc for loc in env.locations if loc.label == "City"]:
        assert int(location.actors[0].group) == 0
        assert int(location.actors[1].group) == 1
        assert int(location.actors[2].group) == 0
        assert int(location.actors[3].group) == 1

    for location in [loc for loc in env.locations if loc.label == "Group"]:
        assert location.actors[0].group == location.actors[1].group

    # not all members of the same group are also in the same city (which is not desired)
    assert not all(location.actors[0].City == location.actors[1].City for location in env.locations)

    class GroupNestedInCity(Group):
        def nest(self):
            return City

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_locations(
        location_designers=[City, GroupNestedInCity],
        delete_magic_actor_attributes=False,
    )

    for location in [loc for loc in env.locations if loc.label == "City"]:
        assert int(location.actors[0].group) == 0
        assert int(location.actors[1].group) == 1
        assert int(location.actors[2].group) == 0
        assert int(location.actors[3].group) == 1

    for location in [loc for loc in env.locations if loc.label == "Group"]:
        assert location.actors[0].group == location.actors[1].group

    # all members of a group are in the same city
    assert all(location.actors[0].City == location.actors[1].City for location in env.locations)
