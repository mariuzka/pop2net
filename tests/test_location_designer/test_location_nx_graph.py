import networkx as nx

import pop2net as p2n


def test_line_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        n_actors = None
        n_locations = None
        only_exact_n_actors = False
        overcrowding = False

    creator.create_actors(n=10)
    creator.create_locations(
        location_designers=[LineLocationDesigner],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 10
    assert len(env.locations) == 9

    assert env.actors[0].LineLocation_head
    assert len(env.actors[0].neighbors()) == 1

    assert env.actors[-1].LineLocation_tail
    assert len(env.actors[-1].neighbors()) == 1

    assert len(env.actors[1].neighbors()) == 2

    assert len(env.actors[-2].neighbors()) == 2


def test_line_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        n_actors = None
        n_locations = None
        only_exact_n_actors = False

    creator.create_actors(n=20)
    creator.create_locations(
        location_designers=[LineLocationDesigner],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 20
    assert len(env.locations) == 18

    # First line
    assert env.actors[0].LineLocation_head
    assert len(env.actors[0].neighbors()) == 1

    assert env.actors[9].LineLocation_tail
    assert len(env.actors[9].neighbors()) == 1

    assert len(env.actors[1].neighbors()) == 2

    assert len(env.actors[8].neighbors()) == 2

    # Second line
    assert env.actors[10].LineLocation_head
    assert len(env.actors[10].neighbors()) == 1

    assert env.actors[19].LineLocation_tail
    assert len(env.actors[19].neighbors()) == 1

    assert len(env.actors[11].neighbors()) == 2

    assert len(env.actors[18].neighbors()) == 2


def test_line_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        n_actors = 15
        n_locations = None
        only_exact_n_actors = False
        overcrowding = None

    creator.create_actors(n=20)
    creator.create_locations(
        location_designers=[LineLocationDesigner],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 20
    assert len(env.locations) == 18

    # First line
    assert env.actors[0].LineLocation_head
    assert len(env.actors[0].neighbors()) == 1

    assert env.actors[9].LineLocation_tail
    assert len(env.actors[9].neighbors()) == 1

    assert len(env.actors[1].neighbors()) == 2

    assert len(env.actors[8].neighbors()) == 2

    # Second line
    assert env.actors[10].LineLocation_head
    assert len(env.actors[10].neighbors()) == 1

    assert env.actors[19].LineLocation_tail
    assert len(env.actors[19].neighbors()) == 1

    assert len(env.actors[11].neighbors()) == 2

    assert len(env.actors[18].neighbors()) == 2


def test_line_4():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        n_actors = 15
        n_locations = None
        only_exact_n_actors = False
        overcrowding = True

    creator.create_actors(n=20)
    creator.create_locations(
        location_designers=[LineLocationDesigner],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 20
    assert len(env.locations) == 18

    # First line
    assert env.actors[0].LineLocation_head
    assert len(env.actors[0].neighbors()) == 1

    assert env.actors[9].LineLocation_tail
    assert len(env.actors[9].neighbors()) == 1

    assert len(env.actors[1].neighbors()) == 2

    assert len(env.actors[8].neighbors()) == 2

    # Second line
    assert env.actors[10].LineLocation_head
    assert len(env.actors[10].neighbors()) == 1

    assert env.actors[19].LineLocation_tail
    assert len(env.actors[19].neighbors()) == 1

    assert len(env.actors[11].neighbors()) == 2

    assert len(env.actors[18].neighbors()) == 2


def test_line_5():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        n_actors = 15
        n_locations = None
        only_exact_n_actors = False
        overcrowding = True

    creator.create_actors(n=5)
    creator.create_locations(
        location_designers=[LineLocationDesigner],
        delete_magic_actor_attributes=False,
    )

    assert len(env.actors) == 5
    assert len(env.locations) == 5  # one location instance is useless

    # First line
    assert env.actors[0].LineLocation_head
    assert len(env.actors[0].neighbors()) == 1

    assert env.actors[4].LineLocation_tail
    assert len(env.actors[4].neighbors()) == 1

    assert len(env.actors[1].neighbors()) == 2

    assert len(env.actors[3].neighbors()) == 2


def test_line_6():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class LineLocationDesigner(p2n.LocationDesigner):
        label = "LineLocation"
        nxgraph = nx.path_graph(10)
        only_exact_n_actors = True

    creator.create_actors(n=5)
    creator.create_locations(location_designers=[LineLocationDesigner])

    assert len(env.actors) == 5
    assert len(env.locations) == 0
