import pandas as pd

import pop2net as p2n


def test_1():
    # bridge+nest with recycle=False
    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Restaurant(p2n.MagicLocation):
        pass

    class Table(p2n.MagicLocation):

        recycle = False

        def bridge(self, agent):
            return agent.gender

        def nest(self):
            return Restaurant

    creator.create_locations(location_classes=[Table, Restaurant])

    assert len(model.agents) == 5
    assert len(model.locations) == 3
    assert sum(location.type == "Table" for location in model.locations) == 2
    assert sum(location.type == "Restaurant" for location in model.locations) == 1

    for location in model.locations:
        if location.type == "Restaurant":
            assert len(location.agents) == 5
            assert [agent.gender for agent in location.agents].count("m") == 2
            assert [agent.gender for agent in location.agents].count("w") == 3
        if location.type == "Classroom":
            assert len(location.agents) == 2
            assert [agent.gender for agent in location.agents].count("m") == 1
            assert [agent.gender for agent in location.agents].count("w") == 1


def test_2():
    # bridge+nest with recycle=True
    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Restaurant(p2n.MagicLocation):
        pass

    class Table(p2n.MagicLocation):

        recycle = True

        def bridge(self, agent):
            return agent.gender

        def nest(self):
            return Restaurant

    creator.create_locations(location_classes=[Table, Restaurant])

    assert len(model.agents) == 5
    assert len(model.locations) == 4
    assert sum(location.type == "Table" for location in model.locations) == 3
    assert sum(location.type == "Restaurant" for location in model.locations) == 1

    for location in model.locations:
        if location.type == "Restaurant":
            assert len(location.agents) == 5
            assert [agent.gender for agent in location.agents].count("m") == 2
            assert [agent.gender for agent in location.agents].count("w") == 3
        if location.type == "Classroom":
            assert len(location.agents) == 2
            assert [agent.gender for agent in location.agents].count("m") == 1
            assert [agent.gender for agent in location.agents].count("w") == 1

test_1()
test_2()
