import pop2net as p2n


def test_if_default_weight_is_1():
    # test env.add_actor_to_location()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    env.add_actor_to_location(location=location, actor=actor1, weight=None)
    assert location.get_weight(actor=actor1) == 1
    assert actor1.get_location_weight(location=location) == 1

    # test location.add_actor()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    location.add_actor(actor=actor1, weight=None)
    assert location.get_weight(actor=actor1) == 1
    assert actor1.get_location_weight(location=location) == 1

    # test location.add_actors()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    location.add_actors(actors=[actor1, actor2], weight=None)
    assert location.get_weight(actor=actor1) == 1
    assert location.get_weight(actor=actor2) == 1
    assert actor1.get_location_weight(location=location) == 1
    assert actor2.get_location_weight(location=location) == 1
    assert actor1.get_actor_weight(actor=actor2) == 1
    assert actor2.get_actor_weight(actor=actor1) == 1

    # test location.connect_actors()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    env.connect_actors(actors=[actor1, actor2], location_cls=p2n.Location, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 1
    assert location.get_weight(actor=actor2) == 1
    assert actor1.get_location_weight(location=location) == 1
    assert actor2.get_location_weight(location=location) == 1
    assert actor1.get_actor_weight(actor=actor2) == 1
    assert actor2.get_actor_weight(actor=actor1) == 1

    # test actor.connect()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor1.connect(actor=actor2, location_cls=p2n.Location, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 1
    assert location.get_weight(actor=actor2) == 1
    assert actor1.get_location_weight(location=location) == 1
    assert actor2.get_location_weight(location=location) == 1
    assert actor1.get_actor_weight(actor=actor2) == 1
    assert actor2.get_actor_weight(actor=actor1) == 1


def test_to_set_a_weight_directly():
    # test env.add_actor_to_location()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    env.add_actor_to_location(location=location, actor=actor1, weight=77)
    assert location.get_weight(actor=actor1) == 77
    assert actor1.get_location_weight(location=location) == 77

    # test location.add_actor()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    location.add_actor(actor=actor1, weight=77)
    assert location.get_weight(actor=actor1) == 77
    assert actor1.get_location_weight(location=location) == 77

    # test location.add_actors()
    env = p2n.Environment()
    location = p2n.Location()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    location.add_actors(actors=[actor1, actor2], weight=77)
    assert location.get_weight(actor=actor1) == 77
    assert location.get_weight(actor=actor2) == 77
    assert actor1.get_location_weight(location=location) == 77
    assert actor2.get_location_weight(location=location) == 77
    assert actor1.get_actor_weight(actor=actor2) == 77
    assert actor2.get_actor_weight(actor=actor1) == 77

    # test location.connect_actors()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    env.connect_actors(actors=[actor1, actor2], location_cls=p2n.Location, weight=77)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 77
    assert location.get_weight(actor=actor2) == 77
    assert actor1.get_location_weight(location=location) == 77
    assert actor2.get_location_weight(location=location) == 77
    assert actor1.get_actor_weight(actor=actor2) == 77
    assert actor2.get_actor_weight(actor=actor1) == 77

    # test actor.connect()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor1.connect(actor=actor2, location_cls=p2n.Location, weight=77)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 77
    assert location.get_weight(actor=actor2) == 77
    assert actor1.get_location_weight(location=location) == 77
    assert actor2.get_location_weight(location=location) == 77
    assert actor1.get_actor_weight(actor=actor2) == 77
    assert actor2.get_actor_weight(actor=actor1) == 77


