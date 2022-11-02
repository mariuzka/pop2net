import random

import agentpy as ap

import src


def test_model(dataframe_regression):
    class Population:
        def __init__(self, model) -> None:
            self.model = model
            self.agents = src.AgentList(model, model.p.agents, MyAgent)
            self.locations = src.LocationList(
                self,
                [
                    src.Location(self, category="home"),
                    src.Location(self, category="school"),
                    src.Location(self, category="home"),
                ],
            )

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

        def update(self) -> None:
            self.agents.visit_locations(self.model)
            self.locations.connect_visitors()

    class MyAgent(src.Agent):
        def setup(self):
            self.n_contacts = 0

        def do_stuff(self):
            self.n_contacts += 1

        @property
        def len_contacts(self):
            return len(self.contact_diary)

    class MyModel(src.Model):
        def setup(self):
            self.population = Population(self)

        def step(self):
            self.population.agents.do_stuff()

        def update(self):
            # record n_contacts
            self.population.agents.record("contacts")
            self.population.agents.record("n_contacts")
            self.population.agents.record("len_contacts")

        def end(self):
            pass

    model = MyModel(parameters={"agents": 6, "steps": 3})
    results = model.run()

    # multi index not supported by pytest-regressions
    result = results.variables.MyAgent.reset_index()

    # lists cannot be saved in pytest-regressions
    result["contacts"] = result.contacts.apply(str)

    dataframe_regression.check(result)
