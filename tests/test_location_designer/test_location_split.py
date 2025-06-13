from collections import Counter

import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def split(self, actor):
            return actor.status

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.actors) == 6
    for location in env.locations:
        if location.actors[0].status == "A":
            assert len(location.actors) == 2
            assert all(actor.status == "A" for actor in location.actors)
        if location.actors[0].status == "B":
            assert len(location.actors) == 3
            assert all(actor.status == "B" for actor in location.actors)
        if location.actors[0].status == "C":
            assert len(location.actors) == 1
            assert all(actor.status == "C" for actor in location.actors)


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
            "sex": ["m", "m", "w", "w", "m", "m"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def split(self, actor):
            return [actor.status, actor.sex]

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 5
    assert len(env.actors) == 6
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 4
    assert len(env.locations[2].actors) == 3
    assert len(env.locations[3].actors) == 2
    assert len(env.locations[4].actors) == 1
    assert (
        Counter(
            [actor.status for actor in env.locations[0].actors],
        )["A"]
        == 2
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[0].actors],
        )["m"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[0].actors],
        )["w"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[1].actors],
        )["A"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[1].actors],
        )["B"]
        == 2
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[1].actors],
        )["C"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[1].actors],
        )["m"]
        == 4
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[2].actors],
        )["B"]
        == 3
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[2].actors],
        )["m"]
        == 2
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[2].actors],
        )["w"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[3].actors],
        )["A"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[3].actors],
        )["B"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[3].actors],
        )["w"]
        == 2
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[4].actors],
        )["C"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[4].actors],
        )["m"]
        == 1
    )


def test_3():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
            "sex": ["m", "m", "w", "w", "m", "m"],
            "relevance": [1, 0, 0, 0, 1, 1],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def split(self, actor):
            if actor.relevance == 1:
                return actor.status
            else:
                return actor.sex

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 5
    assert len(env.actors) == 6
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 1
    assert len(env.locations[4].actors) == 1
    assert (
        Counter(
            [actor.status for actor in env.locations[0].actors],
        )["A"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[0].actors],
        )["m"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[1].actors],
        )["B"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[1].actors],
        )["m"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[2].actors],
        )["A"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[2].actors],
        )["B"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[2].actors],
        )["w"]
        == 2
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[3].actors],
        )["B"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[3].actors],
        )["m"]
        == 1
    )
    assert (
        Counter(
            [actor.status for actor in env.locations[4].actors],
        )["C"]
        == 1
    )
    assert (
        Counter(
            [actor.sex for actor in env.locations[4].actors],
        )["m"]
        == 1
    )
