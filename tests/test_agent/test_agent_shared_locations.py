import pop2net as p2n

def test_1():
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
        location_cls=Home
    )

    actor2.connect(
        actor=actor3,
        location_cls=School
    )

    actor1_2_shared = actor1.shared_locations(
        actor=actor2,
        location_labels=None
    )
    actor2_1_shared = actor2.shared_locations(
        actor=actor1,
        location_labels=None
    )
    actor2_3_shared = actor2.shared_locations(
        actor=actor3,
        location_labels=None
    )
    actor3_2_shared = actor3.shared_locations(
        actor=actor2,
        location_labels=None
    )
    actor1_3_shared = actor1.shared_locations(
        actor=actor3,
        location_labels=None
    )
    actor3_1_shared = actor3.shared_locations(
        actor=actor1,
        location_labels=None
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

    # shared location asserts
    assert len(actor1_2_shared) == 1
    assert len(actor2_1_shared) == 1
    assert len(actor2_3_shared) == 1
    assert len(actor3_2_shared) == 1
    assert len(actor1_3_shared) == 0
    assert len(actor3_1_shared) == 0

    assert (isinstance(actor1_2_shared[0], Home))
    assert (isinstance(actor2_1_shared[0], Home))
    assert (isinstance(actor2_3_shared[0], School))
    assert (isinstance(actor3_2_shared[0], School))


# TODO Location_designer version when its ready