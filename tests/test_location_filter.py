import popy
from popy.pop_maker import PopMaker
import pandas as pd

def test_1():
    df = pd.DataFrame({
        "status": ["A", "B", "B", "A", "B"],
        })
    
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocationA(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "A"
        
    class TestLocationB(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "B"

    popmaker.create_agents(df=df)
    popmaker.create_locations(location_classes=[TestLocationA, TestLocationB])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 3


def test_2():
    df = pd.DataFrame({
        "status": ["A", "B", "B", "A", "B"],
        "sex":    ["w", "m", "m", "m", "w"],
        })

    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocationA(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "A" and agent.sex == "w"
        
    class TestLocationB(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "B" and agent.sex == "w"

    popmaker.create_agents(df=df)
    popmaker.create_locations(location_classes=[TestLocationA, TestLocationB])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1