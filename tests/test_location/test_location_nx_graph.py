import networkx as nx

import pop2net as p2n


def test_line_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        n_agents = None
        n_locations = None
        only_exact_n_agents = False
        overcrowding = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 10
    assert len(model.locations) == 9

    assert model.agents[0].LineLocation_head
    assert len(model.agents[0].neighbors()) == 1

    assert model.agents[-1].LineLocation_tail
    assert len(model.agents[-1].neighbors()) == 1

    assert len(model.agents[1].neighbors()) == 2

    assert len(model.agents[-2].neighbors()) == 2


def test_line_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        n_agents = None
        n_locations = None
        only_exact_n_agents = False

    creator.create_agents(n=20)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 20
    assert len(model.locations) == 18

    # First line
    assert model.agents[0].LineLocation_head
    assert len(model.agents[0].neighbors()) == 1

    assert model.agents[9].LineLocation_tail
    assert len(model.agents[9].neighbors()) == 1

    assert len(model.agents[1].neighbors()) == 2

    assert len(model.agents[8].neighbors()) == 2

    # Second line
    assert model.agents[10].LineLocation_head
    assert len(model.agents[10].neighbors()) == 1

    assert model.agents[19].LineLocation_tail
    assert len(model.agents[19].neighbors()) == 1

    assert len(model.agents[11].neighbors()) == 2

    assert len(model.agents[18].neighbors()) == 2


def test_line_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        n_agents = 15
        n_locations = None
        only_exact_n_agents = False
        overcrowding = None

    creator.create_agents(n=20)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 20
    assert len(model.locations) == 18

    # First line
    assert model.agents[0].LineLocation_head
    assert len(model.agents[0].neighbors()) == 1

    assert model.agents[9].LineLocation_tail
    assert len(model.agents[9].neighbors()) == 1

    assert len(model.agents[1].neighbors()) == 2

    assert len(model.agents[8].neighbors()) == 2

    # Second line
    assert model.agents[10].LineLocation_head
    assert len(model.agents[10].neighbors()) == 1

    assert model.agents[19].LineLocation_tail
    assert len(model.agents[19].neighbors()) == 1

    assert len(model.agents[11].neighbors()) == 2

    assert len(model.agents[18].neighbors()) == 2


def test_line_4():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        n_agents = 15
        n_locations = None
        only_exact_n_agents = False
        overcrowding = True

    creator.create_agents(n=20)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 20
    assert len(model.locations) == 18

    # First line
    assert model.agents[0].LineLocation_head
    assert len(model.agents[0].neighbors()) == 1

    assert model.agents[9].LineLocation_tail
    assert len(model.agents[9].neighbors()) == 1

    assert len(model.agents[1].neighbors()) == 2

    assert len(model.agents[8].neighbors()) == 2

    # Second line
    assert model.agents[10].LineLocation_head
    assert len(model.agents[10].neighbors()) == 1

    assert model.agents[19].LineLocation_tail
    assert len(model.agents[19].neighbors()) == 1

    assert len(model.agents[11].neighbors()) == 2

    assert len(model.agents[18].neighbors()) == 2


def test_line_5():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        n_agents = 15
        n_locations = None
        only_exact_n_agents = False
        overcrowding = True

    creator.create_agents(n=5)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 5
    assert len(model.locations) == 5  # one location instance is useless

    # First line
    assert model.agents[0].LineLocation_head
    assert len(model.agents[0].neighbors()) == 1

    assert model.agents[4].LineLocation_tail
    assert len(model.agents[4].neighbors()) == 1

    assert len(model.agents[1].neighbors()) == 2

    assert len(model.agents[3].neighbors()) == 2


def test_line_6():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LineLocation(p2n.MagicLocation):
        nxgraph = nx.path_graph(10)
        only_exact_n_agents = True

    creator.create_agents(n=5)
    creator.create_locations(location_classes=[LineLocation])

    assert len(model.agents) == 5
    assert len(model.locations) == 0
