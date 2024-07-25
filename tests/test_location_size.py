import popy
from popy.pop_maker import PopMaker
import math
import pandas as pd

def test_1():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        pass

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 10


def test_2():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 5
        n_locations = None
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_3():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 4
        n_locations = None
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4
    assert len(model.locations[2].agents) == 2


def test_4():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 4
        n_locations = None
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5

def test_5():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 4
        n_locations = None
        round_function = math.ceil
        exact_size_only = True

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_6():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 4
        n_locations = None
        round_function = math.floor
        exact_size_only = True

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 4


def test_7():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 2
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_8_1():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_2():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_8_3():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = round
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_9():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 1
        n_locations = 3
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1


def test_10():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 2
        n_locations = 4
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2


def test_11():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 5
        n_locations = 2
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 5


def test_12():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 7
        n_locations = 1
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7


def test_13():
    model = popy.Model()
    popmaker = PopMaker(model)
    
    class TestLocation(popy.MagicLocation):
        size = 7
        n_locations = 2
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3


def test_14():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 7
        n_locations = 2
        round_function = math.ceil
        exact_size_only = True

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

def test_15():
    model = popy.Model()
    popmaker = PopMaker(model)
   
    class TestLocation(popy.MagicLocation):
        size = 7
        n_locations = 3
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 3


def test_16():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = 20
        n_locations = 3
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 10


def test_17():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = math.ceil
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_18():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 4
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_19():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 3
        round_function = math.floor
        exact_size_only = True

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 3
    assert len(model.locations[2].agents) == 3


def test_20():
    model = popy.Model()
    popmaker = PopMaker(model)

    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 6
        round_function = math.floor
        exact_size_only = True

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
    assert len(model.locations) == 6
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1
    assert len(model.locations[4].agents) == 1


def test_21():
    model = popy.Model()
    popmaker = PopMaker(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = 6
        round_function = math.floor
        exact_size_only = False

    popmaker.create_agents(n=10)
    popmaker.create_locations(location_classes=[TestLocation])
    
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
    popmaker = PopMaker(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        size = None
        n_locations = None
        round_function = math.floor
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    popmaker.create_agents(df=df)
    popmaker.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    for location in model.locations:
        if location.agents[0].age == 10 or location.agents[0].age == 20:
            assert len(location.agents) == 4
        else:
            assert len(location.agents) == 2

def test_split_2():
    model = popy.Model()
    popmaker = PopMaker(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        size = 2
        n_locations = None
        round_function = math.floor
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    popmaker.create_agents(df=df)
    popmaker.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert len(model.locations[4].agents) == 2


def test_split_3():
    model = popy.Model()
    popmaker = PopMaker(model)
    inspector = popy.NetworkInspector(model)


    class TestLocation(popy.MagicLocation):
        size = 2
        n_locations = 1
        round_function = math.floor
        exact_size_only = False
    
        def split(self, agent):
            return agent.age

    df = pd.DataFrame({
        "age": [10,10,10,10,20,20,20,20,30,30],
    })

    popmaker.create_agents(df=df)
    popmaker.create_locations(location_classes=[TestLocation])
    
    inspector.plot_bipartite_network()

    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2