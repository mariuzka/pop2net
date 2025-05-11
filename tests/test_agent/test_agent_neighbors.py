#%%
import pop2net as p2n


def test_1():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()

    env.add_actors([actor1, actor2])
    env.add_location(location1)

    location1.add_actors([actor1, actor2])

    assert len(env.actors) == 2
    assert len(env.locations) == 1

    assert len(actor1.neighbors()) == 1
    assert actor1.neighbors()[0] is actor2

    assert len(actor2.neighbors()) == 1
    assert actor2.neighbors()[0] is actor1


def test_2a():
    class Max(p2n.Actor):
        pass

    class Marius(p2n.Actor):
        pass

    class Lukas(p2n.Actor):
        pass

    class WebexMeeting(p2n.LocationDesigner):
        pass

    env = p2n.Environment()
    actor_max = Max()
    actor_marius = Marius()
    actor_lukas = Lukas()
    meeting = WebexMeeting()
    env.add_actors(actors=[actor_max, actor_marius, actor_lukas])
    env.add_location(meeting)
    meeting.add_actors(actors=[actor_max, actor_marius, actor_lukas])

    assert len(env.locations) == 1
    assert len(env.actors) == 3

    assert actor_max.neighbors()[0].type == "Marius"
    assert actor_max.neighbors()[1].type == "Lukas"

    assert actor_marius.neighbors()[0].type == "Max"
    assert actor_marius.neighbors()[1].type == "Lukas"

    assert actor_lukas.neighbors()[0].type == "Max"
    assert actor_lukas.neighbors()[1].type == "Marius"


# all in one location
def test_2b():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Max(p2n.Actor):
        pass

    class Marius(p2n.Actor):
        pass

    class Lukas(p2n.Actor):
        pass

    class WebexMeeting(p2n.LocationDesigner):
        pass

    _max = creator.create_actors(actor_class=Max, n=1)[0]
    _marius = creator.create_actors(actor_class=Marius, n=1)[0]
    _lukas = creator.create_actors(actor_class=Lukas, n=1)[0]
    creator.create_locations(location_designers=[WebexMeeting])

    assert len(env.locations) == 1
    assert len(env.actors) == 3

    assert _max.neighbors()[0].type == "Marius"
    assert _max.neighbors()[1].type == "Lukas"

    assert _marius.neighbors()[0].type == "Max"
    assert _marius.neighbors()[1].type == "Lukas"

    assert _lukas.neighbors()[0].type == "Max"
    assert _lukas.neighbors()[1].type == "Marius"


def test_3a():
    class Max(p2n.Actor):
        pass

    class Marius(p2n.Actor):
        pass

    class Lukas(p2n.Actor):
        pass

    class Meeting1(p2n.Location):
        pass

    class Meeting2(p2n.Location):
        pass

    env = p2n.Environment()
    actor_max = Max()
    actor_marius = Marius()
    actor_lukas = Lukas()
    meeting1 = Meeting1()
    meeting2 = Meeting2()
    env.add_actors([actor_max, actor_marius, actor_lukas])
    env.add_locations([meeting1, meeting2])
    meeting1.add_actors([actor_max, actor_marius])
    meeting2.add_actors([actor_marius, actor_lukas])

    assert len(env.locations) == 2
    assert len(env.actors) == 3

    assert actor_max.neighbors(location_labels=["Meeting1"])[0].type == "Marius"

    assert actor_marius.neighbors(location_labels=["Meeting1"])[0].type == "Max"
    assert actor_marius.neighbors(location_labels=["Meeting2"])[0].type == "Lukas"

    assert actor_lukas.neighbors(location_labels=["Meeting2"])[0].type == "Marius"


# two Locations
def test_3b():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Max(p2n.Actor):
        pass

    class Marius(p2n.Actor):
        pass

    class Lukas(p2n.Actor):
        pass

    class Meeting1(p2n.LocationDesigner):
        location_name = "Meeting1"

        def filter(self, actor):
            return actor.type in ["Max", "Marius"]

    class Meeting2(p2n.LocationDesigner):
        location_name = "Meeting2"

        def filter(self, actor):
            return actor.type in ["Marius", "Lukas"]

    _max = creator.create_actors(actor_class=Max, n=1)[0]
    _marius = creator.create_actors(actor_class=Marius, n=1)[0]
    _lukas = creator.create_actors(actor_class=Lukas, n=1)[0]
    creator.create_locations(location_designers=[Meeting1, Meeting2])

    assert len(env.locations) == 2
    assert len(env.actors) == 3

    assert _max.neighbors(location_labels=["Meeting1"])[0].type == "Marius"

    assert _marius.neighbors(location_labels=["Meeting1"])[0].type == "Max"
    assert _marius.neighbors(location_labels=["Meeting2"])[0].type == "Lukas"

    assert _lukas.neighbors(location_labels=["Meeting2"])[0].type == "Marius"