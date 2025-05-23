import agentpy as ap

import pop2net as p2n


def test_weighting_during_sim1():
    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment()
            self.location = p2n.Location()
            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)
            self.env.add_location(self.location)
            self.location.add_actor(actor=self.actor, weight=None)

        def step(self):
            self.location.set_weight(actor=self.actor, weight=None)

        def update(self):
            assert self.location.get_weight(actor=self.actor) == 1
            assert self.actor.get_location_weight(location=self.location) == 1
            assert self.env.get_weight(location=self.location, actor=self.actor) == 1

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim2():
    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment()
            self.location = p2n.Location()
            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)
            self.env.add_location(self.location)
            self.location.add_actor(actor=self.actor, weight=self.t)

        def step(self):
            self.location.set_weight(actor=self.actor, weight=self.t)

        def update(self):
            assert self.location.get_weight(actor=self.actor) == self.t
            assert self.actor.get_location_weight(location=self.location) == self.t
            assert self.env.get_weight(location=self.location, actor=self.actor) == self.t

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim3():
    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self)

            self.location = p2n.Location()
            self.env.add_location(self.location)

            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)

            self.location.add_actor(actor=self.actor, weight=10)

        def step(self):
            pass

        def update(self):
            assert self.location.get_weight(actor=self.actor) == 10
            assert self.actor.get_location_weight(location=self.location) == 10
            assert self.env.get_weight(location=self.location, actor=self.actor) == 10

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim4():
    class WeightedLocation(p2n.Location):
        def weight(self, actor):
            return self.env.model.t

    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self)

            self.location = WeightedLocation()
            self.env.add_location(self.location)

            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)

            self.location.add_actor(actor=self.actor, weight=None)

        def step(self):
            self.env.update_weights()

        def update(self):
            assert self.location.get_weight(actor=self.actor) == self.t
            assert self.actor.get_location_weight(location=self.location) == self.t
            assert self.env.get_weight(location=self.location, actor=self.actor) == self.t

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim5():
    class WeightedLocation(p2n.Location):
        def weight(self, actor):
            return self.env.model.t

    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self)
            self.location = WeightedLocation()
            self.env.add_location(self.location)
            self.location2 = p2n.Location()
            self.env.add_location(self.location2)
            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)
            self.location.add_actor(actor=self.actor, weight=None)
            self.location2.add_actor(actor=self.actor, weight=None)

        def step(self):
            self.env.update_weights()

        def update(self):
            assert self.location.get_weight(actor=self.actor) == self.t
            assert self.location2.get_weight(actor=self.actor) == 1

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim6():
    class WeightedLocation(p2n.Location):
        def weight(self, actor):
            return self.env.model.t

    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self)
            self.location = WeightedLocation()
            self.env.add_location(self.location)
            self.location2 = p2n.Location()
            self.env.add_location(self.location2)
            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)
            self.location.add_actor(actor=self.actor, weight=None)
            self.location2.add_actor(actor=self.actor, weight=10)

        def step(self):
            self.env.update_weights()

        def update(self):
            assert self.location.get_weight(actor=self.actor) == self.t
            assert self.location2.get_weight(actor=self.actor) == (10 if self.t == 0 else 1)

    model = WeightedModel()
    model.run(steps=10)


def test_weighting_during_sim7():
    class WeightedLocation(p2n.Location):
        label = "WeightedLocation"

        def weight(self, actor):
            return self.env.model.t

    class WeightedModel(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self)
            self.location = WeightedLocation()
            self.env.add_location(self.location)
            self.location2 = p2n.Location()
            self.env.add_location(self.location2)
            self.actor = p2n.Actor()
            self.env.add_actor(self.actor)
            self.location.add_actor(actor=self.actor, weight=None)
            self.location2.add_actor(actor=self.actor, weight=10)

        def step(self):
            self.env.update_weights(location_labels=["WeightedLocation"])

        def update(self):
            assert self.location.get_weight(actor=self.actor) == self.t
            assert self.location2.get_weight(actor=self.actor) == 10

    model = WeightedModel()
    model.run(steps=10)
