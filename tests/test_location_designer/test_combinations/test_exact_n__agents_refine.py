import pandas as pd
import pytest

import pop2net as p2n


@pytest.mark.skip
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B", "B"],
        },
    )

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def refine(self):
            if len(self.actors) % 3 != 0:
                new_actor = p2n.Actor(env)
                new_actor.status = "C"
                self.add_actor(new_actor)

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="status")

    assert len(env.actors) == 7
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 3
    assert sum(not actor.locations for actor in env.actors) == 1
    assert sum(actor.status == "A" for actor in env.locations[0].actors) == 2
    assert sum(actor.status == "C" for actor in env.locations[0].actors) == 1
    assert sum(actor.status == "A" for actor in env.locations[1].actors) == 1
    assert sum(actor.status == "B" for actor in env.locations[1].actors) == 1
    assert sum(actor.status == "C" for actor in env.locations[1].actors) == 1
