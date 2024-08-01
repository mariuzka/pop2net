import popy
from popy.creator import Creator
import pandas as pd
from collections import Counter

def test_1():
    df = pd.DataFrame({
        "status": ["A", "B", "B", "A", "B", "C"],
        })
    
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        def split(self, agent):
            return agent.status
        
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.agents) == 6
    for location in model.locations:
        if len(location.agents) == 4:
            assert len(location.agents) == 2
            assert all(agent.status == "A" for agent in location.agents)
        if location.agents[0].status == "B":
            assert len(location.agents) == 3
            assert all(agent.status == "B" for agent in location.agents)
        if location.agents[0].status == "C":
            assert len(location.agents) == 1
            assert all(agent.status == "C" for agent in location.agents)



def test_2():
    df = pd.DataFrame({
        "status": ["A", "B", "B", "A", "B", "C"],
        "sex": ["m", "m", "w", "w", "m", "m"]
        })
    
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        def split(self, agent):
            return [agent.status, agent.sex]
        
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.agents) == 6
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 3
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 1
    assert Counter(
        [agent.status for agent in model.locations[0].agents])["A"] == 2
    assert Counter(
        [agent.sex for agent in  model.locations[0].agents])["m"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[0].agents])["w"] == 1
    assert Counter(
        [agent.status for agent in model.locations[1].agents])["A"] == 1
    assert Counter(
        [agent.status for agent in model.locations[1].agents])["B"] == 2
    assert Counter(
        [agent.status for agent in model.locations[1].agents])["C"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[1].agents])["m"] == 4
    assert Counter(
        [agent.status for agent in model.locations[2].agents])["B"] == 3
    assert Counter(
        [agent.sex for agent in  model.locations[2].agents])["m"] == 2
    assert Counter(
        [agent.sex for agent in  model.locations[2].agents])["w"] == 1
    assert Counter(
        [agent.status for agent in model.locations[3].agents])["A"] == 1
    assert Counter(
        [agent.status for agent in  model.locations[3].agents])["B"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[3].agents])["w"] == 2
    assert Counter(
        [agent.status for agent in model.locations[4].agents])["C"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[4].agents])["m"] == 1


def test_3():
    df = pd.DataFrame({
        "status": ["A", "B", "B", "A", "B", "C"],
        "sex": ["m", "m", "w", "w", "m", "m"],
        "relevance": [1, 0, 0, 0, 1, 1]
        })
    
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        def split(self, agent):

            if agent.relevance == 1:
                return agent.status
            else:
                return agent.sex
 
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.agents) == 6
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 1
    assert len(model.locations[4].agents) == 1
    assert Counter(
        [agent.status for agent in model.locations[0].agents])["A"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[0].agents])["m"] == 1
    assert Counter(
        [agent.status for agent in model.locations[1].agents])["B"] == 1
    assert Counter(
        [agent.sex for agent in model.locations[1].agents])["m"] == 1
    assert Counter(
        [agent.status for agent in model.locations[2].agents])["A"] == 1
    assert Counter(
        [agent.status for agent in  model.locations[2].agents])["B"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[2].agents])["w"] == 2
    assert Counter(
        [agent.status for agent in model.locations[3].agents])["B"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[3].agents])["m"] == 1
    assert Counter(
        [agent.status for agent in model.locations[4].agents])["C"] == 1
    assert Counter(
        [agent.sex for agent in  model.locations[4].agents])["m"] == 1

