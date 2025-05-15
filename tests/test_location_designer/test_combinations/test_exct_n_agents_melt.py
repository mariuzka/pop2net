import pandas as pd

import pop2net as p2n

# Testen: Wie verhält es sich wenn n_agents vorgegeben ist aber noch lehrer übrig sind
# wie verhält es sich, wenn in der Ziel location n_agent und exact true ist, aber in den unteren nichts gesetz ist
# was passiert wenn ich false und true in den Meltlocation mixe?


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B", "B", "B"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LocA(p2n.MeltLocationDesigner):
        n_actors = 2
        only_exact_n_actors = False

        def filter(self, actor):
            return actor.status == "A"

    class LocB(p2n.MeltLocationDesigner):
        n_actors = 2
        only_exact_n_actors = False

        def filter(self, actor):
            return actor.status == "B"

    class LocAB(p2n.LocationDesigner):
        def melt(self):
            return LocA, LocB

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[LocAB])

    assert len(env.actors) == 6
    assert len(env.locations) == 2
    assert sum(True for actor in env.locations[0].actors if actor.status == "A") == 2
    assert sum(True for actor in env.locations[0].actors if actor.status == "B") == 2
    assert sum(True for actor in env.locations[1].actors if actor.status == "A") == 1
    assert sum(True for actor in env.locations[1].actors if actor.status == "B") == 1

    # Ver. with exact_n set to true
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LocA(p2n.MeltLocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def filter(self, actor):
            return actor.status == "A"

    class LocB(p2n.MeltLocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def filter(self, actor):
            return actor.status == "B"

    class LocAB(p2n.LocationDesigner):
        n_actors = 4
        only_exact_n_actors = True

        def melt(self):
            return LocA, LocB

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[LocAB])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=["status"])

    assert len(env.actors) == 6
    assert len(env.locations) == 1
    assert sum(True for actor in env.locations[0].actors if actor.status == "A") == 2
    assert sum(True for actor in env.locations[0].actors if actor.status == "B") == 2
    assert sum(True for actor in env.actors if not actor.locations) == 2
