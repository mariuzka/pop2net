import agentpy as ap
import pytest

from src.pop_maker import PopMaker


class Model(ap.Model):
    pass


class TestAgent(ap.Agent):
    pass


def test_create_agents(soep100):

    pop_maker = PopMaker(df=soep100, agent_class=TestAgent, agent_params={"model": Model()})
    agents = pop_maker.create_agents()

    assert len(agents) == len(soep100)

    for i, row in soep100.iterrows():
        for col_name in soep100.columns:
            assert row[col_name] == getattr(agents[i], col_name)
