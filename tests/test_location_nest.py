#%%
import pandas as pd
import popy
from collections import Counter


# simple nesting: 2 classrooms in 2 school
def test_1():
    
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(popy.MagicLocation):
        n_agents = 2

    class Classroom(popy.MagicLocation):

        n_agents = 2
        
        def nest(self):
            return School
   
    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 4
    
    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 2
        if location.type == "Classroom":
            assert len(location.agents) == 2
    
    for agent in model.agents:
        assert (agent.neighbors(
            location_classes = [Classroom])[0]
            is
            agent.neighbors(location_classes = [School])[0])
 
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
   



#%%
#test_1()





def test_2():

    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil",
                       "pupil", "pupil", "pupil", "pupil"],
            "group": [1,2,1,2,1,2,1,2]
        }
    )

    # Fall: Aufteilung in falsche Schulen, weil kein nest
    class School(popy.MagicLocation):
        n_agents = 4

    class Classroom(popy.MagicLocation):

        n_agents = 2
        
        def split(self, agent):
            return agent.group
        
        #def nest(self):
            #return School

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 8
    assert len(model.locations) == 6

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    


    class School(popy.MagicLocation):
        n_agents = 4

    class Classroom(popy.MagicLocation):

        n_agents = 2

        def split(self, agent):
            return agent.group
        
        def nest(self):
            return School
    

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])

    assert len(model.agents) == 8
    assert len(model.locations) == 6

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="group")

    # for location in model.locations:
    #     if location.type == "School":
    #         assert len(location.agents) == 4
    #         counter = Counter([agent.group for agent in location.agents])
    #         assert counter[1] == 2
    #         assert counter[2] == 2

    
    #for location in model.locations:
        #if location.type == "School":
            #assert len(location.agents) == 2
        #if location.type == "Classroom":
            #assert len(location.agents) == 2
    
    #for agent in model.agents:
        #assert (agent.neighbors(
            #location_classes = [Classroom])[0]
            #is
            #agent.neighbors(location_classes = [School])[0])

    





test_2()
# TODO Test 2/3 was will ich tesetn? 
#%%