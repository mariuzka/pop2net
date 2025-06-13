import agentpy as ap
import mesa
import pytest

import pop2net as p2n

N_AGENTS = 2
N_LOCATIONS = 2
N_STEPS = 10

agentlist = {
    "agentpy": ap.AgentList,
    "mesa": mesa.agent.AgentSet,
}


@pytest.mark.parametrize("framework", ["agentpy", "mesa"])
def test_p2n_with_framework(framework: str):
    if framework == "agentpy":
        framework_ = ap
    elif framework == "mesa":
        framework_ = mesa

    class Model(framework_.Model):
        if framework == "agentpy":

            def setup(self):
                self.create_env()
        elif framework == "mesa":

            def __init__(self):
                super().__init__()
                self.create_env()

        def create_env(self):
            self.env = p2n.Environment(model=self, framework=framework)

            # create agents and locations
            if framework == "agentpy":
                locations = framework_.AgentList(model=self, objs=N_LOCATIONS, cls=Location)
                actors = framework_.AgentList(model=self, objs=N_AGENTS, cls=Actor)
            elif framework == "mesa":
                locations = Location.create_agents(model=self, n=N_LOCATIONS)
                actors = Actor.create_agents(model=self, n=N_AGENTS)
            else:
                assert False, "Invalid framework."

            # add/connect actors and locations
            self.env.add_locations(locations=locations)
            self.env.add_actors(actors=actors)
            for location in self.env.locations:
                location.add_actors(self.env.actors)

        def step(self):
            if framework == "agentpy":
                self.env.actors.increase_x()
                self.env.locations.increase_y()
            elif framework == "mesa":
                self.env.actors.do("increase_x")
                self.env.locations.do("increase_y")

    class Actor(p2n.Actor, framework_.Agent):
        if framework == "agentpy":

            def setup(self):
                self.x = 0
        elif framework == "mesa":

            def __init__(self, model):
                super().__init__(model)
                self.x = 0

        def increase_x(self):
            self.x += 1

    class Location(p2n.Location, framework_.Agent):
        if framework == "agentpy":

            def setup(self):
                self.y = 0
        elif framework == "mesa":

            def __init__(self, model):
                super().__init__(model)
                self.y = 0

        def increase_y(self):
            self.y += 1

    # create model
    model = Model()

    # run model
    if framework == "agentpy":
        model.run(steps=N_STEPS)
    elif framework == "mesa":
        for _ in range(N_STEPS):
            model.step()

    # check the number of actors/locations
    assert len(model.env.locations) == N_LOCATIONS
    assert len(model.env.actors) == N_AGENTS

    # check the types of the actors and the agent list
    assert isinstance(model.env.actors, agentlist[framework])
    for actor in model.env.actors:
        assert isinstance(actor, Actor)
        assert isinstance(actor, p2n.Actor)
        assert isinstance(actor, framework_.Agent)

    # check the types of the locations and the location list
    assert isinstance(model.env.locations, agentlist[framework])
    for location in model.env.locations:
        assert isinstance(location, Location)
        assert isinstance(location, p2n.Location)
        assert isinstance(location, framework_.Agent)

    # check if the actors/locations-methods have been executed
    assert all([actor.x == N_STEPS for actor in model.env.actors])
    assert all([location.y == N_STEPS for location in model.env.locations])

    # check location.actors
    for location in model.env.locations:
        assert isinstance(location.actors, agentlist[framework])
        assert len(location.actors) == 2

    # check actors.locations
    for actor in model.env.actors:
        assert isinstance(actor.locations, agentlist[framework])
        assert len(actor.locations) == 2

    # check actor.neighbor()
    for actor in model.env.actors:
        assert isinstance(actor.neighbors(), agentlist[framework])
        assert len(actor.neighbors()) == 1

    # check actor.shared_locations()
    shared_locations = model.env.actors[0].shared_locations(model.env.actors[1])
    assert len(shared_locations) == 2
    assert isinstance(shared_locations, agentlist[framework])

    # check actorList functionality
    carl = model.env.actors[0]
    susi = model.env.actors[1]
    carl.name = "Carl"
    susi.name = "Susi"

    if framework == "agentpy":
        list_with_carl = model.env.actors.select(model.env.actors.name == "Carl")
    elif framework == "mesa":
        list_with_carl = model.env.actors.select(lambda actor: actor.name == "Carl")

    assert isinstance(list_with_carl, agentlist[framework])
    assert len(list_with_carl) == 1
    assert list_with_carl[0].name == "Carl"

    # check Actor.connect()
    class TestLocation(p2n.Location, framework_.Agent):
        pass

    carl.connect(susi, location_cls=TestLocation)
    assert len(carl.shared_locations(susi, location_labels=["TestLocation"])) == 1

    if framework == "agentpy":
        assert len(model.env.locations.select(model.env.locations.label == "TestLocation")) == 1
    elif framework == "mesa":
        assert (
            len(model.env.locations.select(lambda location: location.label == "TestLocation")) == 1
        )

    # check Actor.disconnect()
    carl.disconnect(susi, location_labels=["TestLocation"], remove_locations=True)
    assert len(carl.shared_locations(susi, location_labels=["TestLocation"])) == 0
    if framework == "agentpy":
        assert len(model.env.locations.select(model.env.locations.label == "TestLocation")) == 0
    elif framework == "mesa":
        assert (
            len(model.env.locations.select(lambda location: location.label == "TestLocation")) == 0
        )
