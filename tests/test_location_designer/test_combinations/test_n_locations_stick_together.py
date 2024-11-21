# %%
import pandas as pd

import pop2net as p2n

# %%


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_locations = 4

        def stick_together(self, agent):
            return agent.class_id

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_designers=[Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 4

    for location in model.locations[0:2]:
        assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_labels=["Classroom"])[0].class_id == agent.class_id
    assert all(not location.agents for location in model.locations[2:])
