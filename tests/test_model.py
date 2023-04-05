import random

import agentpy as ap
import popy
import pytest


def test_model(dataframe_regression):
    class HealthyAgent(popy.Agent):
        def setup(self):
            self.is_infected = False

        def infect(self):
            for contact in self.neighbors():
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

            self.locations = popy.LocationList(self, 3, popy.Location)

            # home 1
            self.locations[0].add_agent(self.agents[0])
            self.locations[0].add_agent(self.agents[1])
            self.locations[0].add_agent(self.agents[2])

            # school
            self.locations[1].add_agent(self.agents[2])
            self.locations[1].add_agent(self.agents[3])

            # home 2
            self.locations[2].add_agent(self.agents[3])
            self.locations[2].add_agent(self.agents[4])
            self.locations[2].add_agent(self.agents[5])

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


@pytest.mark.parametrize("n_agents", [10, 23, 41])
def test_model_network_export_simple_n_agents(n_agents):
    class MovingAgent(popy.Agent):
        def move(self):
            # old_location = self.locations[0]
            # old_location.remove_agent(self)
            new_location = random.choice(self.model.locations)
            new_location.add_agent(self)

    class MyModel(popy.Model):
        def setup(self):
            self.agents = popy.AgentList(self, n_agents, MovingAgent)
            self.locations = popy.LocationList(self, 3, popy.Location)

            # assign agents to locations
            for agent in self.agents:
                n_loc = random.randint(1, 2)
                for _ in range(n_loc):
                    location = random.choice(self.locations)
                    location.add_agent(agent)

        def step(self):
            self.agents.move()  # type: ignore

    model = MyModel(parameters={"steps": 2})
    model.run()
    graph = model.export_network()

    assert graph.number_of_nodes() == n_agents
