import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil"]})
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Classroom(p2n.LocationDesigner):
        n_actors = 3
        only_exact_n_actors = False

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        pass

    creator.create(df=df, location_designers=[Classroom, School])

    assert len(env.actors) == 5
    assert len(env.locations) == 3
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 5

    # Version with set to true
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Classroom(p2n.LocationDesigner):
        n_actors = 3
        only_exact_n_actors = True

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        pass

    creator.create(df=df, location_designers=[Classroom, School])
    inspector = p2n.NetworkInspector(env=env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=["status"])

    assert len(env.actors) == 5
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 3
    assert len(env.locations[1].actors) == 5


def test_2():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil"]})
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Classroom(p2n.LocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        n_actors = 4
        only_exact_n_actors = True

    creator.create(df=df, location_designers=[Classroom, School])
    inspector = p2n.NetworkInspector(env=env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=["status"])

    assert len(env.actors) == 6
    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 4
    assert env.locations[2].actors not in env.locations[3].actors
