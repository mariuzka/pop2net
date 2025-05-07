from pop2net.agent import Agent
from pop2net.environment import Environment
from pop2net.location import Location


def test_location():
    env = Environment()

    loc = Location()

    agent1 = Agent()
    agent2 = Agent()

    env.add_location(loc)
    env.add_agents([agent1, agent2])

    assert loc.agents == []

    loc.add_agent(agent1, weight=1)

    assert loc.agents == [agent1]

    loc.add_agent(agent2, weight=1)

    assert loc.agents == [agent1, agent2]

    loc.remove_agent(agent1)

    assert loc.agents == [agent2]

    loc.remove_agent(agent2)

    assert loc.agents == []
