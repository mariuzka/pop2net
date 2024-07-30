import popy
from popy.creator import Creator
import math
import pandas as pd

def test_1():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        pass

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 10


def test_2():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 5
        n_locations = None
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_3():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        n_locations = None
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_4():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        n_locations = None
        overcrowding = True
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_5_1():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        n_locations = None
        overcrowding = False
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 2


def test_5_2():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        n_locations = None
        overcrowding = False
        exact_size_only = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_6():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        n_locations = None
        overcrowding = None
        exact_size_only = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_7():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 2
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_8_1():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_2():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_3():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_9():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 1
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1


def test_10():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 2
        n_locations = 4
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2


def test_11():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 5
        n_locations = 2
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_12():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 7
        n_locations = 1
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7


def test_13():
    model = popy.Model()
    creator = Creator(model)
    
    class TestLocation(popy.MagicLocation):
        n_agents = 7
        n_locations = 2
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3


def test_14():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 7
        n_locations = 2
        overcrowding = None
        exact_size_only = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

def test_15():
    model = popy.Model()
    creator = Creator(model)
   
    class TestLocation(popy.MagicLocation):
        n_agents = 7
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3


def test_16():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 20
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 10


def test_17():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_18():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_19():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 3
        overcrowding = None
        exact_size_only = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_20():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 6
        overcrowding = None
        exact_size_only = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 6
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1
    assert len(model.locations[4].agents) == 1


def test_21():
    model = popy.Model()
    creator = Creator(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = 6
        overcrowding = None
        exact_size_only = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 6
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 1
    assert len(model.locations[5].agents) == 1


def test_split_1():
    model = popy.Model()
    creator = Creator(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        n_agents = None
        n_locations = None
        overcrowding = None
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    for location in model.locations:
        if location.agents[0].age == 10 or location.agents[0].age == 20:
            assert len(location.agents) == 4
        else:
            assert len(location.agents) == 2

def test_split_2():
    model = popy.Model()
    creator = Creator(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        n_agents = 2
        n_locations = None
        overcrowding = None
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 2


def test_split_3():
    model = popy.Model()
    creator = Creator(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        n_agents = 2
        n_locations = 1
        overcrowding = None
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2


def test_overcrowding_1():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        overcrowding = True

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_overcrowding_2():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        overcrowding = False

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 2


def test_overcrowding_3():
    model = popy.Model()
    creator = Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 4
        overcrowding = None

    creator.create_agents(n=10)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5