import pandas as pd

import pop2net as p2n


def test_1():
    # recycle=False+stick_together
    df = pd.DataFrame({"gender": ["w", "w", "w", "m", "m"],
                       "friends": [1, 1, 2, 2,1],
                       "identity":[1,2,3,4,5]
                       })
    model = p2n.Model()
    creator = p2n.Creator(model)

    class Friendship(p2n.MagicLocation):
        recycle = False

        def bridge(self, agent):
            return agent.gender
        

        def stick_together(self, agent):
            return agent.friends

    creator.create(df=df, location_classes=[Friendship])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="friends")

    assert len(model.locations) == 2
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1
    
    # check stick_together (should be ignored for agent assignment)
    assert all(agent.identity in [1,4]  for agent in model.locations[0].agents)
    assert all(agent.identity in [2,5] for agent in model.locations[1].agents)

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 1


def test_2():
    # recyle=True+stick_together
    df = pd.DataFrame({"gender": ["w", "w", "w", "m", "m"],
                    "friends": [1, 2, 3, 1, 1],
                    "identity":[1,2,3,4,5]
                    })
    
    model = p2n.Model()
    creator = p2n.Creator(model)

    class Friendship(p2n.MagicLocation):
        recycle = True

        def bridge(self, agent):
            return agent.gender
        

        def stick_together(self, agent):
            return agent.friends

    creator.create(df=df, location_classes=[Friendship])
    
    assert len(model.locations) == 3
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1
    
    # check stick_together (should be ignored for agent assignment)
    assert all(agent.identity in [1,4]  for agent in model.locations[0].agents)
    assert all(agent.identity in [2,5] for agent in model.locations[1].agents)
    assert all(agent.identity  in [3,4] for agent in model.locations[2].agents)

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 1
    assert len(model.agents[3].locations) == 2
    assert len(model.agents[4].locations) == 1