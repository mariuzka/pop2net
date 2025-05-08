import agentpy as ap
import networkx as nx
import pytest

import pop2net as p2n


@pytest.mark.parametrize("location_class", ["default", "custom"])
def test_agentpy_p_transfer_in_location_designer(location_class):
    """Tests whether a MagicLocation can access the parameters p of the model
    when the Creator is working."""

    class TestActor(p2n.Actor, ap.Agent):
        pass

    class TestLocation(p2n.Location, ap.Agent):
        pass

    if location_class == "default":

        class TestLocationDesigner(p2n.LocationDesigner):
            def setup(self):
                self.nxgraph = nx.cycle_graph(n=self.p["n_actors"])
    elif location_class == "custom":

        class TestLocationDesigner(p2n.LocationDesigner):
            location_class = TestLocation

            def setup(self):
                self.nxgraph = nx.cycle_graph(n=self.p["n_actors"])
    else:
        assert False

    class TestModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self, framework="agentpy")
            self.creator = p2n.Creator(env=self.env)
            self.creator.create_actors(n=self.p["n_actors"], actor_class=TestActor)
            self.creator.create_locations(location_designers=[TestLocationDesigner])

    params = {"n_actors": 100}

    model = TestModel(parameters=params)
    model.run(steps=3)

    assert len(model.env.actors) == 100
