# %%
import pandas as pd
import pytest

import pop2net as p2n

# %%


@pytest.mark.skip
def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    class ClassRoom(p2n.LocationDesigner):
        def split(self, actor):
            return actor.status

        def refine(self):
            for actor in self.actors:
                if actor.status == "C":
                    self.remove_actor(actor)

    creator.create_actors(df=df)
    creator.create_locations(location_classes=[ClassRoom])

    assert len(env.actors) == 6
    assert len(env.locations) == 3
    assert not env.locations[2].actors
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[0].actors) == 2
