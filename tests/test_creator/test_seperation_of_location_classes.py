import pytest

import pop2net as p2n


@pytest.fixture
def base_attrs():
    return [
        "add_agent",
        "add_agents",
        "agents",
        "get_weight",
        "id",
        "log",
        "model",
        "neighbors",
        "p",
        "project_weights",
        "record",
        "remove_agent",
        "remove_agents",
        "set_weight",
        "setup",
        "type",
        "vars",
        "weight",
    ]


@pytest.fixture
def magic_attrs():
    return [
        "split",
        "nest",
        "bridge",
        "filter",
        "location_class",
        "melt",
        "n_agents",
        "n_locations",
        "nxgraph",
        "only_exact_n_agents",
        "overcrowding",
        "recycle",
        "refine",
        "static_weight",
        "stick_together",
        "_subsplit",
    ]


def test_1(base_attrs, magic_attrs):
    """Testcase: location_class == None & label == None."""

    class MyLocation(p2n.LocationDesigner):
        def custom_method1(self):
            pass

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MyLocation])
    location = model.locations[0]

    # check number of locations
    assert len(model.locations) == 1

    # test if the types are correct
    assert location.type == "Location"
    assert location.label == "MyLocation"
    assert isinstance(location, p2n.Location)
    assert not isinstance(location, MyLocation)

    # test if magic attributes are deleted
    for attr in magic_attrs:
        assert not hasattr(location, attr)

    # test if base attributes are still there
    for attr in base_attrs:
        assert hasattr(location, attr)

    # test if custom methods are still there
    assert hasattr(location, "custom_method1")


def test_2(base_attrs, magic_attrs):
    """Testcase: location_class == None & label != None."""

    class MyLocation(p2n.LocationDesigner):
        label = "MyLocationYo"

        def custom_method1(self):
            pass

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MyLocation])
    location = model.locations[0]

    # check number of locations
    assert len(model.locations) == 1

    # test if the types are correct
    assert location.type == "Location"
    assert location.label == "MyLocationYo"
    assert isinstance(location, p2n.Location)
    assert not isinstance(location, MyLocation)

    # test if magic attributes are deleted
    for attr in magic_attrs:
        assert not hasattr(location, attr)

    # test if base attributes are still there
    for attr in base_attrs:
        assert hasattr(location, attr)

    # test if custom methods are still there
    assert hasattr(location, "custom_method1")


def test_3(base_attrs, magic_attrs):
    """Testcase: location_class != None & label == None."""

    class MyLocation(p2n.Location):
        def custom_method2(self):
            pass

        def weight(self, agent):
            return "MyLocation"

    class MyLocationDesigner(p2n.LocationDesigner):
        location_class = MyLocation

        def custom_method1(self):
            pass

        def weight(self, agent):
            return "MyLocationDesigner"

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MyLocationDesigner])
    location = model.locations[0]

    # check number of locations
    assert len(model.locations) == 1

    # test if the types are correct
    assert location.type == "MyLocation"
    assert location.label == "MyLocationDesigner"
    assert isinstance(location, p2n.Location)
    assert isinstance(location, MyLocation)
    assert not isinstance(location, p2n.LocationDesigner)

    # test if magic attributes are deleted
    for attr in magic_attrs:
        assert not hasattr(location, attr)

    # test if base attributes are still there
    for attr in base_attrs:
        assert hasattr(location, attr)

    # test if custom methods defined in MyLocationDesigner are still there
    assert hasattr(location, "custom_method1")

    # test if custom methods defined in MyLocation are still there
    assert hasattr(location, "custom_method2")

    # test if the baselocation weight method is overwritten by the magiclocation weight method
    assert location.weight(None) == "MyLocationDesigner"


def test_4(base_attrs, magic_attrs):
    """Testcase: location_class != None & label != None."""

    class MyLocation(p2n.Location):
        def custom_method2(self):
            pass

        def weight(self, agent):
            return "MyLocation"

    class MyLocationDesigner(p2n.LocationDesigner):
        location_class = MyLocation
        label = "BlaBla"

        def custom_method1(self):
            pass

        def weight(self, agent):
            return "MyLocationDesigner"

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MyLocationDesigner])
    location = model.locations[0]

    # check number of locations
    assert len(model.locations) == 1

    # test if the types are correct
    assert location.type == "MyLocation"
    assert location.label == "BlaBla"
    assert isinstance(location, p2n.Location)
    assert isinstance(location, MyLocation)
    assert not isinstance(location, p2n.LocationDesigner)

    # test if magic attributes are deleted
    for attr in magic_attrs:
        assert not hasattr(location, attr)

    # test if base attributes are still there
    for attr in base_attrs:
        assert hasattr(location, attr)

    # test if custom methods defined in MyLocationDesigner are still there
    assert hasattr(location, "custom_method1")

    # test if custom methods defined in MyLocation are still there
    assert hasattr(location, "custom_method2")

    # test if the baselocation weight method is overwritten by the magiclocation weight method
    assert location.weight(None) == "MyLocationDesigner"
