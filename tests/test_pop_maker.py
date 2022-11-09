import agentpy as ap
import pandas as pd
import pytest

from src.location import Location
from src.pop_maker import PopMaker


class Model(ap.Model):
    pass


class Agent(ap.Agent):
    pass


class Home(Location):
    def subtype(self, agent):
        return agent.hid


class School(Location):
    def setup(self):
        self.size = 10

    def subtype(self, agent):
        return 0 if agent.age <= 14 else 1

    def can_affiliate(self, agent):
        return 6 <= agent.age <= 18


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

    pop_maker = PopMaker(df=soep, agent_class=Agent, model=Model())
    agents = pop_maker.create_agents()

    assert len(agents) == len(soep)

    for i, row in soep.iterrows():
        for col_name in soep.columns:
            assert row[col_name] == getattr(agents[i], col_name)


# @pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000"])
def test_create_locations():
    soep = simple_fake_data.copy()
    pop_maker = PopMaker(
        df=soep,
        location_classes=[Home, School],
        agent_class=Agent,
        model=Model(),
    )
    agents = pop_maker.create_agents()
    locations = pop_maker.create_locations(agents=agents)

    assert len([location for location in locations if type(location) == Home]) == 4
    assert len([location for location in locations if type(location) == School]) == 2

    # TODO: test if the process of assigning agents to locations is correct


if __name__ == "__main__":
    test_create_locations()
