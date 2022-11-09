import random
from typing import Dict
from typing import List
from typing import Optional

import agentpy as ap


class PopMaker:
    def __init__(
        self,
        df,
        agent_class,
        location_classes: Optional[List] = None,
        model: Optional[ap.Model] = None,
        seed: int = 999,
    ) -> None:
        self.df = df
        self.location_classes = location_classes
        self.agent_class = agent_class
        self.model = model
        self.rng = random.Random(seed)

    def create_agents(self) -> List:
        """
        Creates one agent-instance of the given agent-class for each row of the given df.
        All columns of the df are added as instance attributes containing the row-specific values of the specific column.
        """
        agents = []
        for _, row in self.df.iterrows():
            agent = self.agent_class(model=self.model)
            for col_name in self.df.columns:
                setattr(agent, col_name, row[col_name])
            agents.append(agent)

        return agents

    def create_locations(self, agents):
        locations = []

        for location_cls in self.location_classes:
            location_dummy = location_cls(model=self.model)
            location_dummy.setup()

            affiliated_agents = [agent for agent in agents if location_dummy.can_affiliate(agent)]

            location_subtypes = {location_dummy.subtype(agent) for agent in affiliated_agents}

            for subtype in location_subtypes:
                print(type(location_dummy))
                print(subtype)

                subtype_affiliated_agents = [
                    agent for agent in agents if location_dummy.subtype(agent) == subtype
                ]

                n_location_subtypes = (
                    1
                    if location_dummy.size is None
                    else max(round(len(subtype_affiliated_agents) / location_dummy.size), 1)
                )

                subtype_locations = [
                    location_cls(model=self.model) for _ in range(n_location_subtypes)
                ]

                for location in subtype_locations:
                    location.setup()

                locations.extend(subtype_locations)

                # Assign agents to locations
                # Should we keep assigning process here for the sake of efficiency or move it into another method for the sake of modularity?
                for agent in subtype_affiliated_agents:
                    assigned = False
                    for location in subtype_locations:
                        if location.size is None or location.n_current_visitors < location.size:
                            assert not assigned  # remove later
                            location.add_agent(agent)
                            assigned = True
                            break

                    if not assigned:

                        random_location = self.rng.choice(subtype_locations)
                        random_location.add_agents(agent)
                        assigned = True

        return locations
