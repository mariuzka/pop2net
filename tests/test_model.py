import random

import agentpy as ap

from src.agent import PopyAgent
from src.environment import PopyEnvironment
from src.location import PopyLocation
from src.model import PopyModel


def test_model(data_regression):
    class MyAgent(PopyAgent):
        def setup(self):
            self.n_contacts = 0

        def do_stuff(self):
            self.n_contacts += 1

        @property
        def len_contacts(self):
            return len(self.contact_diary)

    class MyModel(PopyModel):
        def setup(self):
            # initiate a list of agents
            self.agents = ap.AgentList(self, self.p.agents, MyAgent)
            self.locations = [
                PopyLocation(self, category="home"),
                PopyLocation(self, category="school"),
                PopyLocation(self, category="home"),
            ]
            # home 1
            self.agents[0].add_location(self.locations[0])
            self.agents[1].add_location(self.locations[0])
            self.agents[2].add_location(self.locations[0])

            # school
            self.agents[2].add_location(self.locations[1])
            self.agents[3].add_location(self.locations[1])

            # home 2
            self.agents[3].add_location(self.locations[2])
            self.agents[4].add_location(self.locations[2])
            self.agents[5].add_location(self.locations[2])

        def step(self):
            self.agents.do_stuff()

        def update(self):
            # record n_contacts
            self.agents.record("my_diary")
            self.agents.record("n_contacts")
            self.agents.record("len_contacts")

        def end(self):
            pass

    model = MyModel(parameters={"agents": 6, "steps": 3, "seed": 43})
    results = model.run()

    result = results.variables.MyAgent.to_dict()
    data_regression.check(result)
