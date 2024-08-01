from popy import AgentList
from popy.agent import Agent
from popy.location import Location
from popy.model import Model
import pytest

@pytest.fixture(scope="module")
def two_agent_location():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1, visit_weight=1)
    loc.add_agent(agent2, visit_weight=1)

    return loc


def test_agent_property():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1)
    loc.add_agent(agent2)

    assert AgentList(model, [agent1, agent2]) == loc.agents


def test_create_location():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)
    loc.add_agent(agent1)
    loc.add_agent(agent2)

    neighbours = list(loc.neighbors(agent1))
    assert neighbours


def test_location_size():
    model = Model()
    loc = Location(model=model)
    agent1 = Agent(model=model)
    agent2 = Agent(model=model)

    assert len(loc.agents) == 0
    loc.add_agent(agent1)
    assert len(loc.agents) == 1
    loc.add_agent(agent2)
    assert len(loc.agents) == 2
    loc.remove_agent(agent1)
    assert len(loc.agents) == 1
    loc.remove_agent(agent2)
    assert len(loc.agents) == 0


# def test_melt(
#     size_pizza_group,
#     size_pasta_group,
#     recycle_,
#     only_exact_n_agents_pizza_group,
#     only_exact_n_agents_pasta_group,
# ):
#     class Table(popy.MagicLocation):
#         recycle = recycle_

#         def melt(self):
#             class PizzaGroup(popy.MagicLocation):
#                 n_agents = size_pizza_group
#                 only_exact_n_agents = only_exact_n_agents_pizza_group

#                 def filter(self, agent):
#                     return agent.food == "pizza"

#                 # def split(self, agent):
#                 #    return agent.age

#                 def weight(self, agent):
#                     return 10

#             class PastaGroup(popy.MagicLocation):
#                 n_agents = size_pasta_group
#                 only_exact_n_agents = only_exact_n_agents_pasta_group

#                 def filter(self, agent):
#                     return agent.food == "pasta"

#             return PizzaGroup, PastaGroup

#     df = pd.DataFrame({"food": ["pizza", "pasta"] * 10})
#     model = popy.Model()

#     creator = Creator(model)
#     creator.create_agents(df=df)
#     creator.create_locations(location_classes=[Table])

#     return model
