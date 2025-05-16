# %%
import pandas as pd

import pop2net as p2n

# %%


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_locations = 4

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    assert len(env.actors) == 4
    assert len(env.locations) == 4

    for location in env.locations[0:2]:
        assert len(location.actors) == 2

    for actor in env.actors:
        assert actor.neighbors(location_labels=["Classroom"])[0].class_id == actor.class_id
    assert all(not location.actors for location in env.locations[2:])
