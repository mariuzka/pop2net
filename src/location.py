from typing import List
from typing import Optional

import agentpy as ap


class Location:
    """The place where agents encounter each other."""

    def __init__(self, model, category: Optional[str] = None, max_size: Optional[int] = None):

        self.model = model
        self.category = category
        self.max_size = max_size

        self.visitors_of_the_day: List[int] = []
        self.n_associated_agents: int = 0

    def __repr__(self) -> str:
        return f"Location(category={self.category}"

    def can_visit(self, agent):
        return True

    def visit(self, agent):
        if self.can_visit(agent):
            self.visitors_of_the_day.append(agent)

    def clear_visitors(self):
        self.visitors_of_the_day = []

    def connect_visitors(self):
        for i, agent_i in enumerate(list(self.visitors_of_the_day)):
            for agent_j in list(self.visitors_of_the_day):
                if agent_i == agent_j:
                    continue
                agent_i.add_contact(agent_j)

        self.clear_visitors()
