import random

import pytest

import popy


def test_model():
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
            popy.AgentList(self, 5, HealthyAgent)
            self.agents.extend(popy.AgentList(self, 1, InfectedAgent))
            self.agents.shuffle()

            popy.LocationList(self, 3, popy.Location)

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


@pytest.mark.parametrize(("n_agents", "exp_n_edges"), [(100, 1832), (111, 2298), (115, 2460)])
def test_model_network_export_simple_n_agents(n_agents, exp_n_edges):
    random.seed(42)

    class MovingAgent(popy.Agent):
        def move(self):
            old_location = self.locations[0]
            old_location.remove_agent(self)

            while True:
                new_location = random.choice(self.model.locations)
                if new_location not in self.locations:
                    break
            new_location.add_agent(self)

    class MyModel(popy.Model):
        def setup(self):
            popy.AgentList(self, n_agents, MovingAgent)
            popy.LocationList(self, 10, popy.Location)

            # assign agents to locations
            for agent in self.agents:
                locations = random.sample(self.locations, 2)
                for location in locations:
                    location.add_agent(agent)

        def step(self):
            self.agents.move()  # type: ignore

    model = MyModel(parameters={"steps": 2})
    model.run()
    graph = model.export_agent_network()

    assert graph.number_of_nodes() == n_agents
    assert graph.number_of_edges() == exp_n_edges
