# %%
import pandas as pd
import pytest

import pop2net as p2n

# %%


@pytest.mark.skip
def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    class ClassRoom(p2n.MagicLocation):
        def split(self, agent):
            return agent.status

        def refine(self):
            for agent in self.agents:
                if agent.status == "C":
                    self.remove_agent(agent)

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])

    assert len(model.agents) == 6
    assert len(model.locations) == 3
    assert not model.locations[2].agents
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[0].agents) == 2
