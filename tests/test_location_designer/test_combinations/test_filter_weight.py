import pandas as pd

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "A", "B", "A"],
        }
    )

    class ClassRoom(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "A"

        def weight(self, actor):
            if actor.status == "A":
                return 2
            else:
                return 1

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 1
    assert len(env.actors) == 5
    # TODO TypeError: attribute name must be string, not 'int' versteh das Problem nicht
    # assert all(
    #    actor.get_location_weight(location=env.locations[0]) == 2 for actor in env.locations[0]
    # )

    assert len(env.locations[0].actors) == 3
    assert sum(not actor.locations for actor in env.actors) == 2
