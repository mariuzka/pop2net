import pop2net as p2n


def test_1():
    """Tests if mutate() can be used to create locations with varying number of actors while
    ensuring that actors are only assigned to one mutation of the location designer."""

    class TestActor(p2n.Actor):
        def __init__(self, env):
            super().__init__(env)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 1

        def filter(self, actor):
            """Prevent actors from being assigned to multiple locations of this type."""
            if not any(label.startswith("TestLocation") for label in actor.location_labels):
                return True
            else:
                return False

        def mutate(self):
            """Create multiple locations with varying number of actors."""
            return {"n_actors": [2, 2, 2, 4]}

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    for _ in range(10):
        TestActor(env=env)

    creator.create_locations(location_designers=[TestLocation])

    assert len(env.actors) == 10
    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 4
