import pandas as pd
import pytest

import pop2net as p2n

# TODO Gefundener Nebeneffekt:
# Die Aufteilung der Agenten ist anders als Erwartet
# Hätte erwartet loc 1 mit 3x "pupil" und loc 2 mit 2x "teacher"
# Ist es faslch diese Aufteilung zu erwarten?


@pytest.mark.skip
def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "teacher", "teacher"]})

    class TestLocation(p2n.LocationDesigner):
        n_locations = 2

        def refine(self):
            if len(self.actors) % 2 == 0:
                new_actor = p2n.Actor(env)
                new_actor.status = "pupil"
                self.add_actor(new_actor)

    env = p2n.Environment()

    creator = p2n.Creator(env=env)
    creator.create(df=df, location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="status")

    assert len(env.locations) == 2
    assert len(env.actors) == 6
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 3
    assert sum(actor.status == "pupil" for actor in env.locations[0].actors) == 2
    assert sum(actor.status == "teacher" for actor in env.locations[0].actors) == 1
    assert sum(actor.status == "pupil" for actor in env.locations[1].actors) == 2
    assert sum(actor.status == "teacher" for actor in env.locations[1].actors) == 1
