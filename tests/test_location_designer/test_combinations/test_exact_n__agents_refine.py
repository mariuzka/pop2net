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
        n_agents = 2
        only_exact_n_agents = True

        def refine(self):
            if len(self.agents) % 3 != 0:
                new_agent = p2n.Agent(model)
                new_agent.status = "C"
                self.add_agent(new_agent)

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="status")

    assert len(model.agents) == 7
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 3
    assert sum(not agent.locations for agent in model.agents) == 1
    assert sum(agent.status == "A" for agent in model.locations[0].agents) == 2
    assert sum(agent.status == "C" for agent in model.locations[0].agents) == 1
    assert sum(agent.status == "A" for agent in model.locations[1].agents) == 1
    assert sum(agent.status == "B" for agent in model.locations[1].agents) == 1
    assert sum(agent.status == "C" for agent in model.locations[1].agents) == 1
