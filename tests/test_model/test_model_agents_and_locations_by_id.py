import pop2net as p2n


def test_1():
    env = p2n.Environment()

    for _ in range(10):
        p2n.Actor(env=env)

    for _ in range(10):
        p2n.Location(env=env)

    for _ in range(10):
        p2n.Actor(env=env)

    for _ in range(10):
        p2n.Location(env=env)

    # check if the actors can be found by id actors_dict
    for actor in env.actors:
        assert actor is env.actors_by_id[actor.id]

    # check if the locations can be found by id locations_dict
    for location in env.locations:
        assert location is env.locations_by_id[location.id]

    # assert that the actors cannot be found by id in the normal actor_list
    assert not all(actor is env.actors[actor.id] for actor in env.actors)

    # assert that the locations cannot be found by id in the normal locations_list
    assert not all(actor is env.actors[actor.id] for actor in env.actors)
