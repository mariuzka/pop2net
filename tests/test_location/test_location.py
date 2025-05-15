from pop2net.actor import Actor
from pop2net.environment import Environment
from pop2net.location import Location


def test_location():
    env = Environment()

    loc = Location()

    actor1 = Actor()
    actor2 = Actor()

    env.add_location(loc)
    env.add_actors([actor1, actor2])

    assert loc.actors == []

    loc.add_actor(actor1, weight=1)

    assert loc.actors == [actor1]

    loc.add_actor(actor2, weight=1)

    assert loc.actors == [actor1, actor2]

    loc.remove_actor(actor1)

    assert loc.actors == [actor2]

    loc.remove_actor(actor2)

    assert loc.actors == []
