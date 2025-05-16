import pop2net as p2n

# Laufzeit mit ca. 4.3 GHz: ca. 29-30s


def test_affiliation_tracking():
    class Actor(p2n.Actor):
        def setup(self):
            self.n_locations = 0

        def count_locations(self):
            self.n_locations = len(self.locations)

    class Location(p2n.Location):
        def setup(self):
            self.n_actors = 0

        def count_actors(self):
            self.n_actors = len(self.actors)

    class Environment(p2n.Environment):
        def setup(self):
            n_actors = 1000
            self.add_actors(p2n.ActorList(self, n_actors, Actor))
            self.add_locations(p2n.LocationList(self, n_actors, Location))

            for i, location in enumerate(self.locations):
                location.add_actor(self.actors[i])

        def step(self):
            self.actors.count_locations()  # type: ignore
            self.locations.count_actors()  # type: ignore

    env = Environment(parameters={"steps": 5})
    env.run()

    for actor in env.actors:
        assert actor.n_locations == 1

    for location in env.locations:
        assert location.n_actors == 1


if __name__ == "__main__":
    test_affiliation_tracking()
