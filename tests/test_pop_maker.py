import agentpy as ap
import pytest

from src.pop_maker import PopMaker


class Model(ap.Model):
    pass


class Agent(ap.Agent):
    pass


@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_create_agents(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)

    pop_maker = PopMaker(df=soep, agent_class=Agent, agent_params={"model": Model()})
    agents = pop_maker.create_agents()

    assert len(agents) == len(soep)

    for i, row in soep.iterrows():
        for col_name in soep.columns:
            assert row[col_name] == getattr(agents[i], col_name)
