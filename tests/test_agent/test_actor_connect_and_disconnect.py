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


def test_location_label_without_class():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])

    actor1.connect(
        actor=actor2,
        location_cls=None,
        location_label="Library",
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Library"])) == 1


def test_location_label_with_class():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])

    class Home(p2n.Location):
        pass

    actor1.connect(
        actor=actor2,
        location_cls=Home,
        location_label="Library",
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert len(actor1.shared_locations(actor=actor2, location_labels=["Library"])) == 1


def test_location_cls_is_None_and_model_is_None():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])

    actor1.connect(
        actor=actor2,
        location_cls=None,
        weight=2,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert actor1.get_actor_weight(actor2) == 2


def test_location_cls_is_None_and_model_is_not_None():
    class Model:
        pass

    model = Model()
    env = p2n.Environment(model=model)
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])

    actor1.connect(
        actor=actor2,
        location_cls=None,
        weight=2,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert actor1.get_actor_weight(actor2) == 2


def test_location_cls_is_not_None_and_model_is_not_None():
    class Model:
        pass

    class Location(p2n.Location):
        pass

    model = Model()
    env = p2n.Environment(model=model)
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])

    actor1.connect(
        actor=actor2,
        location_cls=Location,
        weight=2,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert actor1.get_actor_weight(actor2) == 2


def test_framework_is_not_None():
    import mesa

    class Model(mesa.Model):
        pass

    class Location(p2n.Location, mesa.Agent):
        pass

    class Agent(p2n.Actor, mesa.Agent):
        pass

    model = Model()
    env = p2n.Environment(model=model, framework="mesa")
    actor1 = Agent(model=model)
    actor2 = Agent(model=model)
    env.add_actors([actor1, actor2])

    actor1.connect(
        actor=actor2,
        location_cls=Location,
        weight=2,
    )

    assert len(actor1.shared_locations(actor=actor2)) == 1
    assert actor1.get_actor_weight(actor2) == 2
