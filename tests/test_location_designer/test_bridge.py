import pop2net as p2n


def test_1():
    # basic test

    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(3):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(2):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = False

        def bridge(self, actor):
            return actor.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(env.locations) == 2
    assert len(env.actors) == 5

    for location in env.locations:
        assert len(location.actors) == 2
        assert [actor.gender for actor in location.actors].count("m") == 1
        assert [actor.gender for actor in location.actors].count("w") == 1

    assert len(env.actors[0].locations) == 1
    assert len(env.actors[1].locations) == 1
    assert len(env.actors[2].locations) == 0
    assert len(env.actors[3].locations) == 1
    assert len(env.actors[4].locations) == 1


def test_2():
    # test n_locations

    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(3):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(2):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = False
        n_locations = 1

        def bridge(self, actor):
            return actor.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(env.locations) == 1
    assert len(env.actors) == 5

    location = env.locations[0]
    assert len(location.actors) == 2
    assert [actor.gender for actor in location.actors].count("m") == 1
    assert [actor.gender for actor in location.actors].count("w") == 1

    assert len(env.actors[0].locations) == 1
    assert len(env.actors[1].locations) == 0
    assert len(env.actors[2].locations) == 0
    assert len(env.actors[3].locations) == 1
    assert len(env.actors[4].locations) == 0


def test_3():
    # test recycle

    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(3):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(2):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = True

        def bridge(self, actor):
            return actor.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(env.locations) == 3
    assert len(env.actors) == 5

    for location in env.locations:
        assert len(location.actors) == 2
        assert [actor.gender for actor in location.actors].count("m") == 1
        assert [actor.gender for actor in location.actors].count("w") == 1

    assert len(env.actors[0].locations) == 1
    assert len(env.actors[1].locations) == 1
    assert len(env.actors[2].locations) == 1
    assert len(env.actors[3].locations) == 2
    assert len(env.actors[4].locations) == 1


def test_4():
    # test n_locations and recycle

    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(3):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(2):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = True
        n_locations = 1

        def bridge(self, actor):
            return actor.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(env.locations) == 1
    assert len(env.actors) == 5

    location = env.locations[0]
    assert len(location.actors) == 2
    assert [actor.gender for actor in location.actors].count("m") == 1
    assert [actor.gender for actor in location.actors].count("w") == 1

    assert len(env.actors[0].locations) == 1
    assert len(env.actors[1].locations) == 0
    assert len(env.actors[2].locations) == 0
    assert len(env.actors[3].locations) == 1
    assert len(env.actors[4].locations) == 0
