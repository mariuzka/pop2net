import pandas as pd
import pytest

import pop2net as p2n


@pytest.fixture
def model():
    return p2n.Model()


@pytest.fixture
def two_locations(model):
    return p2n.LocationList(
        model,
        [
            p2n.Location(model),
            p2n.Location(model),
        ],
    )


def test_agent_creation(model):
    agent = p2n.Agent(model)
    assert agent.model == model
    assert list(agent.locations) == []


def test_agentlist_broadcasting(model):
    agents = p2n.AgentList(model, [p2n.Agent(model), p2n.Agent(model)])
    agents.x = 1
    assert sum(agents.x) == 2  # type: ignore


def test_agent_locations(model):
    agent = p2n.Agent(model)

    location1 = p2n.Location(model)
    location2 = p2n.Location(model)

    agent.add_location(location1)

    exp = p2n.LocationList(model, [location1])
    assert agent.locations == exp

    agent.add_location(location2)
    exp = p2n.LocationList(model, [location1, location2])
    assert agent.locations == exp

    assert len(agent.locations) == 2


def test_agent_located_at_single_location(model):
    class Model(p2n.Model):
        def setup(self):
            p2n.AgentList(self, 1, p2n.Agent)
            p2n.LocationList(self, 2, p2n.Location)
            self.agents[0].add_location(self.locations[0])

    model = Model(parameters={"steps": 1})
    model.run()

    assert [len(loc.agents) for loc in model.locations] == [1, 0]


def test_agent_visits_two_locations(model):
    class Model(p2n.Model):
        def setup(self):
            p2n.AgentList(self, 1, p2n.Agent)
            p2n.LocationList(self, 2, p2n.Location)
            self.agents[0].add_location(self.locations[0])
            self.agents[0].add_location(self.locations[1])

    model = Model(parameters={"steps": 1})
    model.run()

    assert [len(loc.agents) for loc in model.locations] == [1, 1]


def test_adding_and_removing_agents():
    model = p2n.Model()

    for _ in range(5):
        p2n.Agent(model)

    for _ in range(2):
        p2n.Location(model)

    model.locations[0].add_agents(model.agents[0:3])
    model.locations[1].add_agents(model.agents[3:5])

    assert len(model.agents) == 5
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert len(model.agents[0].neighbors()) == 2
    assert len(model.agents[-1].neighbors()) == 1

    # inspector = p2n.inspector.NetworkInspector(model)
    # inspector.plot_bipartite_network()


def test_color_agents():
    class ColorLocation(p2n.Location):
        def __init__(self, model, color) -> None:
            super().__init__(model)
            self.color = color

    class ColorAgent(p2n.Agent):
        def __init__(self, model, color) -> None:
            super().__init__(model)
            self.color = color

        def change_location(self):
            for location in self.locations:
                if location.color != self.color:
                    self.remove_location(location)

            for location in self.model.locations:
                if location.color == self.color and location not in self.locations:
                    self.add_location(location)
                    return

            if self.color not in [location.color for location in self.model.locations]:
                location = ColorLocation(model=self.model, color=self.color)
                location.add_agent(self)

    class ColorModel(p2n.Model):
        def setup(self):
            for color in ["red", "green", "red", "blue", "blue", "red"]:
                ColorAgent(
                    model=self,
                    color=color,
                )

            ColorLocation(self, "blue")
            ColorLocation(self, "red")

            self.locations[0].add_agents(self.agents[0:3])
            self.locations[1].add_agents(self.agents[3:6])

            assert len(self.agents) == 6
            assert len(self.locations) == 2
            assert len(self.locations[0].agents) == 3
            assert len(self.locations[1].agents) == 3

        def step(self):
            self.agents.change_location()

        def end(self):
            assert len(self.agents) == 6
            assert len(self.locations) == 3
            assert len(self.locations[0].agents) == 2
            assert len(self.locations[1].agents) == 3
            assert len(self.locations[2].agents) == 1


