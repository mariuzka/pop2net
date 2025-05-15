import pandas as pd
import pytest

import pop2net as p2n


@pytest.mark.skip
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B"],
            "sex": ["w", "m", "w"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "A"

        def refine(self):
            for actor in self.actors:
                if actor.sex == "m":
                    self.remove_actor(actor)

    creator.create_actors(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.actors) == 3
    assert len(env.locations[0].actors) == 1
    assert all(actor.status == "A" and actor.sex == "w" for actor in env.locations[0].actors)
    assert sum(not actor.locations for actor in env.actors) == 2
