# %%
import pandas as pd

import popy
from popy.creator import Creator


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "school_id": [1, 2, 1, 2, 1, 2, 1, 2],
        }
    )
    model = popy.Model()
    creator = popy.Creator(model=model)
    


    # zwei Schools
    # filter school_id
    # 4 Classrooms
    # nest classrooms in schools
    class Classroom1(popy.MagicLocation):
        n_agents = 2

        def filter(self, agent):
            return agent.school_id == 1
        def nest(self):
            return School

    class Classroom2(popy.MagicLocation):
        n_agents = 2

        def filter(self,agent):
            return agent.school_id == 2
        def nest(self):
            return School
        
    class School(popy.MagicLocation):
        n_locations = 2
        def filter(self)


    
    

        
    creator.create(df=df, location_classes=[Classroom1,Classroom2, School])
    inspector = popy.NetworkInspector(model = model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status", "school_id"])
        
        
    
test_1()

# %%
