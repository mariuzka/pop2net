import pytest
from popy import AgentList
from popy.agent import Agent
from popy.location import Location
from popy.model import Model


@pytest.fixture(scope="module")
def two_agent_location():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1, visit_weight=1)
    loc.add_agent(agent2, visit_weight=1)

    return loc


def test_agent_property():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1)
    loc.add_agent(agent2)

    assert AgentList(model, [agent1, agent2]) == loc.agents


def test_create_location():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1)
    loc.add_agent(agent2)

    neighbours = list(loc.neighbors(agent1))
    assert neighbours


def test_location_size():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)

    assert loc.n_affiliated_agents == 0
    loc.add_agent(agent1)
    assert loc.n_affiliated_agents == 1
    loc.add_agent(agent2)
    assert loc.n_affiliated_agents == 2
    loc.remove_agent(agent1)
    assert loc.n_affiliated_agents == 1
    loc.remove_agent(agent2)
    assert loc.n_affiliated_agents == 0
