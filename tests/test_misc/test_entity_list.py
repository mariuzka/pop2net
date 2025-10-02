import pop2net as p2n


def test_print_in_environment():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()

    env.add_actors([actor1, actor2])
    env.add_location(location1)

    location1.add_actors([actor1, actor2])

    assert str(env.locations) == "EntityList [1 location]"
    # assert repr(env.locations) == "EntityList [1 entities]"
    assert str(env.actors) == "EntityList [2 actors]"
    # assert repr(env.actors) == "EntityList [2 entities]"

    # mixed objects 
    combined = p2n.EntityList([*env.locations, *env.actors])
    assert str(combined) == "EntityList [1 location, 2 actors]" or str(combined) == "EntityList [2 actors, 1 location]"
    
    # unknown objects
    combined = p2n.EntityList([*env.locations, *[8]])
    assert str(combined) == "EntityList [1 location, 1 entity]" or str(combined) == "EntityList [1 entity, 1 location]"


def test_print_in_creator():
    class TestLocationDesigner(p2n.LocationDesigner):
        pass

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    assert str(creator.create_actors(n=10)) == "EntityList [10 actors]"
    assert (
        str(creator.create_locations(location_designers=[TestLocationDesigner]))
        == "EntityList [1 location]"
    )
