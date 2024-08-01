import pandas as pd
import popy
from popy.agent import Agent
from popy.location import Location
import pytest

class Model(popy.Model):
    pass


class MyAgent(Agent):
    pass


class Home(Location):
    def setup(self):
        self.is_home = True

    def group(self, agent):
        return agent.hid


class School(Location):
    n_agents = 10

    def group(self, agent):
        return 0 if agent.age <= 14 else 1

    def join(self, agent):
        return 6 <= agent.age <= 18

    def can_visit(self, agent):
        pass


simple_fake_data = pd.DataFrame(
    {
        "pid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "hid": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
        "age": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
    },
)


@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_create_agents(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)

    creator = popy.Creator(model=Model())
    agents = creator.create_agents(df=soep, agent_class=MyAgent)

    assert len(agents) == len(soep)

    for i, row in soep.iterrows():
        for col_name in soep.columns:
            assert row[col_name] == getattr(agents[i], col_name)


@pytest.mark.skip()
# @pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000"])
def test_create_locations():
    soep = simple_fake_data.copy()
    model = Model()
    creator = popy.Creator(model=model)

    agents = creator.create_agents(df=soep, agent_class=MyAgent)
    for agent in agents:
        model.env.add_agent(agent)

    locations = creator.create_locations(agents=agents, location_classes=[Home, School])
    for location in locations:
        model.env.add_location(location)

    assert len([location for location in locations if isinstance(location, Home)]) == 4
    assert len([location for location in locations if isinstance(location, School)]) == 2

    for location in locations:
        for agent in location.agents:
            assert location.group(agent) == location.group_id


if __name__ == "__main__":
    test_create_locations()
