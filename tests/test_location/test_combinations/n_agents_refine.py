# %%
import pandas as pd

import popy

# %%
# TODO interessantes Case gefunden: 
# Man kann also theoretisch keine leeren Locations damit erzeugen- gewollt?
# Error: "ZeroDivisionError: division by zero"
def n_agents_zero():

    df = pd.DataFrame({"_id": [1,2,3,4,5,6,7,8,9,10]})
    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocation(popy.MagicLocation):
        # TODO geht das?
        n_agents = 0

    creator.create(df=df, location_classes=[TestLocation])

#n_agents_zero()

# %%
def test_1():


    df = pd.DataFrame({"_id": [1,2,3,4,5,6,7,8,9,10]})
    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocationRemoveAgent(popy.MagicLocation):
        n_agents = 2

        def refine(self):
            for i, agent in enumerate(self.agents, start=1):
                if i != 0 and i % 2 == 0:
                    print("Test refine 1")
                    self.remove_agent(agent)

    class TestLocationAddAgents(popy.MagicLocation):

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


    creator.create(df=df, location_classes=[TestLocationRemoveAgent, TestLocationAddAgents])
    
    #inspector = popy.NetworkInspector(model=model)
    #inspector.plot_bipartite_network()
    #inspector.plot_agent_network()

    for location in model.locations:
        print(location.type)
        print(len(location.agents))

    # nach creator.create kann ich die agenten ohen location finden
    for agent in model.agents:
                if not agent.locations:
                    print("Goes here:after create")
                    print(agent._id)

    print(len(model.locations))
    assert len(model.agents) == 10
    assert len(model.locations) == 6


test_1()
# %%
