import pandas as pd
import pytest

import pop2net as p2n


def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        pass

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 10


def test_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 5
        n_locations = None
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        n_locations = None
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_4():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        n_locations = None
        overcrowding = True
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_5_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        n_locations = None
        overcrowding = False
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 2


def test_5_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        n_locations = None
        overcrowding = False
        only_exact_n_agents = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_6():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        n_locations = None
        overcrowding = None
        only_exact_n_agents = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_7():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 2
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_8_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_9():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 1
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1


def test_10():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 2
        n_locations = 4
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2


def test_11():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 5
        n_locations = 2
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_12():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 7
        n_locations = 1
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7


def test_13():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 7
        n_locations = 2
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3


def test_14():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 7
        n_locations = 2
        overcrowding = None
        only_exact_n_agents = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7


def test_15():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 7
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 0


def test_16():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 20
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 10
    assert len(model.locations[1].agents) == 0
    assert len(model.locations[2].agents) == 0


def test_17():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_18():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_19():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 3
        overcrowding = None
        only_exact_n_agents = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_20():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 6
        overcrowding = None
        only_exact_n_agents = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 6
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1
    assert len(model.locations[4].agents) == 1


def test_21():
    model = p2n.Model()
    creator = p2n.Creator(model)
    inspector = p2n.NetworkInspector(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = 6
        overcrowding = None
        only_exact_n_agents = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(model.locations) == 6
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 1
    assert len(model.locations[5].agents) == 1


def test_split_1():
    model = p2n.Model()
    creator = p2n.Creator(model)
    inspector = p2n.NetworkInspector(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = None
        n_locations = None
        overcrowding = None
        only_exact_n_agents = False

        def split(self, agent):
            return agent.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    for location in model.locations:
        if location.agents[0].age == 10 or location.agents[0].age == 20:
            assert len(location.agents) == 4
        else:
            assert len(location.agents) == 2


def test_split_2():
    model = p2n.Model()
    creator = p2n.Creator(model)
    inspector = p2n.NetworkInspector(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 2
        n_locations = None
        overcrowding = None
        only_exact_n_agents = False

        def split(self, agent):
            return agent.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(model.locations) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 2


# TODO: Maybe bring back the compatibility of n_locations and split in the future
@pytest.mark.skip(reason="n_locations and split are not compatible any more")
def test_split_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 2
        n_locations = 1
        overcrowding = None
        only_exact_n_agents = False

        def split(self, agent):
            return agent.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2


def test_overcrowding_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        overcrowding = True

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_overcrowding_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        overcrowding = False

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 2


def test_overcrowding_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 4
        overcrowding = None

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_melt_1():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_agents = 1

                def filter(self, agent):
                    return agent.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_agents = 1

                def filter(self, agent):
                    return agent.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 0

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 2


def test_melt_2():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_agents = 1
                n_locations = 3

                def filter(self, agent):
                    return agent.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_agents = 1
                n_locations = 3

                def filter(self, agent):
                    return agent.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 0

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2


def test_melt_3():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 4

        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_agents = 1

                def filter(self, agent):
                    return agent.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_agents = 1

                def filter(self, agent):
                    return agent.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 0

    for _ in range(5):
        agent = p2n.Agent(model)
        agent.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
