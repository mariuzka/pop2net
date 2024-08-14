#%%
import pandas as pd
import popy


# TODO nur Blaupauise von nest test
def test_1():
    
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
            "class_id":[1,2,1,2]
        }
    )

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

        
    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 2
    
    for location in model.locations:
        assert len(location.agents) == 2
    
    for agent in model.agents:
        assert (agent.neighbors(
            location_classes = [Classroom])[0].class_id == agent.class_id)
            
        
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")



# stick together with uneven agent-location "seats"
def test_2():

    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil"],
            "class_id":[1,2,1,2,1]
        }
    )

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

        
    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

    assert len(model.agents) == 5
    assert len(model.locations) == 2

    expected_loc_lens = [2,3]
    for location in model.locations:
        assert len(location.agents) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.agents))]
    
    for agent in model.agents:
        for agent in model.agents:
            assert all(nghbr.class_id == agent.class_id for nghbr in agent.neighbors())





# stick_together vs filter
def test_3():

    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
            "class_id":[1,2,1,2],
            "friends": [1,1,2,2],
        }
    )

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.class_id

        def stick_together(self, agent):
            return agent.friends

        
    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

    # assert len(model.agents) == 5
    # assert len(model.locations) == 2

    # expected_loc_lens = [2,3]
    # for location in model.locations:
    #     assert len(location.agents) in expected_loc_lens
    #     del expected_loc_lens[expected_loc_lens.index(len(location.agents))]
    
    # for agent in model.agents:
    #     for agent in model.agents:
    #         assert all(nghbr.class_id == agent.class_id for nghbr in agent.neighbors())



#test_1()
#test_2()
test_3()
#%%
    