def test_generated_weight():
    class WeightedLocation(p2n.Location):
        def weight(self, actor):
            return 10

    # test env.add_actor_to_location()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    env.add_actor_to_location(location=location, actor=actor1, weight=None)
    assert location.get_weight(actor=actor1) == 10
    assert actor1.get_location_weight(location=location) == 10

    # test location.add_actor()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    location.add_actor(actor=actor1, weight=None)
    assert location.get_weight(actor=actor1) == 10
    assert actor1.get_location_weight(location=location) == 10

    # test location.add_actors()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    location.add_actors(actors=[actor1, actor2], weight=None)
    assert location.get_weight(actor=actor1) == 10
    assert location.get_weight(actor=actor2) == 10
    assert actor1.get_location_weight(location=location) == 10
    assert actor2.get_location_weight(location=location) == 10
    assert actor1.get_actor_weight(actor=actor2) == 10
    assert actor2.get_actor_weight(actor=actor1) == 10

    # test location.connect_actors()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    env.connect_actors(actors=[actor1, actor2], location_cls=WeightedLocation, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 10
    assert location.get_weight(actor=actor2) == 10
    assert actor1.get_location_weight(location=location) == 10
    assert actor2.get_location_weight(location=location) == 10
    assert actor1.get_actor_weight(actor=actor2) == 10
    assert actor2.get_actor_weight(actor=actor1) == 10

    # test actor.connect()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor1.connect(actor=actor2, location_cls=WeightedLocation, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 10
    assert location.get_weight(actor=actor2) == 10
    assert actor1.get_location_weight(location=location) == 10
    assert actor2.get_location_weight(location=location) == 10
    assert actor1.get_actor_weight(actor=actor2) == 10
    assert actor2.get_actor_weight(actor=actor1) == 10


def test_individually_generated_weights():
    class WeightedLocation(p2n.Location):
        def weight(self, actor):
            return actor.w

    # test env.set_weight()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    env.add_actor_to_location(location=location, actor=actor1, weight=1)
    env.add_actor_to_location(location=location, actor=actor2, weight=1)
    env.set_weight(actor=actor1, location=location)
    env.set_weight(actor=actor2, location=location)
    assert location.get_weight(actor=actor1) == 100
    assert actor1.get_location_weight(location=location) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor2.get_location_weight(location=location) == 200

    # test location.set_weight()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    env.add_actor_to_location(location=location, actor=actor1, weight=1)
    env.add_actor_to_location(location=location, actor=actor2, weight=1)
    location.set_weight(actor=actor1)
    location.set_weight(actor=actor2)
    assert location.get_weight(actor=actor1) == 100
    assert actor1.get_location_weight(location=location) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor2.get_location_weight(location=location) == 200

    # test env.add_actor_to_location()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    env.add_actor_to_location(location=location, actor=actor1, weight=None)
    env.add_actor_to_location(location=location, actor=actor2, weight=None)
    assert location.get_weight(actor=actor1) == 100
    assert actor1.get_location_weight(location=location) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor2.get_location_weight(location=location) == 200

    # test location.add_actor()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    location.add_actor(actor=actor1, weight=None)
    location.add_actor(actor=actor2, weight=None)
    assert location.get_weight(actor=actor1) == 100
    assert actor1.get_location_weight(location=location) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor2.get_location_weight(location=location) == 200

    # test location.add_actors()
    env = p2n.Environment()
    location = WeightedLocation()
    env.add_location(location)
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    location.add_actors(actors=[actor1, actor2], weight=None)
    assert location.get_weight(actor=actor1) == 100
    assert actor1.get_location_weight(location=location) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor2.get_location_weight(location=location) == 200
    assert actor1.get_actor_weight(actor=actor2) == 100
    assert actor2.get_actor_weight(actor=actor1) == 100

    # test location.connect_actors()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    env.connect_actors(actors=[actor1, actor2], location_cls=WeightedLocation, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor1.get_location_weight(location=location) == 100
    assert actor2.get_location_weight(location=location) == 200
    assert actor1.get_actor_weight(actor=actor2) == 100
    assert actor2.get_actor_weight(actor=actor1) == 100

    # test actor.connect()
    env = p2n.Environment()
    actor1 = p2n.Actor()
    env.add_actor(actor1)
    actor1.w = 100
    actor2 = p2n.Actor()
    env.add_actor(actor2)
    actor2.w = 200
    actor1.connect(actor=actor2, location_cls=WeightedLocation, weight=None)
    location = env.locations[0]
    assert location.get_weight(actor=actor1) == 100
    assert location.get_weight(actor=actor2) == 200
    assert actor1.get_location_weight(location=location) == 100
    assert actor2.get_location_weight(location=location) == 200
    assert actor1.get_actor_weight(actor=actor2) == 100
    assert actor2.get_actor_weight(actor=actor1) == 100
