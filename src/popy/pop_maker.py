"""Create a population for the simulation."""

import random
from typing import Optional

import pandas as pd

import popy

from .exceptions import PopyException

import warnings

from . import agent as _agent
from . import location as _location

def make_it_a_list_if_it_is_no_list(x):
    if isinstance(x, list):
        return x
    else:
        return [x]

class PopMaker:
    """Create a population for the simulation."""

    def __init__(
        self,
        model: Optional[popy.Model] = None,
        seed: int = 999,
    ) -> None:
        """Instantiate a population maker for a specific model.

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
                if replace_sample_level_column:
                    sample.loc[:, sample_level + "_original"] = sample.loc[:, sample_level]
                    sample.loc[:, sample_level] = sample_cluster_id

                samples.append(sample)

                counter += len(sample)
                sample_cluster_id += 1

            df_sample = pd.concat(samples).reset_index(drop=True)

        return df_sample

    def create_agents(
            self, 
            agent_class, 
            df: pd.DataFrame | None = None,
            n: int | None = None,
            ) -> popy.AgentList:
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
        if df is not None:
            df = df.copy()

            # create one agent for each row in df
            agents = []
            for _, row in df.iterrows():
                agent = agent_class(model=self.model)
                for col_name in df.columns:
                    if col_name == "id":
                        raise Exception("You are not allowed to set an agent attribute called `id`.")
                    else:
                        setattr(agent, col_name, row[col_name])
                agents.append(agent)

        else:
            if n is not None:
                agents = [agent_class(model=self.model) for _ in range(n)]
            else:
                raise Exception("Either `df` or `n` must be not None.")


        agents = popy.AgentList(model=self.model, objs=agents)
        self.agents = agents
        
        # TODO: is this smart?
        #self.model.agents = agents
        
        return self.agents


    def _get_affiliated_agents(self, agents, location_dummy) -> []:
        return [agent for agent in agents if location_dummy.join(agent)]

    def _get_mother_group_id(self, agent: _agent, location_dummy: _location) -> str:
        if location_dummy.nest() is None:
            return "None"
        
        else:
            mother_location = None
            
            # search for mother location assigned to this agent
            n_mother_locations_found = 0
            for location in agent.locations:
                if isinstance(location, location_dummy.nest()):
                    mother_location = location
                    n_mother_locations_found += 1
            
            # Check if the number of mother locations is not 1
            if n_mother_locations_found > 1:
                warnings.warn(
                    f"""For agent {agent},
                    {n_mother_locations_found} locations of class 
                    {location_dummy.nest()} were found as potential mothers of 
                    {location_dummy} in the list of locations."""
                )
            elif n_mother_locations_found == 0:
                raise Exception(
                    f"The mother of {location_dummy} is missing. Are the location classes in the right order?",
                )
            return "-".join([str(mother_location.group_value), str(mother_location.group_id)])


    def _get_split_values(self, agents: [_agent], location_dummy: _location, allow_nesting: bool = False) -> {int | str}:
        all_values = []
        for agent in agents:
            agent_values = make_it_a_list_if_it_is_no_list(location_dummy.split(agent))
            
            if allow_nesting:
                # Add mother location's value to the value of the lower level location
                for i, value in enumerate(agent_values):
                    agent_values[i] = "-".join([self._get_mother_group_id(agent, location_dummy), str(value)])
            
            # Temporarely store group values as agent attribute to assign them to the corresponding location group later
            agent._TEMP_group_values = agent_values
            all_values.extend(agent_values)

        return set(all_values)
    

    def _get_groups(self, agents, location_dummy) -> [[_agent]]:
        # determine the number of groups needed
        if location_dummy.n_locations is None:
            n_location_groups = (
                1
                if location_dummy.size is None
                else max(location_dummy.round_function(len(agents) / location_dummy.size), 1)
            )
        else:
            n_location_groups = location_dummy.n_locations
        
        group_lists = [[] for _ in range(n_location_groups)]
        stick_values = {location_dummy.stick_together(agent) for agent in agents}

        # for each group of sticky agents
        for stick_value in stick_values:
            sticky_agents = [agent for agent in agents if location_dummy.stick_together(agent) == stick_value]
            assigned = False

            # for each group
            for group_list in group_lists:

                # if there are still enough free places available
                if location_dummy.size is None or (location_dummy.size - len(group_list)) >= len(sticky_agents):
                    # assign agents
                    for agent in sticky_agents:
                        group_list.append(agent)
                    assigned = True
                    break

            # if agents are not assigned while all locations are full and overcrowding is enabled
            if not assigned and location_dummy.allow_overcrowding:
                # sort by the number of assigned agents
                group_lists.sort(key=lambda x: len(x))
                
                # assign agents to the group_list with the fewest members
                for agent in sticky_agents:
                    group_lists[0].append(agent)
                assigned = True
        
        random.shuffle(group_lists)
        return group_lists


    def _get_group_value_affiliated_agents(self, agents: [_agent], group_value: int | str) -> [_agent]:
        group_affiliated_agents = [agent for agent in agents if group_value in agent._TEMP_group_values]
        random.shuffle(group_affiliated_agents)
        return group_affiliated_agents


    def _get_melted_groups(self, agents: [_agent], location_dummy: _location) -> [[_agent]]:
        
        # get all mother locations the agents are nested in
        all_mother_group_ids = {self._get_mother_group_id(agent, location_dummy) for agent in agents}
        
        # for each mother location
        for mother_group_id in all_mother_group_ids:
            
            # get agents that are part of this location
            nested_agents = [
                agent for agent in agents 
                if self._get_mother_group_id(agent, location_dummy) == mother_group_id
                ]
            
            # a list that stores a list of groups for each location
            groups_to_melt_by_location: [
                [[_agent], [_agent], [_agent]], # groups of location 1
                [[_agent], [_agent]],           # groups of location 2 
                                                # ...
                ] = []
            
            # for each location that shall be melted
            for location_cls in location_dummy.melt():
                
                # create dummy location
                melt_location_dummy = location_cls(model=self.model)
                melt_location_dummy.setup()
                
                # get all agents that should be assigned to this location
                melt_location_affiliated_agents = self._get_affiliated_agents(
                    agents=nested_agents,
                    location_dummy=melt_location_dummy,
                    )
                
                # get all values for which seperated groups/locations should be created
                melt_group_values = self._get_split_values(
                    agents=melt_location_affiliated_agents, 
                    location_dummy=melt_location_dummy, 
                    allow_nesting=False,
                    )

                # for each split value: get groups and collect them in one list for all values
                location_groups_to_melt: [[_agent]] = []
                for melt_group_value in melt_group_values:
                    melt_group_value_affiliated_agents = self._get_group_value_affiliated_agents(
                        agents=melt_location_affiliated_agents,
                        group_value=melt_group_value,
                    )
                    location_groups_to_melt.extend(
                        self._get_groups(
                            agents=melt_group_value_affiliated_agents, 
                            location_dummy=melt_location_dummy,
                            )
                    )
                random.shuffle(location_groups_to_melt)
                groups_to_melt_by_location.append(location_groups_to_melt)
            
            # Melt groups
            all_melted_groups: [[_agent]] = []
            len_of_longest_list_of_groups_to_melt = sorted([len(l) for l in groups_to_melt_by_location], reverse=True)[0]
            for i in range(len_of_longest_list_of_groups_to_melt):
                melted_group = []
                for groups_to_melt in groups_to_melt_by_location:
                    if len(groups_to_melt) > 0:
                        if location_dummy.multi_melt:
                            melted_group.extend(groups_to_melt[i % len(groups_to_melt)])
                        else:
                            try:
                                melted_group.extend(groups_to_melt[i])
                            except:
                                pass
                                
                                
                            
                all_melted_groups.append(melted_group)
        
        return all_melted_groups


    def _get_cls_as_str(self, cls):
        return str(cls).split(".")[1].split("'")[0]


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
        # TODO: is this smart?
        self.model.agents = agents

        #WaRUM GEHT DAS NICHT???????????????
        random.shuffle(agents)

        locations = []

        # for each location class
        for location_cls in location_classes:

            #WaRUM GEHT DAS NICHT???????????????
            random.shuffle(agents)
            
            # create an agent attribute for this location class and assign unique dummy values
            str_location_cls = self._get_cls_as_str(location_cls)
            for agent in agents:
                setattr(agent, str_location_cls, "None_"+str(agent.id))

            # create location dummy in order to use the location's methods
            location_dummy = location_cls(model=self.model)
            location_dummy.setup()

            # get all agents that could be assigned to locations of this class
            affiliated_agents = self._get_affiliated_agents(agents=agents, location_dummy=location_dummy)

            # get all values that are used to split the agents into groups
            group_values = self._get_split_values(
                agents=affiliated_agents, 
                location_dummy=location_dummy,
                allow_nesting=True,
                )
            
            # for each group split value
            for group_value in group_values:
                # get all agents with that value
                group_value_affiliated_agents = self._get_group_value_affiliated_agents(
                    agents=affiliated_agents, 
                    group_value=group_value,
                    )
                
                # if this location glues together other location
                if location_dummy.melt() is None:
                    group_lists: [[_agent]] = self._get_groups(
                        agents=group_value_affiliated_agents, 
                        location_dummy=location_dummy,
                        )
                else:
                    group_lists: [[_agent]] = self._get_melted_groups(
                        agents=group_value_affiliated_agents, 
                        location_dummy=location_dummy,
                        )
                
                # for each group of agents
                for i, group_list in enumerate(group_lists):
                    location_dummy = location_cls(model=self.model)
                    location_dummy.setup()
                    location_dummy.group_agents = group_list

                    # get all subgroub values
                    subgroup_values = {
                        agent_subgroup_value 
                        for agent in group_list 
                        for agent_subgroup_value 
                        in make_it_a_list_if_it_is_no_list(location_dummy.subsplit(agent))
                        }
                    
                    # for each group of agents assigned to a specific sublocation
                    for j, subgroup_value in enumerate(subgroup_values):
                        
                        # get all subgroup affiliated agents
                        subgroup_affiliated_agents = []
                        
                        #for agent in group_affiliated_agents:
                        for agent in group_list:
                            agent_subgroup_value = make_it_a_list_if_it_is_no_list(location_dummy.subsplit(agent))
                            if subgroup_value in agent_subgroup_value:
                                subgroup_affiliated_agents.append(agent)
                            
                        # Build the final location
                        subgroup_location = location_cls(model=self.model)
                        subgroup_location.setup()
                        subgroup_location.group_value = group_value
                        subgroup_location.subgroup_value = subgroup_value
                        subgroup_location.group_id = i
                        subgroup_location.subgroup_id = j
                        subgroup_location.group_agents = group_list # maybe delete later
                        
                        # Assigning process:
                        for agent in subgroup_affiliated_agents:
                            subgroup_location.add_agent(agent)

                            group_info_str = f"gv={subgroup_location.group_value}, gid={subgroup_location.group_id}"
                            
                            setattr(agent, str_location_cls, group_info_str)
                            
                            # TODO: DELETE LATER
                            agent._initial_locations.append(
                                "| " + str_location_cls + ": " + group_info_str,
                                )
                            
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
        
        # delete temporary agent attributes
        for agent in self.model.agents:
            if hasattr(agent, "_TEMP_group_values"):
                del(agent._TEMP_group_values)

        # delete temporary location attributes
        for location in locations:
            del(location.group_agents)
            
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
