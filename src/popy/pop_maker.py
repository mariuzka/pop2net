"""Create a population for the simulation."""

import random
from typing import Optional

import pandas as pd

import popy
from popy import utils

from .exceptions import PopyException

class PopMaker:
    """Create a population for the simulation."""

    def __init__(
        self,
        model: popy.Model,
        seed: int = 999,
    ) -> None:
        """Instantiate a population make for a specific model.

        Args:
            model (popy.Model): Model, for which a population should be created
            seed (int, optional): A seed for reproducibility. Defaults to 999.
        """
        # TODO: Seed should default to None.
        self.model = model
        self.rng = random.Random(seed)
        self.agents: Optional[popy.AgentList] = None
        self.locations: Optional[popy.LocationList] = None

    def draw_sample(
        self,
        df: pd.DataFrame,
        n: int,
        sample_level: Optional[str] = None,
        weight: Optional[str] = None,
    ) -> pd.DataFrame:
        """Draw a sample from a base population.

        Args:
            df (:class:`pandas.DataFrame`): DF of the actual population
            n (int): Target size of the final sample. If this is higher the the size of the input
                DataFrame, the sampling will occure with replacement. Without otherwise.
            sample_level (str, optional): A variable the specifies groups in the data. For
                instance a household ID to sample by households. Defaults to None.
            weight (str, optional): _description_. Defaults to None.

        Returns:
            The drawn sample.
        """
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

    def create_agents(self, df: pd.DataFrame, agent_class) -> popy.AgentList:
        """Creates one agent-instance of the given agent-class for each row of the given df.

        All columns of the df are added as instance attributes containing the row-specific values
        of the specific column.

        Args:
            df (:class:`pandas.DataFrame`): _description_
            agent_class: A class to instantiate all agents with. Every column in the DataFrame will
                result in an attribute of the agents.

        Returns:
            A list of agents, created based on the input.
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
        """_summary_.

        Args:
            agents (_type_): _description_
            location_classes (_type_): _description_

        Returns:
            _type_: _description_
        """
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
        """_summary_.

        Raises:
            PopyException: _description_
            PopyException: _description_
        """
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
        """_summary_.

        Raises:
            PopyException: _description_

        Returns:
            pd.DataFrame: _description_
        """
        if self.agents is None:
            msg = "There are no agents."
            raise PopyException(msg)

        return pd.DataFrame([vars(agent) for agent in self.agents])
