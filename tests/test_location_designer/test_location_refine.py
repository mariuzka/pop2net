import pytest

import pop2net as p2n


@pytest.mark.skip
def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 3

        def refine(self):
            actor = p2n.Actor(env=self.env)
            self.add_actor(actor)

    creator.create_locations(location_classes=[ClassRoom])

    assert len(env.locations) == 3
    assert len(env.actors) == 3

    for location in env.locations:
        assert len(location.actors) == 1


@pytest.mark.skip
def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    for _ in range(10):
        p2n.Actor(env=env)

    class ClassRoom(p2n.LocationDesigner):
        n_locations = 2

        def refine(self):
            self.remove_actor(self.actors[0])

    creator.create_locations(location_classes=[ClassRoom])

    assert len(env.locations) == 2
    assert len(env.actors) == 10

    for location in env.locations:
        assert len(location.actors) == 4
