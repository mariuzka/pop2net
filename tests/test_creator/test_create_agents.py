import pop2net as p2n


def test_simple():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    creator.create_actors(n=77)

    assert len(env.actors) == 77


def test_given_actor_class_without_model_in_constructor():
    class TestActor(p2n.Actor):
        pass

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    creator.create_actors(n=77, actor_class=TestActor)

    assert len(env.actors) == 77


def test_given_actor_class_with_model_in_constructor():
    class TestActor(p2n.Actor):
        def __init__(self, model):
            super().__init__()
            self.model = model

    class Model:
        pass

    model = Model()
    env = p2n.Environment(
        model=model
    )  # TODO: If the given actor class needs a model, the env also needs a model. Is that a good design?
    creator = p2n.Creator(env=env)

    creator.create_actors(n=77, actor_class=TestActor)

    assert len(env.actors) == 77
