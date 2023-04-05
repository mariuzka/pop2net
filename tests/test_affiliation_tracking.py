import popy
import pytest

# Laufzeit mit ca. 4.3 GHz: ca. 29-30s

def test_affiliation_tracking():
    class Agent(popy.Agent):
        def setup(self):
            self.n_locations = 0

        def count_locations(self):
            self.n_locations = len(self.locations)

    class Location(popy.Location):
        def setup(self):
            self.n_agents = 0

        def count_agents(self):
            self.n_agents = len(self.agents)

    class Model(popy.Model):
        def setup(self):
            N_AGENTS = 1000
            self.agents = popy.AgentList(self, N_AGENTS, Agent)
            self.locations = popy.LocationList(self, N_AGENTS, Location)

            for i, location in enumerate(self.locations):
                location.add_agent(self.agents[i])

        def step(self):
            self.agents.count_locations()  # type: ignore
            self.locations.count_agents()  # type: ignore


    model = Model(parameters={"steps": 5})
    model.run()

    for agent in model.agents:
        assert agent.n_locations == 1

    for location in model.locations:
        assert location.n_agents == 1


if __name__ == "__main__":
    test_affiliation_tracking()
