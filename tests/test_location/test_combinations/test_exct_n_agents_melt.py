import pandas as pd
import pop2net as p2n

# Testen: Wie verhält es sich wenn n_agents vorgegeben ist aber noch lehrer übrig sind
# wie verhält es sich, wenn in der Ziel location n_agent und exact true ist, aber in den unteren nichts gesetz ist
# was passiert wenn ich false und true in den Meltlocation mixe?


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B", "B", "B"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class LocA(p2n.MeltLocation):
        n_agents = 2
        only_exact_n_agents = False

        def filter(self, agent):
            return agent.status == "A"

    class LocB(p2n.MeltLocation):
        n_agents = 2
        only_exact_n_agents = False

        def filter(self, agent):
            return agent.status == "B"

    class LocAB(p2n.MagicLocation):
        def melt(self):
            return LocA, LocB

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[LocAB])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status"])

    assert len(model.agents) == 6
    assert len(model.locations) == 2
    assert sum(True for agent in model.locations[0].agents if agent.status == "A") == 2
    assert sum(True for agent in model.locations[0].agents if agent.status == "B") == 2
    assert sum(True for agent in model.locations[1].agents if agent.status == "A") == 1
    assert sum(True for agent in model.locations[1].agents if agent.status == "B") == 1

    # Ver. with exact_n set to true
    model = p2n.Model()
    creator = p2n.Creator(model)

    class LocA(p2n.MeltLocation):
        n_agents = 2
        only_exact_n_agents = True

        def filter(self, agent):
            return agent.status == "A"

    class LocB(p2n.MeltLocation):
        n_agents = 2
        only_exact_n_agents = True

        def filter(self, agent):
            return agent.status == "B"

    class LocAB(p2n.MagicLocation):
        n_agents = 4
        only_exact_n_agents = True

        def melt(self):
            return LocA, LocB

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[LocAB])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status"])

    assert len(model.agents) == 6
    assert len(model.locations) == 1
    assert sum(True for agent in model.locations[0].agents if agent.status == "A") == 2
    assert sum(True for agent in model.locations[0].agents if agent.status == "B") == 2
    assert sum(True for agent in model.agents if not agent.locations) == 2
