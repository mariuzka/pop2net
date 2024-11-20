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

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "A"

        def refine(self):
            for agent in self.agents:
                if agent.sex == "m":
                    self.remove_agent(agent)

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.agents) == 3
    assert len(model.locations[0].agents) == 1
    assert all(agent.status == "A" and agent.sex == "w" for agent in model.locations[0].agents)
    assert sum(not agent.locations for agent in model.agents) == 2
