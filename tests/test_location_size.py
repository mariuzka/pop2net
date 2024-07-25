import popy
from popy.pop_maker import PopMaker
import math

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


def test_8():
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
    assert len(model.locations[1].agents) == 3


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