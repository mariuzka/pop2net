import pop2net as p2n


def test_actor_connect_1():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    actor3 = p2n.Actor()
    env.add_actors([actor1, actor2, actor3])

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    actor1.connect(
        actor=actor2,
        location_cls=Home,
    )

    actor2.connect(
        actor=actor3,
        location_cls=School,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert actor1 in env.locations[0].actors
    assert actor1 not in env.locations[1].actors

    assert actor2 in env.locations[0].actors
    assert actor2 in env.locations[1].actors

    assert actor3 not in env.locations[0].actors
    assert actor3 in env.locations[1].actors

    actor1.disconnect(
        actor2,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=True,
    )


def test_actor_disconnect_1():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    actor3 = p2n.Actor()
    env.add_actors([actor1, actor2, actor3])

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    actor1.connect(
        actor=actor2,
        location_cls=Home,
    )

    actor2.connect(
        actor=actor3,
        location_cls=School,
    )

    actor1.disconnect(
        actor2,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=True,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert actor1 not in env.locations[0].actors
    assert actor1 not in env.locations[1].actors

    assert actor2 not in env.locations[0].actors
    assert actor2 in env.locations[1].actors

    assert actor3 not in env.locations[0].actors
    assert actor3 in env.locations[1].actors

    actor2.disconnect(
        actor3,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=False,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], Home)
    assert isinstance(env.locations[1], School)

    assert actor1 not in env.locations[0].actors
    assert actor1 not in env.locations[1].actors

    assert actor2 not in env.locations[0].actors
    assert actor2 in env.locations[1].actors

    assert actor3 not in env.locations[0].actors
    assert actor3 not in env.locations[1].actors


def test_actor_disconnect_2():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    actor3 = p2n.Actor()
    env.add_actors([actor1, actor2, actor3])

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    actor1.connect(
        actor=actor2,
        location_cls=Home,
    )

    actor1.connect(
        actor=actor2,
        location_cls=School,
    )

    actor1.disconnect(
        actor2,
        location_labels=["Home"],
        remove_locations=True,
        remove_neighbor=True,
        remove_self=True,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], School)

    assert actor1 in env.locations[0].actors

    assert actor2 in env.locations[0].actors

    assert actor3 not in env.locations[0].actors

    actor1.disconnect(
        actor2,
        location_labels=["School"],
        remove_locations=False,
        remove_neighbor=False,
        remove_self=True,
    )

    assert len(env.actors) == 3

    assert isinstance(env.locations[0], School)

    assert actor1 not in env.locations[0].actors

    assert actor2 in env.locations[0].actors

    assert actor3 not in env.locations[0].actors
