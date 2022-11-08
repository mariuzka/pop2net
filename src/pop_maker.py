from typing import Dict
from typing import List
from typing import Optional


class PopMaker:
    def __init__(
        self,
        df,
        agent_class,
        agent_params: Optional[Dict] = None,
        location_classes: Optional[List] = None,
    ) -> None:
        self.df = df
        self.location_classes = location_classes
        self.agent_class = agent_class
        self.agent_params = agent_params

    def create_agents(self) -> List:
        """
        Creates one agent-instance of the given agent-class for each row of the given df.
        All columns of the df are added as instance attributes containing the row-specific values of the specific column.
        """
        agents = []
        for _, row in self.df.iterrows():
            agent = self.agent_class(**self.agent_params)
            for col_name in self.df.columns:
                setattr(agent, col_name, row[col_name])
            agents.append(agent)

        return agents

    def create_locations(self, agents):
        for agent in agents:
            pass