def test_chef_agents():
    class Town(p2n.LocationDesigner):
        n_agents = 4

        def stick_together(self, agent):
            return agent.couple

        def assert_(self):
            assert len(self.agents) == 4

    class Home(p2n.LocationDesigner):
        def split(self, agent):
            return agent.couple

        def weight(self, agent):
            return 12

        def assert_(self):
            assert len({a.couple for a in self.agents}) == 1

    class Restaurant(p2n.LocationDesigner):
        def setup(self):
            chef = Chef(self.model)
            self.add_agent(chef)
            self.set_weight(agent=chef, weight=8)

        def weight(self, agent):
            return 2

        def split(self, agent):
            return agent.food

        def nest(self):
            return "Town"

        def assert_(self):
            # assert that affiliated agents are affiliated with the same Town
            assert (
                len(
                    {
                        agent.locations.select(agent.locations.label == "Town")[0]
                        for agent in self.agents
                        if agent.type == "MyAgent"  # Chef-agents are not affiliated with Towns
                    },
                )
                == 1
            )

    class Chef(p2n.Agent):
        def assert_(self):
            assert len(self.locations) == 1
            assert self.locations[0].label == "Restaurant"
            assert self.get_location_weight(self.locations[0]) == 8
            assert (
                len([1 for a in self.locations[0].neighbors(self) if self.get_agent_weight(a) != 2])
                == 0
            )

    class MyAgent(p2n.Agent):
        def assert_(self):
            couple_agent = [
                agent
                for agent in self.model.agents.select(self.model.agents.type == "MyAgent")
                if agent.couple == self.couple and agent is not self
            ][0]

            assert self.neighbors(location_labels=["Home"])[0] is couple_agent

            assert self.get_agent_weight(couple_agent) == 12 + 1

            print(self.locations)
            for location in self.locations:
                print(location.label)

            print(self.shared_locations(couple_agent))
            for l in self.shared_locations(couple_agent):
                print(l.label)

            print([location for location in self.locations if location.label == "Town"])
            print(self.shared_locations(couple_agent, location_labels=["Town"]))

            for location in self.locations:
                print(location.label, location.id)

            for location in couple_agent.locations:
                print(location.label, location.id)

            assert [location for location in self.locations if location.label == "Town"][
                0
            ] is self.shared_locations(couple_agent, location_labels=["Town"])[0]

    df = pd.DataFrame(
        {
            "food": ["pizza", "pasta", "pizza", "pasta", "pizza", "pasta", "pizza", "pasta"],
            "couple": [1, 1, 2, 2, 3, 3, 4, 4],
            "age": [40, 40, 60, 60, 40, 40, 60, 60],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)
    # inspector = NetworkInspector(model)

    creator.create_agents(df=df, agent_class=MyAgent)

    creator.create_locations(
        location_designers=[
            Town,
            Home,
            Restaurant,
        ],
    )

    # inspector.plot_bipartite_network()
    # inspector.plot_agent_network()

    model.agents.assert_()
    model.locations.assert_()


@pytest.mark.skip
def test_table_agents():
    # TODO: copied from new_structure.ipynb but has no assert statements.
    # not sure what is being checked here.

    model = p2n.Model()
    creator = p2n.Creator(model)

    df = pd.DataFrame(
        {
            "food": ["pizza", "pasta", "pizza", "pasta", "pizza", "pasta", "pizza", "pasta"],
            "couple": [1, 1, 2, 2, 3, 3, 4, 4],
            "age": [40, 40, 60, 60, 40, 40, 60, 60],
        },
    )

    df = creator.draw_sample(df=df, n=20)

    creator.create_agents(df=df)

    class Table(p2n.LocationDesigner):
        recycle = True

        def melt(self):
            class PizzaGroup(p2n.LocationDesigner):
                n_agents = 3
                only_exact_n_agents = False

                def filter(self, agent):
                    return agent.food == "pizza"

                # def split(self, agent):
                #    return agent.age

                def weight(self, agent):
                    return 10

            class PastaGroup(p2n.LocationDesigner):
                n_agents = 2
                only_exact_n_agents = False

                def filter(self, agent):
                    return agent.food == "pasta"

            return PizzaGroup, PastaGroup

        def nest(self):
            return "Restaurant"

        def weight(self, agent):
            return 5

    class Restaurant(p2n.LocationDesigner):
        n_agents = 10

        # def stick_together(self, agent):
        #    return agent.Table

        # def filter(self, agent):
        #    return agent.Table

    creator.create_locations(
        location_designers=[
            Restaurant,
            Table,
        ],
    )

    raise AssertionError()

    # inspector = p2n.inspector.NetworkInspector(model)
    # inspector.plot_agent_network(node_attrs=["food", "age", "couple"], node_color="food")
    # inspector.plot_bipartite_network()
