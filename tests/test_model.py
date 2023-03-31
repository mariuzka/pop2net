import random

import agentpy as ap
import popy
import pytest


@pytest.mark.skip
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

    class MyModel(popy.Model):
        def setup(self):
            self.agents = popy.AgentList(self, 5, HealthyAgent)
            self.agents.extend(popy.AgentList(self, 1, InfectedAgent))
            self.agents.shuffle()

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

        def step(self):
            self.agents.infect()  # type: ignore

        def update(self):
            self.agents.record("is_infected")  # type: ignore

        def end(self):
            pass

    model = MyModel(parameters={"agents": 6, "steps": 2})
    results = model.run()

    # multi index not supported by pytest-regressions
    result = results.variables.HealthyAgent.reset_index()

    assert sum(result.is_infected.values) == 10
