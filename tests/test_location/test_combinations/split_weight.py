# %%
import pandas as pd

import popy


# %%
def test_1():

    model = popy.Model()
    creator = popy.Creator(model=model)
    inspector = popy.NetworkInspector(model=model)
    df = pd.DataFrame(
        {"status": ["A", "B", "B", "A", "A"]        
         }
        )
    
    class ClassRoom(popy.MagicLocation):

        def split(self, agent):
            return agent.status
        
        def weight(self, agent):
            return 5
        
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])
    inspector.plot_bipartite_network()
    inspector.plot_agent_network()

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0])
    assert all(agent.status == "B" for agent in model.locations[1])
    
    # TODO Warum triggered das nicht assert?
    #assert all([[location.get_weight(agent) == 4 for agent in location.agents] for location in model.locations])

    # TODO
    # keine Ahnung wie ich das effizienter ermitteln könnte
    # List comprehension geschachtelt geht bei mir nicht siehe oben
    locations_weights = []
    #model sum weight
    for location in model.locations:
            locations_weights.append(sum([model.get_weight(agent, location) for agent in location.agents]))
    assert sum(locations_weights) == 25
    # individual weights
    assert all(location.get_weight(agent) == 5 for agent in location.agents)

     
test_1()


# %%
def test_2():

    model = popy.Model()
    creator = popy.Creator(model=model)
    inspector = popy.NetworkInspector(model=model)
    df = pd.DataFrame(
        {"status": ["A", "B", "A", "B", "A"],
         })
    
    class ClassRoom(popy.MagicLocation):

        def split(self, agent):
            return agent.status
        
        def weight(self, agent):
            if agent.status == "A":
                return 2
            if agent.status == "B":
                return 4
            
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0])
    assert all(agent.status == "B" for agent in model.locations[1])

    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 6
    )
    assert (
        sum([model.get_weight(agent, model.locations[1]) for agent in model.locations[1].agents])
        == 8
    )
    assert all(
        model.locations[0].get_weight(agent) == 2 for agent in model.locations[0].agents
    )
    assert all(
        model.locations[1].get_weight(agent) == 4 for agent in model.locations[1].agents
    )

test_2()


# %%
def test_3():

    model = popy.Model()
    creator = popy.Creator(model=model)
    inspector = popy.NetworkInspector(model=model)
    df = pd.DataFrame(
        {"status": ["A", "B", "A", "B"],
         "attention_span": [1, 3, 2.5, 4]
         })
    
    class ClassRoom(popy.MagicLocation):

        def split(self, agent):
            return agent.status
        
        def weight(self, agent):
            return agent.attention_span
        
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.locations) == 2
    assert len(model.agents) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 3.5
    )

    assert (
        sum([model.get_weight(agent, model.locations[1]) for agent in model.locations[1].agents])
        == 7
    )
            
test_3()