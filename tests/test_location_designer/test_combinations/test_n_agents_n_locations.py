
#%%

import pop2net as p2n
import pytest


@pytest.mark.parametrize("n_actors", [0, 1, 2])
def test_small_n_actors(n_actors):
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    env.add_actors([p2n.Actor() for _ in range(8)])

    class TestLocation(p2n.LocationDesigner):
        n_locations = 4
    
    TestLocation.n_actors = n_actors
    
    creator.create_locations(location_designers=[TestLocation])

    inspector = p2n.NetworkInspector(env=env)
    inspector.plot_bipartite_network()

    assert len(env.locations) == 4
    assert len(env.actors) == 8
    
    for location in env.locations:
        assert len(location.actors) == n_actors