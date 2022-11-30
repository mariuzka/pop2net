import random

import agentpy as ap
import popy


def test_model(dataframe_regression):
    class HealthyAgent(popy.Agent):
        def setup(self):
            self.is_infected = False

        def infect(self):
            for contact in self.contacts():
                p_infect = 0.1
                if p_infect < 0.3:
                    contact.is_infected = 1

    class InfectedAgent(HealthyAgent):
        def setup(self):
            self.is_infected = True

    class Population:
        def __init__(self, model) -> None:
            self.model = model

            self.agents = popy.AgentList(model, 5, HealthyAgent)
            self.agents.extend(popy.AgentList(model, 1, InfectedAgent))
            self.agents.shuffle()

            self.model.is_weekday = True

            self.locations = popy.LocationList(
                self,
                [
                    popy.Location(self),
                    popy.Location(self),
                    popy.Location(self),
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

    class MyModel(popy.Model):
        def setup(self):
            self.population = Population(self)

        def step(self):
            self.population.agents.infect()

        def update(self):
            self.population.agents.record("is_infected")

        def end(self):
            pass

    model = MyModel(parameters={"agents": 6, "steps": 2})
    results = model.run()

    # multi index not supported by pytest-regressions
    result = results.variables.HealthyAgent.reset_index()

    assert sum(result.is_infected.values) == 10
