import pop2net as p2n


def test_location_label():

    # Test 1: Default label (label is class name)
    location = p2n.Location()
    assert location.label == "Location"

    # Test 2: Label is custom class name
    class MyLocation(p2n.Location):
        pass

    location = MyLocation()
    assert location.label == "MyLocation"

    # Test 3: Label is custom string
    class MyLocation(p2n.Location):
        label = "MyLocationYo"

    location = MyLocation()
    assert location.label == "MyLocationYo"


def test_location_designer_label():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    # Test 1: Default label (label is designer class name)
    class School(p2n.LocationDesigner):
        n_locations = 1

    location = creator.create_locations(location_designers=[School])[0]
    assert location.label == "School"

    # Test 2: Label is custom string
    class School(p2n.LocationDesigner):
        label = "SchoolYo"
        n_locations = 1

    location = creator.create_locations(location_designers=[School])[0]
    assert location.label == "SchoolYo"

    # Test 3: Label is the designer class name even if a custom location class is used
    class School(p2n.Location):
        pass

    class SchoolDesigner(p2n.LocationDesigner):
        n_locations = 1
        location_class = School

    location = creator.create_locations(location_designers=[SchoolDesigner])[0]
    assert location.label == "SchoolDesigner"

    # Test 4: Label is the label defined in the designer class even if a location class is used
    class School(p2n.Location):
        label = "Schoooooool"

    class SchoolDesigner(p2n.LocationDesigner):
        label = "SchoolYOOO"
        n_locations = 1
        location_class = School

    location = creator.create_locations(location_designers=[SchoolDesigner])[0]
    assert location.label == "SchoolYOOO"
