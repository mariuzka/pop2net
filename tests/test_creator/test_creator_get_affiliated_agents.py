import pop2net as p2n


def test_0():
    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(5):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(5):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class School(p2n.LocationDesigner):
        pass

    school = School()
    env.add_location(school)

    assert not all(
        actor.gender == "w"
        for actor in creator._get_affiliated_actors(actors=env.actors, dummy_location=school)
    )

    env = p2n.Environment()
    creator = p2n.Creator(env)

    for _ in range(5):
        actor = p2n.Actor()
        actor.gender = "w"
        env.add_actor(actor)

    for _ in range(5):
        actor = p2n.Actor()
        actor.gender = "m"
        env.add_actor(actor)

    class School(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.gender == "w"

    school = School()
    env.add_location(school)

    assert all(
        actor.gender == "w"
        for actor in creator._get_affiliated_actors(actors=env.actors, dummy_location=school)
    )
