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


def test_2a():
    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class WebexMeeting(popy.MagicLocation):
        pass

    model = popy.Model()
    agent_max = Max(model=model)
    agent_marius = Marius(model=model)
    agent_lukas = Lukas(model=model)
    meeting = WebexMeeting(model=model)
    meeting.add_agents(agents=[agent_max, agent_marius, agent_lukas])

    assert len(model.locations) == 1
    assert len(model.agents) == 3

    assert agent_max.neighbors()[0].type == "Marius"
    assert agent_max.neighbors()[1].type == "Lukas"

    assert agent_marius.neighbors()[0].type == "Max"
    assert agent_marius.neighbors()[1].type == "Lukas"

    assert agent_lukas.neighbors()[0].type == "Max"
    assert agent_lukas.neighbors()[1].type == "Marius"


# all in one location
def test_2b():
    model = popy.Model()
    creator = popy.Creator(model)
    
    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class WebexMeeting(popy.MagicLocation):
        pass

    _max = creator.create_agents(agent_class=Max, n=1)[0]
    _marius = creator.create_agents(agent_class=Marius, n=1)[0]
    _lukas = creator.create_agents(agent_class=Lukas, n=1)[0]
    creator.create_locations(location_classes=[WebexMeeting])

    assert len(model.locations) == 1
    assert len(model.agents) == 3

    assert _max.neighbors()[0].type == "Marius"
    assert _max.neighbors()[1].type == "Lukas"

    assert _marius.neighbors()[0].type == "Max"
    assert _marius.neighbors()[1].type == "Lukas"

    assert _lukas.neighbors()[0].type == "Max"
    assert _lukas.neighbors()[1].type == "Marius"


def test_3a():
    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class Meeting1(popy.MagicLocation):
        pass

    class Meeting2(popy.MagicLocation):
        pass

    model = popy.Model()
    agent_max = Max(model=model)
    agent_marius = Marius(model=model)
    agent_lukas = Lukas(model=model)
    meeting1 = Meeting1(model=model)
    meeting2 = Meeting2(model=model)
    meeting1.add_agents([agent_max, agent_marius])
    meeting2.add_agents([agent_marius, agent_lukas])

    assert len(model.locations) == 2
    assert len(model.agents) == 3

    assert agent_max.neighbors(location_classes=[Meeting1])[0].type == "Marius"

    assert agent_marius.neighbors(location_classes=[Meeting1])[0].type == "Max"
    assert agent_marius.neighbors(location_classes=[Meeting2])[0].type == "Lukas"

    assert agent_lukas.neighbors(location_classes=[Meeting2])[0].type == "Marius"


# two Locations
def test_3b():
    model = popy.Model()
    creator = popy.Creator(model)

    class Max(popy.Agent):
        pass

    class Marius(popy.Agent):
        pass

    class Lukas(popy.Agent):
        pass

    class Meeting1(popy.MagicLocation):
        def filter(self, agent):
            return agent.type in ["Max", "Marius"]

    class Meeting2(popy.MagicLocation):
        def filter(self, agent):
            return agent.type in ["Marius", "Lukas"]

    _max = creator.create_agents(agent_class=Max, n=1)
    _marius = creator.create_agents(agent_class=Marius, n=1)
    _lukas = creator.create_agents(agent_class=Lukas, n=1)
    creator.create_locations(location_classes=[Meeting1, Meeting2])

    assert len(model.locations) == 2
    assert len(model.agents) == 3

    assert _max.neighbors(location_classes=[Meeting1])[0][0].type == "Marius"

    assert _marius.neighbors(location_classes=[Meeting1])[0][0].type == "Max"
    assert _marius.neighbors(location_classes=[Meeting2])[0][0].type == "Lukas"

    assert _lukas.neighbors(location_classes=[Meeting2])[0][0].type == "Marius"
