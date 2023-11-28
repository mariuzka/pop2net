"""Create a population for the simulation."""

import random
from typing import Optional

import pandas as pd

import popy
from popy import utils

import math

from .exceptions import PopyException

class PopMaker:
    """Create a population for the simulation."""

    def __init__(
        self,
        model: Optional[popy.Model] = None,
        seed: int = 999,
    ) -> None:
        """Instantiate a population make for a specific model.

        Args:
            model (popy.Model): Model, for which a population should be created
            seed (int, optional): A seed for reproducibility. Defaults to 999.
        """
        # TODO: Seed should default to None.
        
        self.model = model if model is not None else popy.Model()
        self.seed = seed
        self.rng = random.Random(seed)
        self.agents: Optional[popy.AgentList] = None
        self.locations: Optional[popy.LocationList] = None

    def draw_sample(
        self,
        df: pd.DataFrame,
        n: Optional[int] = None,
        sample_level: Optional[str] = None,
        sample_weight: Optional[str] = None,
        replace_sample_level_column: bool = True,
    ) -> pd.DataFrame:
        """Draw a sample from a base population.

        Args:
            df (:class:`pandas.DataFrame`): DF of the actual population
            n (int): Target size of the final sample. If this is higher the the size of the input
                DataFrame, the sampling will occure with replacement. Without otherwise. If `n` is
                set to `None`, df is returned as it is.
            sample_level (str, optional): A variable the specifies groups in the data. For
                instance a household ID to sample by households. Defaults to None.
            sample_weight (str, optional): _description_. Defaults to None.

        Returns:
            The drawn sample.
        """
        
        # TODO: Möglichkeit einbauen, zu erzwingen n_agents genau zu treffen, falls sample_level an ist
        
        df = df.copy()

        if n is None:
            return df

        elif sample_level is None:
            df_sample = df.sample(
                n=n,
                replace=not (n <= len(df) and sample_weight is None),
                weights=sample_weight,
                random_state=self.seed,
            )

        else:
            sample_level_ids = list(df[sample_level].drop_duplicates())

            if sample_weight is not None:
                weights = list(df.drop_duplicates(subset=sample_level)[sample_weight])

            samples = []
            counter = 0
            sample_cluster_id = 1
            while counter < n:
                if sample_weight is None:
                    random_id = self.rng.choice(sample_level_ids)
                else:
                    random_id = self.rng.choices(sample_level_ids, weights=weights, k=1)[0]

                sample = df.loc[df[sample_level] == random_id, :].copy()
                
                # create new unique ids for sample level variable
                # TODO: Hinweis/Warnung printen, dass die originale sample_level-Spalte ersetzt wurde
                if replace_sample_level_column:
                    sample.loc[:, sample_level + "_original"] = sample.loc[:, sample_level]
                    sample.loc[:, sample_level] = sample_cluster_id

                samples.append(sample)

                counter += len(sample)
                sample_cluster_id += 1

            df_sample = pd.concat(samples).reset_index(drop=True)

        return df_sample

    def create_agents(self, df: pd.DataFrame, agent_class) -> popy.AgentList:
        """Creates one agent-instance of the given agent-class for each row of the given df.

        All columns of the df are added as instance attributes containing the row-specific values
        of the specific column.

        Args:
            df: The DataFrame from which the agents should be created from.
            agent_class: A class to instantiate all agents with. Every column in the DataFrame will
                result in an attribute of the agents.

        Returns:
            A list of agents, created based on the input.
        """
        df = df.copy()

        # create one agent for each row in df

        # TODO: sicherstellen, dass kein Attribut mit dem Namen `id` erstellt wird
        agents = []
        for _, row in df.iterrows():
            agent = agent_class(model=self.model)
            for col_name in df.columns:
                setattr(agent, col_name, row[col_name])
            agents.append(agent)

        agents = popy.AgentList(model=self.model, objs=agents)
        self.agents = agents

        # TODO: is this smart?
        self.model.agents = agents
        
        return self.agents

    def create_locations(
        self,
        agents,
        location_classes,
        round_function = math.ceil,
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
            
            # get all group values
            location_groups = []
            for agent in affiliated_agents:
                agent_group_value = location_dummy.group(agent)
                if isinstance(agent_group_value, list):
                    location_groups.extend(agent_group_value)
                else:
                    location_groups.append(agent_group_value)
            location_groups = set(location_groups)

            for group in location_groups:
                # get all group affiliated agents
                group_affiliated_agents = []
                for agent in affiliated_agents:
                    agent_group_value = location_dummy.group(agent)
                    if isinstance(agent_group_value, list):
                        if group in agent_group_value:
                            group_affiliated_agents.append(agent)
                    else:
                        if group == agent_group_value:
                            group_affiliated_agents.append(agent)
                

                #####################################################################################################

                ### get group lists

                # determine the number of groups needed
                n_location_groups = (
                    1
                    if location_dummy.size is None
                    else max(round_function(len(group_affiliated_agents) / location_dummy.size), 1)
                )
                
                group_lists = [[] for _ in range(n_location_groups)]
                stick_values = {location_dummy.stick_together(agent) for agent in group_affiliated_agents}

                # for each group of sticky agents
                for stick_value in stick_values:
                    sticky_agents = [agent for agent in group_affiliated_agents if location_dummy.stick_together(agent) == stick_value]
                    assigned = False

                    # for each location of this group
                    for group_list in group_lists:

                        # if there are still enough free places available
                        if location_dummy.size is None or (location_dummy.size - len(group_list)) >= len(sticky_agents):
                            # assign agents
                            for agent in sticky_agents:
                                group_list.append(agent)
                            assigned = True
                            break

                    # if agents are not assigned and all locations are full
                    # TODO: hier verschiedene Möglichkeiten anbieten, was passieren soll, wenn Agenten übrigen bleiben
                    if not assigned:
                        random_group_list = self.rng.choice(group_lists)
                        # assign agents
                        for agent in sticky_agents:
                            random_group_list.append(agent)
                        assigned = True

                #####################################################################################################
                
                for i, group_list in enumerate(group_lists):
                    location_dummy = location_cls(model=self.model)
                    location_dummy.setup()
                    location_dummy.group_agents = group_list

                    # get all subgroub values
                    location_subgroups = []
                    for agent in group_list:
                        agent_subgroup_value = location_dummy.subgroup(agent)
                        if isinstance(agent_subgroup_value, list):
                            location_subgroups.extend(agent_subgroup_value)
                        else:
                            location_subgroups.append(agent_subgroup_value)
                    location_subgroups = set(location_subgroups)
                    
                    for j, subgroup in enumerate(location_subgroups):
                        
                        # get all subgroup affiliated agents
                        subgroup_affiliated_agents = []
                        
                        #for agent in group_affiliated_agents:
                        for agent in group_list:
                            agent_subgroup_value = location_dummy.subgroup(agent)
                            
                            if isinstance(agent_subgroup_value, list):
                                if subgroup in agent_subgroup_value:
                                    subgroup_affiliated_agents.append(agent)
                            else:
                                if subgroup == agent_subgroup_value:
                                    subgroup_affiliated_agents.append(agent)
                        
                        subgroup_location = location_cls(model=self.model)
                        subgroup_location.setup()
                        subgroup_location.group_value = group
                        subgroup_location.subgroup_value = subgroup
                        subgroup_location.group_id = i
                        subgroup_location.subgroup_id = j
                        
                        # Assigning process:
                        for agent in subgroup_affiliated_agents:
                            subgroup_location.add_agent(agent)
                        
                        locations.append(subgroup_location)

        # TODO:
        # Warum gibt es keinen Fehler, wenn man ein Argument falsch schreibt? Habe gerade ewig
        # nach einem Bug gesucht und letzt hatte ich nur das "j" in "objs" vergessen
        self.agents = agents
        self.locations = popy.LocationList(
            model=self.model,
            objs=locations,
        )
        # is this smart?
        self.model.locations = locations

        # execute an action after all locations have been created
        for location in self.locations:
            location.do_this_after_creation()

        return self.locations


    def make(
        self,
        df: pd.DataFrame,
        agent_class,
        location_classes,
        n_agents: Optional[int] = None,
        sample_level: Optional[str] = None,
        sample_weight: Optional[str] = None,
        replace_sample_level_column: bool = True,
    ) -> tuple:
        """Creates agents and locations based on a given dataset.

        Combines the PopMaker-methods `draw_sample()`, `create_agents()` and `create_locations()`.

        Args:
            df (pd.DataFrame): A data set with individual data that forms the basis for
                the creation of agents. Each row is (potentially) translated into one agent.
                Each column is translated into one agent attribute.
            agent_class (_type_): The class from which the agent instances are created.
            location_classes (_type_): The class from which the location instances are created.
            n_agents (Optional[int], optional): The number of agents that will be created.
                If `n_agents` is set to None, each row of `df` is translated into exactly one agent.
                Otherwise, rows are randomly drawn (with replacement,
                if `n_agents > len(df)`) from `df` until the number of agents created
                equals `n_agents`.
            sample_level (Optional[str], optional): If `sample_level` is None,
                the rows are sampled individually.
                Otherwise the rows are sampled as groups. `sample_level` defines
                which column of `df` contains the group id.

        Returns:
            tuple: _description_
        """
        # draw a sample from dataset
        df_sample = self.draw_sample(
            df=df, 
            n=n_agents, 
            sample_level=sample_level, 
            sample_weight=sample_weight,
            replace_sample_level_column=replace_sample_level_column,
            )

        # create agents
        agents = self.create_agents(df=df_sample, agent_class=agent_class)

        # create locations
        locations = self.create_locations(agents=agents, location_classes=location_classes)

        return agents, locations


    def eval_affiliations(self) -> None:
        """Prints information on the distribution of agents per location and locations per agent.

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
        """Returns the latest created population of agents as a dataframe.

        Raises:
            PopyException: _description_

        Returns:
            pd.DataFrame: A dataframe which contains one row for each
            agent and one column for each agent attribute.
        """
        if self.agents is None:
            msg = "There are no agents."
            raise PopyException(msg)

        return pd.DataFrame([vars(agent) for agent in self.agents])
