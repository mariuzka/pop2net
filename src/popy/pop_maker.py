import random
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import agentpy as ap
import pandas as pd
import popy
import popy.utils as utils

from .exceptions import PopyException


class PopMaker:
    def __init__(
        self,
        model: popy.Model,
        seed: int = 999,
    ) -> None:
        self.model = model
        self.rng = random.Random(seed)
        self.agents: Optional[popy.AgentList] = None
        self.locations: Optional[popy.LocationList] = None

    def create_agents(self, df, agent_class):
        """
        Creates one agent-instance of the given agent-class for each row of the given df.
        All columns of the df are added as instance attributes containing the row-specific values of the specific column.
        """
        agents = []
        for _, row in df.iterrows():
            agent = agent_class(model=self.model)
            for col_name in df.columns:
                setattr(agent, col_name, row[col_name])
            agents.append(agent)

        self.agents = popy.AgentList(model=self.model, objs=agents)

        return self.agents

    def create_locations(
        self,
        agents,
        location_classes,
    ):
        # check if there is exactly one home location among the given location classes
        self.check_home_location(location_classes=location_classes)

        locations = []

        for location_cls in location_classes:

            # create location dummy in order to use the location's methods
            location_dummy = location_cls(model=self.model)
            location_dummy.setup()

            # get all agents that could be assigned to locations of this type
            affiliated_agents = [agent for agent in agents if location_dummy.can_affiliate(agent)]

            # get all possible subtype-labels of this location class
            location_subtypes = {location_dummy.groupby(agent) for agent in affiliated_agents}

            for subtype in location_subtypes:

                # get all agents that could be assigned to locations of this subtype
                subtype_affiliated_agents = [
                    agent
                    for agent in affiliated_agents
                    if location_dummy.groupby(agent) == subtype
                ]

                # determine the number of locations needed of this subtype
                n_location_subtypes = (
                    1
                    if location_dummy.size is None
                    else max(round(len(subtype_affiliated_agents) / location_dummy.size), 1)
                )

                # create the required number of instances of locations of this subtype
                subtype_locations = [
                    location_cls(model=self.model) for _ in range(n_location_subtypes)
                ]

                for location in subtype_locations:
                    location.setup()
                    location.subtype = subtype

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
                        random_location.add_agent(agent)
                        assigned = True

        self.agents = agents
        self.locations = popy.LocationList(
            model=self.model,
            objs=locations,
        )  # Warum gibt es keinen Fehler, wenn man ein Argument falsch schreibt? Habe gerade ewig nach einem Bug gesucht und letzt hatte ich nur das "j" in "objs" vergessen

        return self.locations

    def eval_affiliations(self) -> None:
        if self.agents is None:
            raise PopyException("You have to create agents first!")

        if self.locations is None:
            raise PopyException("You have to create locations first!")

        df_locations = pd.DataFrame(
            [
                {
                    "location_class": str(type(location)).split(".")[-1].split("'")[0],
                    "n_agents": len(location.agents),
                }
                for location in self.locations
            ],
        )

        print(self.locations)
        utils.print_header("Number of agents per location")
        print(df_locations.groupby("location_class").describe())

        df_agents = pd.DataFrame(
            [
                {
                    "agent_id": agent.id,
                    "n_affiliated_locations": len(agent.locations),
                }
                for agent in self.agents
            ],
        )

        utils.print_header("Number of affiliated locations per agent")
        print(df_agents.n_affiliated_locations.describe())

    def get_df_agents(self) -> pd.DataFrame:
        if self.agents is None:
            raise PopyException("There are no agents.")

        return pd.DataFrame([vars(agent) for agent in self.agents])

    def check_home_location(self, location_classes):
        # evtl. später entfernen, weil nicht allgemein genug.
        # Es kann auch Simulationen geben, in denen es keine Homelocation braucht oder
        # diese für unterschiedliche Agenten jeweils unterschiedliche Locationclasses sind.

        n_home_locations = 0
        for location_cls in location_classes:
            location_dummy = location_cls(model=self.model)
            location_dummy.setup()
            if location_dummy.is_home:
                n_home_locations += 1

        if n_home_locations != 1:
            raise PopyException(
                f"There must be exactly one class of locations that is defined as a home location. Currently there are {n_home_locations}",
            )
