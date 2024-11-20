import pandas as pd
import pytest

import pop2net as p2n


@pytest.mark.skip(reason="TODO")
def test_1():
    df = pd.DataFrame({"_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class TestLocationRemoveAgent(p2n.LocationDesigner):
        n_agents = 2

        def refine(self):
            for i, agent in enumerate(self.agents, start=1):
                if i != 0 and i % 2 == 0:
                    print("Test refine 1")
                    self.remove_agent(agent)

    class TestLocationAddAgents(p2n.LocationDesigner):
        # workaround: no agents in this location at start
        def filter(self, agent):
            return agent._id == 0
            # unterer return sogt dafür, dass refine ausgeführt wird
            # return agent_id == 1

        # TODO interessante Interaktion, zum Zeitpunkt wo refine aufgerufen wird
        # scheinen die agents noch nicht aus der anderen Location entfernt worden zu sein
        # wie werden die refines ausgeführt im Hintergrund?
        # PLUS refine der zweiten Location wird gar nicht ausgeführt (siehe prints)
        # TODO refine wird anscheinend nicht ausgeführt, wenn die Location leer ist!!! so gewollt?
        def refine(self):
            # Warum kein refin 2 print ?
            print("Test refin 2")
            for agent in model.agents:
                if not agent.locations:
                    print("Goes here:Refine")
                    self.add_agent(agent)
            # Test
            for agent in model.agents:
                print("Goes here: Test")
                if agent.locations:
                    self.add_agent(agent)

    creator.create(df=df, location_designers=[TestLocationRemoveAgent, TestLocationAddAgents])

    # inspector = p2n.NetworkInspector(model=model)
    # inspector.plot_bipartite_network()
    # inspector.plot_agent_network()

    for location in model.locations:
        print(location.type)
        print(len(location.agents))

    # nach creator.create kann ich die agenten ohen location finden
    for agent in model.agents:
        if not agent.locations:
            print("Goes here:after create")
            print(agent._id)

    print(len(model.locations))
    # TODO
    # assert len(model.agents) == 10
    # assert len(model.locations) == 6


# %%
