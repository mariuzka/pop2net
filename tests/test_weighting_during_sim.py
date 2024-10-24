import pop2net as p2n


def test_weighting_during_sim1():
    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=None)

        def step(self):
            self.location.set_weight(agent=self.agent, weight=None)

        def update(self):
            assert self.location.get_weight(agent=self.agent) == 1
            assert self.agent.get_location_weight(location=self.location) == 1
            assert self.get_weight(location=self.location, agent=self.agent) == 1

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim2():
    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=self.t)

        def step(self):
            self.location.set_weight(agent=self.agent, weight=self.t)

        def update(self):
            assert self.location.get_weight(agent=self.agent) == self.t
            assert self.agent.get_location_weight(location=self.location) == self.t
            assert self.get_weight(location=self.location, agent=self.agent) == self.t

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim3():
    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=10)

        def step(self):
            pass

        def update(self):
            assert self.location.get_weight(agent=self.agent) == 10
            assert self.agent.get_location_weight(location=self.location) == 10
            assert self.get_weight(location=self.location, agent=self.agent) == 10

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim4():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return self.model.t

    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = WeightedLocation(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=None)

        def step(self):
            self.update_weights()

        def update(self):
            assert self.location.get_weight(agent=self.agent) == self.t
            assert self.agent.get_location_weight(location=self.location) == self.t
            assert self.get_weight(location=self.location, agent=self.agent) == self.t

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim5():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return self.model.t

    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = WeightedLocation(model=self)
            self.location2 = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=None)
            self.location2.add_agent(agent=self.agent, weight=None)

        def step(self):
            self.update_weights()

        def update(self):
            assert self.location.get_weight(agent=self.agent) == self.t
            assert self.location2.get_weight(agent=self.agent) == 1

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim6():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return self.model.t

    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = WeightedLocation(model=self)
            self.location2 = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=None)
            self.location2.add_agent(agent=self.agent, weight=10)

        def step(self):
            self.update_weights()

        def update(self):
            assert self.location.get_weight(agent=self.agent) == self.t
            assert self.location2.get_weight(agent=self.agent) == (10 if self.t == 0 else 1)

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim7():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return self.model.t

    class WeightedModel(p2n.Model):
        def setup(self):
            self.location = WeightedLocation(model=self)
            self.location2 = p2n.Location(model=self)
            self.agent = p2n.Agent(model=self)
            self.location.add_agent(agent=self.agent, weight=None)
            self.location2.add_agent(agent=self.agent, weight=10)

        def step(self):
            self.update_weights(location_classes=[WeightedLocation])

        def update(self):
            assert self.location.get_weight(agent=self.agent) == self.t
            assert self.location2.get_weight(agent=self.agent) == 10

    model = WeightedModel()
    model.run(steps=10)
