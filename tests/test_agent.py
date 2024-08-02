import pandas as pd
import popy
import pytest


@pytest.fixture()
def model():
    return popy.Model()


@pytest.fixture()
def two_locations(model):
    return popy.LocationList(
        model,
        [
            popy.Location(model),
            popy.Location(model),
        ],
    )


def test_agent_creation(model):
    agent = popy.Agent(model)
    assert agent.model == model
    assert list(agent.locations) == []


def test_agentlist_broadcasting(model):
    agents = popy.AgentList(model, [popy.Agent(model), popy.Agent(model)])
    agents.x = 1
    assert sum(agents.x) == 2  # type: ignore


def test_agent_locations(model):
    agent = popy.Agent(model)

    location1 = popy.Location(model)
    location2 = popy.Location(model)

    agent.add_location(location1)

    exp = popy.LocationList(model, [location1])
    assert agent.locations == exp

    agent.add_location(location2)
    exp = popy.LocationList(model, [location1, location2])
    assert agent.locations == exp

    assert len(agent.locations) == 2


def test_agent_located_at_single_location(model):
    class Model(popy.Model):
        def setup(self):
            popy.AgentList(self, 1, popy.Agent)
            popy.LocationList(self, 2, popy.Location)
            self.agents[0].add_location(self.locations[0])

    model = Model(parameters={"steps": 1})
    model.run()

    assert [len(loc.agents) for loc in model.locations] == [1, 0]


def test_agent_visits_two_locations(model):
    class Model(popy.Model):
        def setup(self):
            popy.AgentList(self, 1, popy.Agent)
            popy.LocationList(self, 2, popy.Location)
            self.agents[0].add_location(self.locations[0])
            self.agents[0].add_location(self.locations[1])

    model = Model(parameters={"steps": 1})
    model.run()

    assert [len(loc.agents) for loc in model.locations] == [1, 1]


def test_adding_and_removing_agents():
    model = popy.Model()

    for _ in range(5):
        popy.Agent(model)

    for _ in range(2):
        popy.Location(model)

    model.locations[0].add_agents(model.agents[0:3])
    model.locations[1].add_agents(model.agents[3:5])

    assert len(model.agents) == 5
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert len(model.agents[0].neighbors()) == 2
    assert len(model.agents[-1].neighbors()) == 1

    # inspector = popy.inspector.NetworkInspector(model)
    # inspector.plot_bipartite_network()


def test_color_agents():
    class ColorLocation(popy.Location):
        def __init__(self, model, color) -> None:
            super().__init__(model)
            self.color = color

    class ColorAgent(popy.Agent):
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

    class ColorModel(popy.Model):
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
    class Town(popy.MagicLocation):
        n_agents = 4

        def stick_together(self, agent):
            return agent.couple

        def assert_(self):
            assert len(self.agents) == 4

    class Home(popy.MagicLocation):
        def split(self, agent):
            return agent.couple

        def weight(self, agent):
            return 12

        def assert_(self):
            assert len({a.couple for a in self.agents}) == 1

    class Restaurant(popy.MagicLocation):
        def setup(self):
            chef = Chef(self.model)
            self.add_agent(chef)
            self.set_weight(agent=chef, weight=8)

        def weight(self, agent):
            return 2

        def split(self, agent):
            return agent.food

        def nest(self):
            return Town

        def assert_(self):
            # assert that affiliated agents are affiliated with the same Town
            assert (
                len(
                    {
                        agent.locations.select(agent.locations.type == "Town")[0]
                        for agent in self.agents
                        if isinstance(agent, MyAgent)  # Chef-agents are not affiliated with Towns
                    },
                )
                == 1
            )

    class Chef(popy.Agent):
        def assert_(self):
            assert len(self.locations) == 1
            assert self.locations[0].type == "Restaurant"
            assert self.get_location_weight(self.locations[0]) == 8
            assert (
                len([1 for a in self.locations[0].neighbors(self) if self.get_agent_weight(a) != 2])
                == 0
            )

    class MyAgent(popy.Agent):
        def assert_(self):
            couple_agent = [
                agent
                for agent in self.model.agents.select(self.model.agents.type == "MyAgent")
                if agent.couple == self.couple and agent is not self
            ][0]

            assert self.neighbors(location_classes=[Home])[0] is couple_agent

            assert self.get_agent_weight(couple_agent) == 12 + 1

            assert (
                self.locations.select(self.locations.type == "Town")[0]
                is self.shared_locations(couple_agent, location_classes=[Town])[0]
            )

    df = pd.DataFrame(
        {
            "food": ["pizza", "pasta", "pizza", "pasta", "pizza", "pasta", "pizza", "pasta"],
            "couple": [1, 1, 2, 2, 3, 3, 4, 4],
            "age": [40, 40, 60, 60, 40, 40, 60, 60],
        },
    )

    model = popy.Model()
    creator = popy.Creator(model)
    # inspector = NetworkInspector(model)

    creator.create_agents(df=df, agent_class=MyAgent)

    creator.create_locations(
        location_classes=[
            Town,
            Home,
            Restaurant,
        ],
    )

    # inspector.plot_bipartite_network()
    # inspector.plot_agent_network()

    model.agents.assert_()
    model.locations.assert_()


@pytest.mark.skip()
def test_table_agents():
    # TODO: copied from new_structure.ipynb but has no assert statements.
    # not sure what is being checked here.

    model = popy.Model()
    creator = popy.Creator(model)

    df = pd.DataFrame(
        {
            "food": ["pizza", "pasta", "pizza", "pasta", "pizza", "pasta", "pizza", "pasta"],
            "couple": [1, 1, 2, 2, 3, 3, 4, 4],
            "age": [40, 40, 60, 60, 40, 40, 60, 60],
        },
    )

    df = creator.draw_sample(df=df, n=20)

    creator.create_agents(df=df)

    class Table(popy.MagicLocation):
        recycle = True

        def melt(self):
            class PizzaGroup(popy.MagicLocation):
                n_agents = 3
                only_exact_n_agents = False

                def filter(self, agent):
                    return agent.food == "pizza"

                # def split(self, agent):
                #    return agent.age

                def weight(self, agent):
                    return 10

            class PastaGroup(popy.MagicLocation):
                n_agents = 2
                only_exact_n_agents = False

                def filter(self, agent):
                    return agent.food == "pasta"

            return PizzaGroup, PastaGroup

        def nest(self):
            return Restaurant

        def weight(self, agent):
            return 5

    class Restaurant(popy.MagicLocation):
        n_agents = 10

        # def stick_together(self, agent):
        #    return agent.Table

        # def filter(self, agent):
        #    return agent.Table

    creator.create_locations(
        location_classes=[
            Restaurant,
            Table,
        ],
    )

    raise AssertionError()

    # inspector = popy.inspector.NetworkInspector(model)
    # inspector.plot_agent_network(node_attrs=["food", "age", "couple"], node_color="food")
    # inspector.plot_bipartite_network()
