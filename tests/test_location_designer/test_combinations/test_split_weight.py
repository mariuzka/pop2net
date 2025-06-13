import pandas as pd

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    df = pd.DataFrame({"status": ["A", "B", "B", "A", "A"]})

    class ClassRoom(p2n.LocationDesigner):
        def split(self, actor):
            return actor.status

        def weight(self, actor):
            return 5

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 2
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)

    locations_weights = []
    for location in env.locations:
        locations_weights.append(
            sum([env.get_weight(actor, location) for actor in location.actors])
        )
    assert sum(locations_weights) == 25
    assert all(location.get_weight(actor) == 5 for actor in location.actors)


def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "A", "B", "A"],
        }
    )

    class ClassRoom(p2n.LocationDesigner):
        def split(self, actor):
            return actor.status

        def weight(self, actor):
            if actor.status == "A":
                return 2
            if actor.status == "B":
                return 4

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 2
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)

    assert sum([env.get_weight(actor, env.locations[0]) for actor in env.locations[0].actors]) == 6
    assert sum([env.get_weight(actor, env.locations[1]) for actor in env.locations[1].actors]) == 8
    assert all(env.locations[0].get_weight(actor) == 2 for actor in env.locations[0].actors)
    assert all(env.locations[1].get_weight(actor) == 4 for actor in env.locations[1].actors)


def test_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame({"status": ["A", "B", "A", "B"], "attention_span": [1, 3, 2.5, 4]})

    class ClassRoom(p2n.LocationDesigner):
        def split(self, actor):
            return actor.status

        def weight(self, actor):
            return actor.attention_span

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 2
    assert len(env.actors) == 4
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)

    assert (
        sum([env.get_weight(actor, env.locations[0]) for actor in env.locations[0].actors]) == 3.5
    )

    assert sum([env.get_weight(actor, env.locations[1]) for actor in env.locations[1].actors]) == 7
