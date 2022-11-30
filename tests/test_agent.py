import popy
import pytest


@pytest.fixture
def model():
    return popy.Model()


@pytest.fixture
def two_locations(model):
    return popy.LocationList(
        model,
        [
            popy.Location(model),
            popy.Location(model),
        ],
    )


def test_agent_creation(model):
    agent = popy.Agent(model)
    assert agent.model == model
    assert list(agent.locations) == []


def test_agentlist_broadcasting(model):
    agents = popy.AgentList(model, [popy.Agent(model), popy.Agent(model)])
    agents.x = 1
    assert sum(agents.x) == 2


def test_agent_locations(model):

    agent = popy.Agent(model)

    location1 = popy.Location(model)
    location2 = popy.Location(model)

    agent.add_location(location1)
    exp = popy.LocationList(model, [location1])
    assert agent.locations == exp

    agent.add_location(location2)
    exp = popy.LocationList(model, [location1, location2])
    assert agent.locations == exp

    assert len(agent.locations) == 2


def test_agents_error_when_location_is_added_twice(model, two_locations):

    agent = popy.Agent(model)
    agent.add_location(two_locations[0])

    with pytest.raises(popy.PopyException):
        agent.add_location(two_locations[0])


@pytest.mark.skip
def test_agent_visits_single_location(model, two_locations):

    agent = popy.Agent(model)
    agent.add_location(two_locations[0])
    agent.visit_locations(model)

    assert list(two_locations.visitors_of_the_day) == [[agent], []]


@pytest.mark.skip
def test_agent_visits_two_locations(model, two_locations):

    agent = popy.Agent(model)
    agent.add_location(two_locations[0])
    agent.add_location(two_locations[1])
    agent.visit_locations(model)

    assert list(two_locations.visitors_of_the_day) == [[agent], [agent]]
