import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
            ],
            "class_id": [1, 2, 1, 2, 1, 2, 1, 2, 3],
        }
    )
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Classroom1(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.class_id == 1

        def nest(self):
            return School

    class Classroom2(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.class_id == 2

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.class_id == 1 or agent.class_id == 2

    creator.create(df=df, location_classes=[Classroom1, Classroom2, School])
    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status", "class_id"])

    assert len(model.agents) == 9
    assert len(model.locations) == 3
    assert all(agent.class_id == 1 for agent in model.locations[0].agents)
    assert all(agent.class_id == 2 for agent in model.locations[1].agents)
    assert all(agent.class_id in [1, 2] for agent in model.locations[2].agents)
    assert all(not agent.locations for agent in model.agents if agent.class_id == 3)


# %%
def test_2():
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
            ],
            "school_id": [1, 2, 1, 2, 1, 2, 1, 2, 3],
        }
    )
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Classroom1(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.school_id == 1

        def nest(self):
            return School1

    class Classroom2(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.school_id == 2

        def nest(self):
            return School2

    class School1(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.school_id == 1

    class School2(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.school_id == 2

    creator.create(df=df, location_classes=[Classroom1, Classroom2, School1, School2])
    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status", "school_id"])
    print(model.locations[3])

    assert len(model.agents) == 9
    assert len(model.locations) == 4
    assert all(agent.school_id == 1 for agent in model.locations[0].agents)
    assert all(agent.school_id == 2 for agent in model.locations[1].agents)
    assert all(agent.school_id == 1 for agent in model.locations[2].agents)
    assert all(agent.school_id == 2 for agent in model.locations[3].agents)
    assert all(not agent.locations for agent in model.agents if agent.school_id == 3)
