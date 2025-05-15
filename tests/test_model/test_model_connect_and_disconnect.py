import pop2net as p2n


def test_model_connect_actors_and_disconnect_actors_1():
    """A test without specifying location types and without removing locations from env."""

    env = p2n.Environment()
    actor1 = p2n.Actor(env)
    actor2 = p2n.Actor(env)
    actor3 = p2n.Actor(env)
    actors = [actor1, actor2, actor3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    env.connect_actors(
        actors=actors,
        location_cls=Home,
    )

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=School,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert actor1 in env.locations[0].actors
    assert actor1 in env.locations[1].actors
    assert actor2 in env.locations[0].actors
    assert actor2 in env.locations[1].actors
    assert actor3 in env.locations[0].actors
    assert actor3 not in env.locations[1].actors

    env.disconnect_actors(actors, remove_locations=False)

    assert len(env.actors) == 3

    assert len(env.locations) == 2
    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert len(env.locations[0].actors) == 0
    assert len(env.locations[1].actors) == 0

    assert len(actor1.locations) == 0
    assert len(actor2.locations) == 0
    assert len(actor3.locations) == 0


def test_model_connect_actors_and_disconnect_actors_2():
    """A test without removing locations from env."""

    env = p2n.Environment()
    actor1 = p2n.Actor(env)
    actor2 = p2n.Actor(env)
    actor3 = p2n.Actor(env)
    actors = [actor1, actor2, actor3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    env.connect_actors(
        actors=actors,
        location_cls=Home,
    )

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=School,
    )

    env.disconnect_actors(actors, location_labels=["Home"], remove_locations=False)

    assert len(env.actors) == 3

    assert len(env.locations) == 2
    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert len(env.locations[0].actors) == 0
    assert len(env.locations[1].actors) == 2

    assert len(actor1.locations) == 1
    assert len(actor2.locations) == 1
    assert len(actor3.locations) == 0

    env.disconnect_actors(actors, location_labels=["School"], remove_locations=False)

    assert len(env.actors) == 3

    assert len(env.locations) == 2
    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert len(env.locations[0].actors) == 0
    assert len(env.locations[1].actors) == 0

    assert len(actor1.locations) == 0
    assert len(actor2.locations) == 0
    assert len(actor3.locations) == 0

    env.connect_actors(actors=actors, location_cls=School)
    env.disconnect_actors(actors=[actor1, actor2], location_labels=["School"])

    assert len(env.actors) == 3

    assert len(env.locations) == 3
    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)
    assert isinstance(env.locations[2], School)

    assert len(env.locations[0].actors) == 0
    assert len(env.locations[1].actors) == 0
    assert len(env.locations[2].actors) == 1

    assert len(actor1.locations) == 0
    assert len(actor2.locations) == 0
    assert len(actor3.locations) == 1


def test_model_connect_actors_and_disconnect_actors_3():
    env = p2n.Environment()
    actor1 = p2n.Actor(env)
    actor2 = p2n.Actor(env)
    actor3 = p2n.Actor(env)
    actors = [actor1, actor2, actor3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    env.connect_actors(
        actors=actors,
        location_cls=Home,
    )

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=School,
    )

    env.disconnect_actors(actors, location_labels=["School"], remove_locations=True)

    assert len(env.actors) == 3

    assert len(env.locations) == 1
    assert isinstance(env.locations[0], Home)

    assert len(env.locations[0].actors) == 3

    assert len(actor1.locations) == 1
    assert len(actor2.locations) == 1
    assert len(actor3.locations) == 1

    env.disconnect_actors(actors, location_labels=["Home"], remove_locations=True)

    assert len(env.actors) == 3

    assert len(env.locations) == 0

    assert len(actor1.locations) == 0
    assert len(actor2.locations) == 0
    assert len(actor3.locations) == 0


def test_model_connect_actors_and_disconnect_actors_4():
    env = p2n.Environment()
    actor1 = p2n.Actor(env)
    actor2 = p2n.Actor(env)
    actor3 = p2n.Actor(env)
    actors = [actor1, actor2, actor3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    env.connect_actors(
        actors=actors,
        location_cls=Home,
    )

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=School,
    )

    env.disconnect_actors(actors=[actor1, actor2], remove_locations=True)

    assert len(env.actors) == 3

    assert len(env.locations) == 0

    assert len(actor1.locations) == 0
    assert len(actor2.locations) == 0
    assert len(actor3.locations) == 0


def test_model_connect_actors_and_disconnect_actors_5():
    """Test actor.shared_locations()"""
    env = p2n.Environment()
    actor1 = p2n.Actor(env)
    actor2 = p2n.Actor(env)

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    assert len(actor1.shared_locations(actor2)) == 0
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Home"])) == 0
    assert len(actor1.shared_locations(actor=actor2, location_labels=["School"])) == 0

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=Home,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Home"])) == 1
    assert len(actor1.shared_locations(actor=actor2, location_labels=["School"])) == 0

    env.connect_actors(
        actors=[actor1, actor2],
        location_cls=School,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 2
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Home"])) == 1
    assert len(actor1.shared_locations(actor=actor2, location_labels=["School"])) == 1

    env.disconnect_actors(actors=[actor1, actor2], remove_locations=True)

    assert len(actor1.shared_locations(actor=actor2)) == 0
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Home"])) == 0
    assert len(actor1.shared_locations(actor=actor2, location_labels=["School"])) == 0
