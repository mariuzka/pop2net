import pop2net as p2n


def test_1a():
    env = p2n.Environment()

    class Max(p2n.Actor):
        pass

    class Marius(p2n.Actor):
        pass

    class Lukas(p2n.Actor):
        pass

    class Meeting1(p2n.Location):
        pass

    class Meeting2(p2n.Location):
        pass

    actor_max = Max()
    actor_marius = Marius()
    actor_lukas = Lukas()
    meeting1 = Meeting1()
    meeting2 = Meeting2()

    env.add_actors([actor_max, actor_marius, actor_lukas])
    env.add_locations([meeting1, meeting2])
    meeting1.add_actors([actor_max, actor_marius])
    meeting2.add_actors([actor_marius, actor_lukas])

    assert len(env.locations) == 2
    assert len(env.actors) == 3

    assert len(actor_max.shared_locations(actor=actor_marius)) == 1
    assert actor_max.shared_locations(actor=actor_marius)[0].label == "Meeting1"
    assert not bool(actor_max.shared_locations(actor=actor_lukas))

    assert len(actor_marius.shared_locations(actor=actor_max)) == 1
    assert actor_marius.shared_locations(actor=actor_max)[0].label == "Meeting1"
    assert len(actor_marius.shared_locations(actor=actor_lukas)) == 1
    assert actor_marius.shared_locations(actor=actor_lukas)[0].label == "Meeting2"

    assert len(actor_lukas.shared_locations(actor=actor_marius)) == 1
    assert actor_lukas.shared_locations(actor=actor_marius)[0].label == "Meeting2"
    assert len(actor_lukas.shared_locations(actor=actor_max)) == 0
    assert not bool(actor_lukas.shared_locations(actor=actor_max))


def test_1b():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Max(p2n.Agent):
        pass

    class Marius(p2n.Agent):
        pass

    class Lukas(p2n.Agent):
        pass

    class Meeting1(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.type in ["Max", "Marius"]

    class Meeting2(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.type in ["Marius", "Lukas"]

    _max = creator.create_agents(agent_class=Max, n=1)[0]
    _marius = creator.create_agents(agent_class=Marius, n=1)[0]
    _lukas = creator.create_agents(agent_class=Lukas, n=1)[0]
    creator.create_locations(location_designers=[Meeting1, Meeting2])

    assert len(model.locations) == 2
    assert len(model.agents) == 3

    assert _max.shared_locations(agent=_marius)[0].label == "Meeting1"
    assert not bool(_max.shared_locations(agent=_lukas))

    assert _marius.shared_locations(agent=_max)[0].label == "Meeting1"
    assert _marius.shared_locations(agent=_lukas)[0].label == "Meeting2"

    assert _lukas.shared_locations(agent=_marius)[0].label == "Meeting2"
    assert not bool(_lukas.shared_locations(agent=_max))
