import networkx as nx

import pop2net as p2n


def test_p_transfer():
    """Tests whether a MagicLocation can access the parameters p of the model
    when the Creator is working."""

    class TestLocation(p2n.LocationDesigner):
        def __init__(self, model: p2n.Model) -> None:
            super().__init__(model)
            self.nxgraph = nx.cycle_graph(n=self.p["n_agents"])

    class TestModel(p2n.Model):
        def setup(self):
            self.creator = p2n.Creator(model=self)
            self.creator.create_agents(n=self.p["n_agents"])
            self.creator.create_locations(location_designers=[TestLocation])

    params = {"n_agents": 100}

    model = TestModel(parameters=params)
    model.run(steps=3)

    assert len(model.agents) == 100
