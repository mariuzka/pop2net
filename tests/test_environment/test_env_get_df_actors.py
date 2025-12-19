import pytest

import pop2net as p2n
import mesa
import pandas as pd


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])
    df_actors = env.get_df_actors()
    df_actors = df_actors.drop(columns=["env"])
    df_assert = pd.DataFrame({"id_p2n":[0, 1, 2, 3],
                              "model":[None, None, None, None],
                              "type": ["Actor", "Actor", "Actor", "Actor"],
                              "status": ["pupil", "pupil", "pupil", "pupil"],
                              "class_id": [1, 2, 1, 2]})
    
    pd.testing.assert_frame_equal(df_actors.reset_index(drop=True), df_assert.reset_index(drop=True))


def test_2():
    #df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})
    class Actor(p2n.Actor, mesa.Agent):
        def __init__(self, class_id, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.status = "pupil"
            self.class_id = class_id

        def say_hello(self):
            print("Hello I am an actor.")

    class Location(p2n.Location, mesa.Agent):
        def say_hello(self):
            print("Hello I am a location.")

    class Model(mesa.Model):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # add pop2net environment object as model attribute
            self.env = p2n.Environment(model=self, framework="mesa")

            # add one actor to the environment
            self.env.add_actor(Actor(model=self, class_id=1))
            self.env.add_actor(Actor(model=self, class_id=2))
            self.env.add_actor(Actor(model=self, class_id=1))
            self.env.add_actor(Actor(model=self, class_id=2))


            # add one location to the environment
            self.env.add_location(Location(model=self))

        def step(self):
            # Because env.actors and env.locations are AgentSets now,
            # we can use the Mesa Syntax to let the agents do something:
            self.env.actors.do("say_hello")
            self.env.locations.do("say_hello")

    model = Model()
    df_actors = model.env.get_df_actors()
    df_assert = pd.DataFrame({"id_p2n":[0, 1, 2, 3],
                              "type": ["Actor", "Actor", "Actor", "Actor"],
                              "unique_id":[1, 2, 3, 4],
                              "status": ["pupil", "pupil", "pupil", "pupil"],
                              "class_id": [1, 2, 1, 2]})
    
    assert df_actors["model"].all()
    pd.testing.assert_frame_equal(df_actors.drop(columns=["env", "model", "pos"]).reset_index(drop=True), df_assert.reset_index(drop=True))
