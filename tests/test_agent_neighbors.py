import popy


def test_1():
    model = popy.Model()
    agent1 = popy.Agent(model)
    agent2 = popy.Agent(model)
    location1 = popy.Location(model)

    location1.add_agents([agent1, agent2])

    assert len(model.agents) == 2
    assert len(model.locations) == 1

    assert len(agent1.neighbors()) == 1
    assert agent1.neighbors()[0] is agent2

    assert len(agent2.neighbors()) == 1
    assert agent2.neighbors()[0] is agent1
