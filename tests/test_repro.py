# %%
import agentpy as ap
import networkx as nx
import pytest

import pop2net as p2n


def test_network_repro():
    """Tests if the exact same network is generated."""

    model = ap.Model(parameters={"seed": 1, "steps": 1})

    # run the model 1 step to set the seed
    model.run()

    env = p2n.Environment(model=model, framework="agentpy")
    creator = p2n.Creator(env=env, seed=1)

    class Cluster(p2n.LocationDesigner):
        n_actors = 5

    class Ring(p2n.LocationDesigner):
        nxgraph = nx.cycle_graph(n=20)

        def filter(self, actor):
            return actor.Cluster_head

    creator.create_actors(n=100)
    creator.create_locations(location_designers=[Cluster, Ring])

    for i in range(100):
        random_actor_1 = model.random.choice(env.actors)
        random_actor_2 = model.random.choice(env.actors)

        if random_actor_1 is not random_actor_2:
            random_actor_1.connect(random_actor_2)

    average_clustering = nx.average_clustering(env.export_actor_network())

    assert average_clustering == pytest.approx(0.4594978355)
