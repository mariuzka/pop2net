import pandas as pd

import pop2net as p2n


def test_simple():
    df_actors = pd.DataFrame({"name": ["John", "Paul", "Gustav"]})
    df_edges = pd.DataFrame(
        [
            {"source": "John", "target": "Paul", "weight": 1},
            {"source": "John", "target": "Gustav", "weight": 3},
        ]
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    creator.create_actors(df=df_actors)
    creator.create_locations_from_pandas_edgelist(
        df=df_edges,
        id_attr_name="name",
        location_label="TestLocation",
    )

    assert len(env.actors) == 3
    assert len(env.locations) == 2

    assert env.locations[0].label == "TestLocation"

    assert (
        env._get_actor_by_attr_value("name", "John")
        in env._get_actor_by_attr_value("name", "Paul").neighbors()
    )

    assert (
        env._get_actor_by_attr_value("name", "Gustav")
        in env._get_actor_by_attr_value("name", "John").neighbors()
    )

    assert (
        env._get_actor_by_attr_value("name", "Gustav")
        not in env._get_actor_by_attr_value("name", "Paul").neighbors()
    )


def test_with_framework():
    df_actors = pd.DataFrame({"name": ["John", "Paul", "Gustav"]})
    df_edges = pd.DataFrame(
        [
            {"source": "John", "target": "Paul", "weight": 1},
            {"source": "John", "target": "Gustav", "weight": 3},
        ]
    )

    import mesa

    model = mesa.Model()
    env = p2n.Environment(model=model, framework="mesa")
    creator = p2n.Creator(env=env)

    creator.create_actors(df=df_actors)
    creator.create_locations_from_pandas_edgelist(
        df=df_edges,
        id_attr_name="name",
        location_label="TestLocation",
    )

    assert len(env.actors) == 3
    assert len(env.locations) == 2

    assert env.locations[0].label == "TestLocation"

    assert (
        env._get_actor_by_attr_value("name", "John")
        in env._get_actor_by_attr_value("name", "Paul").neighbors()
    )

    assert (
        env._get_actor_by_attr_value("name", "Gustav")
        in env._get_actor_by_attr_value("name", "John").neighbors()
    )

    assert (
        env._get_actor_by_attr_value("name", "Gustav")
        not in env._get_actor_by_attr_value("name", "Paul").neighbors()
    )
