import pop2net as p2n


def test_1():
    """Tests if mutate() can be used to create locations with varying number of agents while
    ensuring that agents are only assigned to one mutation of the location designer."""

    class TestAgent(p2n.Agent):
        def __init__(self, model):
            super().__init__(model)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 1

        def filter(self, agent):
            """Prevent agents from being assigned to multiple locations of this type."""
            if not any(label.startswith("TestLocation") for label in agent.location_labels):
                return True
            else:
                return False

        def mutate(self):
            """Create multiple locations with varying number of agents."""
            return {"n_agents": [2, 2, 2, 4]}

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    for _ in range(10):
        TestAgent(model=model)

    creator.create_locations(location_designers=[TestLocation])

    assert len(model.agents) == 10
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 4
