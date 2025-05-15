import pop2net as p2n


def test_1():
    class CityDesigner(p2n.LocationDesigner):
        label = "City"
        n_actors = 4

    class GroupDesigner(p2n.LocationDesigner):
        label = "Group"
        n_actors = 2

        def split(self, actor):
            return actor.group

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    for i in range(8):
        actor = p2n.Actor(env=env)
        actor.group = i % 2

    creator.create_locations(
        location_designers=[CityDesigner, GroupDesigner],
        delete_magic_actor_attributes=False,
    )

    for actor in env.actors:
        print(vars(actor))

    for location in env.locations.select(env.locations.label == "City"):
        assert int(location.actors[0].group) == 0
        assert int(location.actors[1].group) == 1
        assert int(location.actors[2].group) == 0
        assert int(location.actors[3].group) == 1

    for location in env.locations.select(env.locations.label == "Group"):
        assert location.actors[0].group == location.actors[1].group

    # not all members of the same group are also in the same city (which is not desired)
    assert not all(
        location.actors[0].City == location.actors[1].City for location in env.locations
    )

    class GroupNestedInCityDesigner(GroupDesigner):
        def nest(self):
            return "City"

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_locations(
        location_designers=[CityDesigner, GroupNestedInCityDesigner],
        delete_magic_actor_attributes=False,
    )

    for location in env.locations.select(env.locations.label == "City"):
        assert int(location.actors[0].group) == 0
        assert int(location.actors[1].group) == 1
        assert int(location.actors[2].group) == 0
        assert int(location.actors[3].group) == 1

    for location in env.locations.select(env.locations.label == "Group"):
        assert location.actors[0].group == location.actors[1].group

    # all members of a group are in the same city
    assert all(location.actors[0].City == location.actors[1].City for location in env.locations)
