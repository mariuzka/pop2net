import popy


def test_1():
    model = popy.Model()

    for _ in range(10):
        popy.Agent(model=model)

    for _ in range(10):
        popy.Location(model=model)

    for _ in range(10):
        popy.Agent(model=model)

    for _ in range(10):
        popy.Location(model=model)

    # check if the agents can be found by id agents_dict
    for agent in model.agents:
        assert agent is model.agents_by_id[agent.id]

    # check if the locations can be found by id locations_dict
    for location in model.locations:
        assert location is model.locations_by_id[location.id]

    # assert that the agents cannot be found by id in the normal agent_list
    assert not all(agent is model.agents[agent.id] for agent in model.agents)

    # assert that the locations cannot be found by id in the normal locations_list
    assert not all(agent is model.agents[agent.id] for agent in model.agents)
