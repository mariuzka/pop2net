import popy


def test_0():
    model = popy.Model()
    creator = popy.Creator(model=model)

    for _ in range(5):
        agent = popy.Agent(model=model)
        agent.gender = "w"

    for _ in range(5):
        agent = popy.Agent(model=model)
        agent.gender = "m"

    class School(popy.MagicLocation):
        pass

    school = School(model=model)

    assert not all(
        agent.gender == "w"
        for agent in creator._get_affiliated_agents(agents=model.agents, dummy_location=school)
    )

    class School(popy.MagicLocation):
        def filter(self, agent):
            return agent.gender == "w"

    school = School(model=model)

    assert all(
        agent.gender == "w"
        for agent in creator._get_affiliated_agents(agents=model.agents, dummy_location=school)
    )
