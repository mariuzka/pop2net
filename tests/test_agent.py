import pytest

import src


@pytest.fixture
def model():
    return src.Model()


@pytest.fixture
def two_locations(model):
    return src.LocationList(
        model,
        [
            src.Location(model, category="home"),
            src.Location(model, category="work"),
        ],
    )


def test_agent_creation(model):
    agent = src.Agent(model)
    assert agent._model == model
    assert agent.contact_diary == src.AgentList(model)
    assert list(agent.contact_diary) == []
    assert list(agent.locations) == []


def test_agent_locations(model):

    agent = src.Agent(model)

    location1 = src.Location(model, category="home")
    location2 = src.Location(model, category="work")

    agent.add_location(location1)
    exp = src.LocationList(model, [location1])
    assert agent.locations == exp

    agent.add_location(location2)
    exp = src.LocationList(model, [location1, location2])
    assert agent.locations == exp

    assert len(agent.locations) == 2


def test_agents_error_when_location_is_added_twice(model, two_locations):

    agent = src.Agent(model)
    agent.add_location(two_locations[0])

    with pytest.raises(src.PopyException):
        agent.add_location(two_locations[0])


def test_agent_visits_single_location(model, two_locations):

    agent = src.Agent(model)
    agent.add_location(two_locations[0])
    agent.visit_locations(model)

    assert list(two_locations.visitors_of_the_day) == [[agent], []]


def test_agent_visits_two_locations(model, two_locations):

    agent = src.Agent(model)
    agent.add_location(two_locations[0])
    agent.add_location(two_locations[1])
    agent.visit_locations(model)

    assert list(two_locations.visitors_of_the_day) == [[agent], [agent]]
