import pandas as pd

import pop2net as p2n


# TODO ist das so gewollt? n_locations macht drei leere Location-Objecte und dann
# generiert split die Locations mit den Agenten, aber auch nicht richtig:
# !Komisch ist, dass jeder Agent eine eigene Location zugewiesen bekommt!
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        n_locations = 3

        def split(self, agent):
            return agent.status

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status"])

    # assert len(model.locations) == 3
    # assert len(model.agents) == 6
    # for location in model.locations:
    #     if location.agents[0].status == "A":
    #         assert len(location.agents) == 2
    #         assert all(agent.status == "A" for agent in location.agents)
    #     if location.agents[0].status == "B":
    #         assert len(location.agents) == 3
    #         assert all(agent.status == "B" for agent in location.agents)
    #     if location.agents[0].status == "C":
    #         assert len(location.agents) == 1
    #         assert all(agent.status == "C" for agent in location.agents)
