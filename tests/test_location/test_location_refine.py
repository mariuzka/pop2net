import popy


def test_1():
    model = popy.Model()
    creator = popy.Creator(model=model)

    class ClassRoom(popy.MagicLocation):
        n_locations = 3

        def refine(self):
            agent = popy.Agent(model=self.model)
            self.add_agent(agent)

    creator.create_locations(location_classes=[ClassRoom])

    assert len(model.locations) == 3
    assert len(model.agents) == 3

    for location in model.locations:
        assert len(location.agents) == 1


def test_2():
    model = popy.Model()
    creator = popy.Creator(model=model)

    for _ in range(10):
        popy.Agent(model=model)

    class ClassRoom(popy.MagicLocation):
        n_locations = 2

        def refine(self):
            self.remove_agent(self.agents[0])

    creator.create_locations(location_classes=[ClassRoom])

    assert len(model.locations) == 2
    assert len(model.agents) == 10

    for location in model.locations:
        assert len(location.agents) == 4
