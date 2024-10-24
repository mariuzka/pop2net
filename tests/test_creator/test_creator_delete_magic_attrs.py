import pandas as pd

import pop2net as p2n

magic_agent_attributes = ["", "_assigned", "_id", "_position", "_head", "_tail"]
magic_agent_attributes = ["Location1" + attr for attr in magic_agent_attributes] + [
    "Location2" + attr for attr in magic_agent_attributes
]


def test_del_magic_agent_attrs1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Location1(p2n.MagicLocation):
        pass

    class Location2(p2n.MagicLocation):
        pass

    # First test: Do NOT delete magic agent attributes
    creator.create_agents(n=10)
    creator.create_locations(
        location_classes=[Location1, Location2],
        delete_magic_agent_attributes=False,
    )

    for agent in model.agents:
        for attr in magic_agent_attributes:
            assert hasattr(agent, attr)

    # Second test: DELETE magic agent attributes
    creator.create_agents(n=10, clear=True)
    creator.create_locations(
        location_classes=[Location1, Location2],
        delete_magic_agent_attributes=True,
        clear=True,
    )

    for agent in model.agents:
        for attr in magic_agent_attributes:
            assert not hasattr(agent, attr)


def test_del_magic_agent_attrs2():
    df = pd.DataFrame({"testattr": [10, 11, 12, 13]})

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class Location1(p2n.MagicLocation):
        pass

    class Location2(p2n.MagicLocation):
        pass

    # First test: Do NOT delete magic agent attributes
    creator.create(
        df=df,
        n_agents=10,
        location_classes=[Location1, Location2],
        delete_magic_agent_attributes=False,
    )

    for agent in model.agents:
        for attr in magic_agent_attributes:
            assert hasattr(agent, attr)

    # Second test: DELETE magic agent attributes
    creator.create(
        df=df,
        n_agents=10,
        location_classes=[Location1, Location2],
        delete_magic_agent_attributes=True,
        clear=True,
    )

    for agent in model.agents:
        for attr in magic_agent_attributes:
            assert not hasattr(agent, attr)
