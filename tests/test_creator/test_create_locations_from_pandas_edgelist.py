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

    actors_by_name = env._get_actors_by_attribute(attr_name="name")

    assert (
        actors_by_name["John"]
        in actors_by_name["Paul"].neighbors()
    )

    assert (
        actors_by_name["Gustav"]
        in actors_by_name["John"].neighbors()
    )

    assert (
        actors_by_name["Gustav"]
        not in actors_by_name["Paul"].neighbors()
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

    actors_by_name = env._get_actors_by_attribute(attr_name="name")

    assert (
            actors_by_name["John"]
            in actors_by_name["Paul"].neighbors()
        )
    
    assert (
        actors_by_name["Gustav"]
        in actors_by_name["John"].neighbors()
    )

    assert (
        actors_by_name["Gustav"]
        not in actors_by_name["Paul"].neighbors()
    )
