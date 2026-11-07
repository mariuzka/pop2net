import pop2net as p2n


def test_unique_ids_in_original_order():
    env = p2n.Environment()
    creator = p2n.Creator(env)

    creator.create_actors_from_id_list(
        id_list=["b", "a", "c", "a", "b"],
        id_attr_name="name",
        actor_class=None,
    )

    # one actor per unique id, in the order of first occurrence
    assert [actor.name for actor in env.actors] == ["b", "a", "c"]
