import pandas as pd

import pop2net as p2n


def test_1():
    # recyle=False
    df = pd.DataFrame(
            {
                "status": ["A", "B", "B", "B", "A"],
                "sex": ["w", "m", "m", "m", "w"],
            },
        )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        recycle = False
        def bridge(self, agent):
            return agent.status

        def split(self, agent):
            return agent.sex
        
    creator.create(df=df, location_classes=[TestLocation])
    
    assert len(model.locations) == 0
    assert len(model.agents) == 5


def test_2():
    # recyle=True
    df = pd.DataFrame(
            {
                "status": ["A", "B", "B", "B", "A"],
                "sex": ["w", "m", "m", "m", "w"],
            },
        )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        recycle = True
        def bridge(self, agent):
            return agent.status

        def split(self, agent):
            return agent.sex
        
    creator.create(df=df, location_classes=[TestLocation])
    
    assert len(model.locations) == 5
    assert len(model.agents) == 5
    for location in model.locations:
        assert len(location.agents) == 1


def test_3():
    # recyle=False
    df = pd.DataFrame(
            {
                "status": ["A", "B", "B", "A", "B"],
                "sex": ["w", "m", "m", "m", "w"],
            },
        )

    model = p2n.Model()
    creator = p2n.Creator(model)
    
    class TestLocation(p2n.MagicLocation):
        recycle = False
        def bridge(self, agent):
            return agent.status

        def split(self, agent):
            return agent.sex
        
    creator.create(df=df, location_classes=[TestLocation])
    
    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert [agent.sex for agent in model.locations[0].agents].count("w") == 2
    assert [agent.sex for agent in model.locations[1].agents].count("m") == 2
    assert sum(not agent.locations for agent in model.agents) == 1


def test_4():
    # recyle=True
    df = pd.DataFrame(
            {
                "status": ["A", "B", "B", "A", "B"],
                "sex": ["w", "m", "m", "m", "w"],
            },
        )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        recycle = True
        def bridge(self, agent):
            return agent.status

        def split(self, agent):
            return agent.sex
        
    creator.create(df=df, location_classes=[TestLocation])
   
    assert len(model.locations) == 3
    assert len(model.agents) == 5
    assert [agent.sex for agent in model.locations[0].agents].count("w") == 2
    assert [agent.sex for agent in model.locations[1].agents].count("m") == 2
    assert [agent.sex for agent in model.locations[2].agents].count("m") == 2
    
    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 1
    assert len(model.agents[3].locations) == 2
    assert len(model.agents[4].locations) == 1