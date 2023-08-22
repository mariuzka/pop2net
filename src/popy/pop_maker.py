import random
from typing import Optional

import pandas as pd

import popy
from popy import utils

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

    def draw_sample(
        self,
        df,
        n,
        sample_level: Optional[str] = None,
        weight: Optional[str] = None,
    ) -> pd.DataFrame:

        if sample_level is None:
            df_sample = df.sample(
                n=n,
                replace=not (n <= len(df) and weight is None),
                weights=weight,
            )

        else:
            sample_level_ids = list(df[sample_level].drop_duplicates())

            if weight is not None:
                weights = list(df.drop_duplicates(subset=sample_level)[weight])

            samples = []
            counter = 0
            while counter < n:
                if weight is None:
                    random_id = random.choice(sample_level_ids)
                else:
                    random_id = random.choices(sample_level_ids, weights=weights, k=1)[0]

                sample = df.loc[df[sample_level] == random_id, :]
                samples.append(df.loc[df[sample_level] == random_id, :])

                counter += len(sample)

            df_sample = pd.concat(samples).reset_index(drop=True)

        return df_sample

    def create_agents(self, df, agent_class):
        """Creates one agent-instance of the given agent-class for each row of the given df.
        All columns of the df are added as instance attributes containing the row-specific values
        of the specific column.
        """
        # create one agent for each row in
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

        locations = []

        for location_cls in location_classes:

            # create location dummy in order to use the location's methods
            location_dummy = location_cls(model=self.model)
            location_dummy.setup()

            # get all agents that could be assigned to locations of this type
            affiliated_agents = [agent for agent in agents if location_dummy.join(agent)]

            # get all possible subtype-labels of this location class
            location_subtypes = {location_dummy.group(agent) for agent in affiliated_agents}

            for subtype in location_subtypes:

                # get all agents that could be assigned to locations of this subtype
                subtype_affiliated_agents = [
                    agent for agent in affiliated_agents if location_dummy.group(agent) == subtype
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
                # Should we keep assigning process here for the sake of efficiency or move it into
                # another method for the sake of modularity?
                for agent in subtype_affiliated_agents:
                    assigned = False
                    for location in subtype_locations:
                        if location.size is None or location.n_affiliated_agents < location.size:
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
        )  # Warum gibt es keinen Fehler, wenn man ein Argument falsch schreibt? Habe gerade ewig
        # nach einem Bug gesucht und letzt hatte ich nur das "j" in "objs" vergessen

        return self.locations

    def eval_affiliations(self) -> None:
        if self.agents is None:
            msg = "You have to create agents first!"
            raise PopyException(msg)

        if self.locations is None:
            msg = "You have to create locations first!"
            raise PopyException(msg)

        df_locations = pd.DataFrame(
            [
                {
                    "location_class": str(type(location)).split(".")[-1].split("'")[0],
                    "n_agents": len(location.agents),
                }
                for location in self.locations
            ],
        )

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
            msg = "There are no agents."
            raise PopyException(msg)

        return pd.DataFrame([vars(agent) for agent in self.agents])
