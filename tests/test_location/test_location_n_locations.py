# %%

import pop2net as p2n


def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class ClassRoom(p2n.MagicLocation):
        n_locations = 4
        n_agents = None
        only_exact_n_agents = False

    creator.create_locations(location_classes=[ClassRoom])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()

    assert len(model.locations) == 4


# %%


def test_2():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class ClassRoom(p2n.MagicLocation):
        n_locations = 4
        n_agents = 2

    creator.create_locations(location_classes=[ClassRoom])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()

    assert len(model.locations) == 4


test_2()

# %%


def test_3():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class ClassRoom(p2n.MagicLocation):
        n_locations = 4
        n_agents = 2
        only_exact_n_agents = False

    for _ in range(10):
        p2n.Agent(model=model)

    creator.create_locations(location_classes=[ClassRoom])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()

    assert len(model.locations) == 4
    assert len(model.agents) == 10

    for location in model.locations:
        assert len(location.agents) == 2


test_3()

# %%


def test_4():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class ClassRoom(p2n.MagicLocation):
        n_locations = 4
        n_agents = 3
        only_exact_n_agents = True

    for _ in range(10):
        p2n.Agent(model=model)

    creator.create_locations(location_classes=[ClassRoom])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    assert len(model.agents) == 10

    for location in model.locations:
        assert len(location.agents) == 3


test_4()
