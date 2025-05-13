import pandas as pd
import pytest

import pop2net as p2n
from pop2net.actor import Actor
from pop2net.location import Location


# TODO wie das übersetzen? 
#class Model(p2n.Model):
   # pass


class MyAgent(Actor):
    pass


class Home(Location):
    def setup(self):
        self.is_home = True

    def group(self, actor):
        return actor.hid


class School(Location):
    n_actors = 10

    def group(self, actor):
        return 0 if actor.age <= 14 else 1

    def join(self, actor):
        return 6 <= actor.age <= 18

    def can_visit(self, actor):
        pass


simple_fake_data = pd.DataFrame(
    {
        "pid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "hid": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
        "age": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
    },
)


@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_create_actors(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    actors = creator.create_actors(df=soep, actor_class=MyAgent)

    assert len(actors) == len(soep)

    for i, row in soep.iterrows():
        for col_name in soep.columns:
            assert row[col_name] == getattr(actors[i], col_name)


@pytest.mark.skip
# @pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000"])
def test_create_locations():
    soep = simple_fake_data.copy()
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    actors = creator.create_actors(df=soep, actor_class=MyAgent)
    for actor in actors:
        env.add_actor(actor)

    locations = creator.create_locations(agents=actors, location_designers=[Home, School])
    for location in locations:
        env.add_location(location)

    assert len([location for location in locations if isinstance(location, Home)]) == 4
    assert len([location for location in locations if isinstance(location, School)]) == 2

    for location in locations:
        for actor in location.actors:
            assert location.group(actor) == location.group_id

test_create_actors()
test_create_locations()