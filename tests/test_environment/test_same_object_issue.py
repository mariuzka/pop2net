import pop2net as p2n
import pytest

def test_1():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    env.add_actors([actor1, actor2])
    with pytest.raises(ValueError):
        actor1.get_actor_weight(actor1)


def test_2_creator():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(n=2)
    with pytest.raises(ValueError):
        env.actors[0].get_actor_weight(env.actors[0])