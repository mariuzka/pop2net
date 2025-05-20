import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 4
        n_actors = None
        only_exact_n_actors = False

    creator.create_locations(location_designers=[ClassRoom])
    assert len(env.locations) == 4


def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 4
        n_actors = 2

    creator.create_locations(location_designers=[ClassRoom])
    assert len(env.locations) == 4


def test_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 4
        n_actors = 2
        only_exact_n_actors = False

    env.add_actors([p2n.Actor() for _ in range(10)])
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 4
    assert len(env.actors) == 10

    for location in env.locations:
        assert len(location.actors) == 2


def test_4():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 4
        n_actors = 3
        only_exact_n_actors = True

    env.add_actors([p2n.Actor() for _ in range(10)])

    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.locations) == 3
    assert len(env.actors) == 10

    for location in env.locations:
        assert len(location.actors) == 3
