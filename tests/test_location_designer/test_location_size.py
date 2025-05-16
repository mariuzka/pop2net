import pandas as pd
import pytest

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        pass

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 10


def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 5
        n_locations = None
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        n_locations = None
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_4():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        n_locations = None
        overcrowding = True
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_5_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        n_locations = None
        overcrowding = False
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 4
    assert len(env.locations[2].actors) == 2


def test_5_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        n_locations = None
        overcrowding = False
        only_exact_n_actors = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 4


def test_6():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        n_locations = None
        overcrowding = None
        only_exact_n_actors = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 4


def test_7():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 2
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_8_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_8_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_8_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_9():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 1
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 1


def test_10():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2
        n_locations = 4
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2


def test_11():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 5
        n_locations = 2
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_12():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 7
        n_locations = 1
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 7


def test_13():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 7
        n_locations = 2
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 7
    assert len(env.locations[1].actors) == 3


def test_14():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 7
        n_locations = 2
        overcrowding = None
        only_exact_n_actors = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 7


def test_15():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 7
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 7
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 0


def test_16():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 20
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 10
    assert len(env.locations[1].actors) == 0
    assert len(env.locations[2].actors) == 0


def test_17():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_18():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_19():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 3
        overcrowding = None
        only_exact_n_actors = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 3
    assert len(env.locations[2].actors) == 3


def test_20():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 6
        overcrowding = None
        only_exact_n_actors = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 6
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 1
    assert len(env.locations[3].actors) == 1
    assert len(env.locations[4].actors) == 1


def test_21():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    inspector = p2n.NetworkInspector(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = 6
        overcrowding = None
        only_exact_n_actors = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(env.locations) == 6
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2
    assert len(env.locations[4].actors) == 1
    assert len(env.locations[5].actors) == 1


def test_split_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    inspector = p2n.NetworkInspector(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = None
        n_locations = None
        overcrowding = None
        only_exact_n_actors = False

        def split(self, actor):
            return actor.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(env.locations) == 3
    for location in env.locations:
        if location.actors[0].age == 10 or location.actors[0].age == 20:
            assert len(location.actors) == 4
        else:
            assert len(location.actors) == 2


def test_split_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    inspector = p2n.NetworkInspector(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2
        n_locations = None
        overcrowding = None
        only_exact_n_actors = False

        def split(self, actor):
            return actor.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    inspector.plot_bipartite_network()

    assert len(env.locations) == 5
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2
    assert len(env.locations[4].actors) == 2


# TODO: Maybe bring back the compatibility of n_locations and split in the future
@pytest.mark.skip(reason="n_locations and split are not compatible any more")
def test_split_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2
        n_locations = 1
        overcrowding = None
        only_exact_n_actors = False

        def split(self, actor):
            return actor.age

    df = pd.DataFrame(
        {
            "age": [10, 10, 10, 10, 20, 20, 20, 20, 30, 30],
        },
    )

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2


def test_overcrowding_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        overcrowding = True

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_overcrowding_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        overcrowding = False

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 4
    assert len(env.locations[1].actors) == 4
    assert len(env.locations[2].actors) == 2


def test_overcrowding_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4
        overcrowding = None

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 5


def test_melt_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_actors = 1

                def filter(self, actor):
                    return actor.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_actors = 1

                def filter(self, actor):
                    return actor.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 0

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 5
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2
    assert len(env.locations[4].actors) == 2


def test_melt_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_actors = 1
                n_locations = 3

                def filter(self, actor):
                    return actor.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_actors = 1
                n_locations = 3

                def filter(self, actor):
                    return actor.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 0

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2


def test_melt_3():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 4

        def melt(self):
            class TestMeltLocation0(p2n.MeltLocationDesigner):
                n_actors = 1

                def filter(self, actor):
                    return actor.opinion == 0

            class TestMeltLocation1(p2n.MeltLocationDesigner):
                n_actors = 1

                def filter(self, actor):
                    return actor.opinion == 1

            return TestMeltLocation0, TestMeltLocation1

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 0

    for _ in range(5):
        actor = p2n.Actor(env)
        actor.opinion = 1

    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2
