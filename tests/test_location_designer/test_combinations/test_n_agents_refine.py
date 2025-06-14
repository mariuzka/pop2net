import pandas as pd
import pytest

import pop2net as p2n


@pytest.mark.skip(reason="TODO")
def test_1():
    df = pd.DataFrame({"_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocationRemoveActor(p2n.LocationDesigner):
        n_actors = 2

        def refine(self):
            for i, actor in enumerate(self.actors, start=1):
                if i != 0 and i % 2 == 0:
                    print("Test refine 1")
                    self.remove_actor(actor)

    class TestLocationAddActors(p2n.LocationDesigner):
        # workaround: no actors in this location at start
        def filter(self, actor):
            return actor._id == 0
            # unterer return sogt dafür, dass refine ausgeführt wird
            # return actor_id == 1

        # TODO interessante Interaktion, zum Zeitpunkt wo refine aufgerufen wird
        # scheinen die actors noch nicht aus der anderen Location entfernt worden zu sein
        # wie werden die refines ausgeführt im Hintergrund?
        # PLUS refine der zweiten Location wird gar nicht ausgeführt (siehe prints)
        # TODO refine wird anscheinend nicht ausgeführt, wenn die Location leer ist!!! so gewollt?
        def refine(self):
            # Warum kein refin 2 print ?
            print("Test refin 2")
            for actor in env.actors:
                if not actor.locations:
                    print("Goes here:Refine")
                    self.add_actor(actor)
            # Test
            for actor in env.actors:
                print("Goes here: Test")
                if actor.locations:
                    self.add_actor(actor)

    creator.create(df=df, location_designers=[TestLocationRemoveActor, TestLocationAddActors])

    # inspector = p2n.NetworkInspector(env=env)
    # inspector.plot_bipartite_network()
    # inspector.plot_actor_network()

    for location in env.locations:
        print(location.type)
        print(len(location.actors))

    # nach creator.create kann ich die actors ohen location finden
    for actor in env.actors:
        if not actor.locations:
            print("Goes here:after create")
            print(actor._id)

    print(len(env.locations))
    # TODO
    # assert len(env.actors) == 10
    # assert len(env.locations) == 6
