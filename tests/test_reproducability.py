import pytest

import pop2net as p2n


def test_1():
    
    class TestLocation(p2n.LocationDesigner):
        n_actors = 10

        def split(self, actor):
            return actor.id_p2n % 2    

    env1 = p2n.Environment()
    creator1 = p2n.Creator(env=env1, seed=1)
    creator1.create_actors(n=100)
    creator1.create_locations(location_designers=[TestLocation])

    env2 = p2n.Environment()
    creator2 = p2n.Creator(env=env2, seed=1)
    creator2.create_actors(n=100)
    creator2.create_locations(location_designers=[TestLocation])

    assert [actor.id_p2n for actor in env1.locations[0].actors] == [actor.id_p2n for actor in env2.locations[0].actors]