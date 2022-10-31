import statistics as stats

import agentpy as ap


class PopyAgent(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self._model = model
        self.contacts = set()
        self.contact_diary = []
        self.locations = []

    @property
    def _n_agents_ever_met(self) -> int:
        return len(self._contacts)

    @property
    def _mean_hours_not_at_home(self) -> float:
        return stats.mean(self._hours_not_at_home)

    @property
    def _max_hours_not_at_home(self) -> int:
        return max(self._hours_not_at_home)

    @property
    def my_diary(self):
        return list(self.contact_diary)

    def add_contact(self, agent) -> None:
        self.contact_diary.append(agent.id)

    def add_location(self, location) -> None:
        self.locations.append(location)

    def clean_diary(self) -> None:
        self.contact_diary = ap.AgentList(self.model)

    def visit_locations(self, model) -> None:
        """
        Agent visits all its locations and writes its visit in the locations' daily guest books,
        if the corresponding visiting conditions are met.
        """

        # for each location category the agent has in its dictionary of locations
        for location in self.locations:
            location.visit(self)
