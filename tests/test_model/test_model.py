import random

import pytest

import pop2net as p2n


def test_model():
    class HealthyActor(p2n.Actor):
        def setup(self):
            self.is_infected = False

        def infect(self):
            for contact in self.neighbors():
                p_infect = 0.1
                if p_infect < 0.3:
                    contact.is_infected = 1

    class InfectedActor(HealthyActor):
        def setup(self):
            self.is_infected = True

    class MyEnvironment(p2n.Environment):
        def setup(self):
            p2n.ActorList(self, 5, HealthyActor)
            self.actors.extend(p2n.ActorList(self, 1, InfectedActor))
            self.actors.shuffle()

            p2n.LocationList(self, 3, p2n.Location)

            # home 1
            self.locations[0].add_actor(self.actors[0])
            self.locations[0].add_actor(self.actors[1])
            self.locations[0].add_actor(self.actors[2])

            # school
            self.locations[1].add_actor(self.actors[2])
            self.locations[1].add_actor(self.actors[3])

            # home 2
            self.locations[2].add_actor(self.actors[3])
            self.locations[2].add_actor(self.actors[4])
            self.locations[2].add_actor(self.actors[5])

        def step(self):
            self.actors.infect()  # type: ignore

        def update(self):
            self.actors.record("is_infected")  # type: ignore

        def end(self):
            pass

    env = MyEnvironment(parameters={"actors": 6, "steps": 2})
    results = env.run()

    # multi index not supported by pytest-regressions
    result = results.variables.HealthyActor.reset_index()

    assert sum(result.is_infected.values) == 10


@pytest.mark.parametrize(("n_actors", "exp_n_edges"), [(100, 1832), (111, 2298), (115, 2460)])
def test_model_network_export_simple_n_actors(n_actors, exp_n_edges):
    random.seed(42)

    class MovingActor(p2n.Actor):
        def move(self):
            old_location = self.locations[0]
            old_location.remove_actor(self)

            while True:
                new_location = random.choice(self.env.locations)
                if new_location not in self.locations:
                    break
            new_location.add_actor(self)

    class MyEnvironment(p2n.Environment):
        def setup(self):
            p2n.ActorList(self, n_actors, MovingActor)
            p2n.LocationList(self, 10, p2n.Location)

            # assign actors to locations
            for actor in self.actors:
                locations = random.sample(self.locations, 2)
                for location in locations:
                    location.add_actor(actor)

        def step(self):
            self.actors.move()  # type: ignore

    env = MyEnvironment(parameters={"steps": 2})
    env.run()
    graph = env.export_actor_network()

    assert graph.number_of_nodes() == n_actors
    assert graph.number_of_edges() == exp_n_edges
