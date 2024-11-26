import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil"]})
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Classroom(p2n.LocationDesigner):
        n_agents = 3
        only_exact_n_agents = False

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        pass

    creator.create(df=df, location_designers=[Classroom, School])

    assert len(model.agents) == 5
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 5

    # Version with set to true
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Classroom(p2n.LocationDesigner):
        n_agents = 3
        only_exact_n_agents = True

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        pass

    creator.create(df=df, location_designers=[Classroom, School])
    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status"])

    assert len(model.agents) == 5
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 5


def test_2():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil"]})
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Classroom(p2n.LocationDesigner):
        n_agents = 2
        only_exact_n_agents = True

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        n_agents = 4
        only_exact_n_agents = True

    creator.create(df=df, location_designers=[Classroom, School])
    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status", "id"])

    assert len(model.agents) == 6
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 4
    assert model.locations[2].agents not in model.locations[3].agents
