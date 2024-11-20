import pandas as pd

import pop2net as p2n


def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "A", "B", "A"],
        }
    )

    class ClassRoom(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "A"

        def weight(self, agent):
            if agent.status == "A":
                return 2
            else:
                return 1

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(model.locations) == 1
    assert len(model.agents) == 5
    # TODO TypeError: attribute name must be string, not 'int' versteh das Problem nicht
    # assert all(
    #    agent.get_location_weight(location=model.locations[0]) == 2 for agent in model.locations[0]
    # )

    assert len(model.locations[0].agents) == 3
    assert sum(not agent.locations for agent in model.agents) == 2
