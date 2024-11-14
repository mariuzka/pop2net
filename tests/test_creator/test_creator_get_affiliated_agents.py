import pop2net as p2n


def test_0():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    for _ in range(5):
        agent = p2n.Agent(model=model)
        agent.gender = "w"

    for _ in range(5):
        agent = p2n.Agent(model=model)
        agent.gender = "m"

    class School(p2n.LocationDesigner):
        pass

    school = School(model=model)

    assert not all(
        agent.gender == "w"
        for agent in creator._get_affiliated_agents(agents=model.agents, dummy_location=school)
    )

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    for _ in range(5):
        agent = p2n.Agent(model=model)
        agent.gender = "w"

    for _ in range(5):
        agent = p2n.Agent(model=model)
        agent.gender = "m"

    class School(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.gender == "w"

    school = School(model=model)

    assert all(
        agent.gender == "w"
        for agent in creator._get_affiliated_agents(agents=model.agents, dummy_location=school)
    )
