import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B", "B", "A", "A"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocationA(p2n.LocationDesigner):
        n_locations = 2

        def filter(self, actor):
            return actor.status == "A"

    class TestLocationB(p2n.LocationDesigner):
        n_locations = 1

        def filter(self, actor):
            return actor.status == "B"

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])
    inspector = p2n.NetworkInspector(env=env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=["status"])

    assert len(env.locations) == 3
    assert len(env.actors) == 6
    assert all(len(location.actors) == 2 for location in env.locations)
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "A" for actor in env.locations[1].actors)
    assert all(actor.status == "B" for actor in env.locations[2].actors)
