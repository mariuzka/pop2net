"""Create a population for the simulation."""

from __future__ import annotations

import math
import random
import warnings

import pandas as pd

import pop2net as p2n
import pop2net.utils as utils

from .exceptions import Pop2netException


class Creator:
    """Creates and connects agents and locations."""

    def __init__(
        self,
        model: p2n.Model,
        seed: int = None,
    ) -> None:
        """Instantiate a creator for a specific model.

        Args:
            model (p2n.Model): Model, for which a population should be created
            seed (int, optional): A seed for reproducibility. Defaults to 999.
        """
        self.model = model
        self.seed = seed
        self.rng = random.Random(seed)
        self._dummy_model = p2n.Model()

    def _create_dummy_location(self, location_cls) -> p2n.Location:
        location = location_cls(model=self._dummy_model)
        location.setup()
        return location

    def draw_sample(
        self,
        df: pd.DataFrame,
        n: int | None = None,
        sample_level: str | None = None,
        sample_weight: str | None = None,
        replace_sample_level_column: bool = True,
    ) -> pd.DataFrame:
        """Draw a sample from a dataframe.

        Args:
            df (:class:`pandas.DataFrame`): a pandas DataFrame
            n (int): Target size of the final sample. If this is higher the size of the input
                DataFrame, the sampling will occure with replacement. Without otherwise. If `n` is
                set to `None`, df is returned as it is.
            sample_level (str, optional): A variable the specifies sample units,
                i.e. rows that should always
            be sampled together. For instance, a household ID to sample by households.
                Defaults to None.
            sample_weight (str, optional): The column of df which should be used as
                probability weight. Defaults to None.
            replace_sample_level_column (bool): Should the original values of the sample level be
                overwritten by unique values after sampling to avoid duplicates?

        Returns:
            A pandas DataFrame.
        """
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
        agent_class=p2n.Agent,
        agent_class_attr: None | str = None,
        agent_class_dict: None | dict = None,
        df: pd.DataFrame | None = None,
        n: int | None = None,
    ) -> p2n.AgentList:
        """Creates agents from a pandas DataFrame.

        Creates one agent-instance of the given agent-class for each row of the given df,
        if df is not None.
        All columns of the df are added as instance attributes containing the row-specific values
        of the specific column.
        If df is None and n is not None, n default agents without any additional attributes are
        created.

        Args:
            agent_class: A class to instantiate all agents with. Every column in the DataFrame will
                result in an attribute of the agents.
            df: The DataFrame from which the agents should be created from.
            n: The number of agents that should be created. Defaults to None.
            clear_agents: Should existing agents be removed before creating new ones?

        Returns:
            A list of agents.
        """
        if df is not None:
            df = df.copy()

            # create one agent for each row in df
            agents = []
            for _, row in df.iterrows():
                if agent_class_dict is None:
                    agent = agent_class(model=self.model)
                else:
                    agent = agent_class_dict[row[agent_class_attr]](model=self.model)

                for col_name in df.columns:
                    if col_name == "id":
                        msg = "You are not allowed to set an agent attribute called `id`."
                        raise Exception(msg)
                    else:
                        setattr(agent, col_name, row[col_name])
                agents.append(agent)

        else:
            if n is not None:
                agents = [agent_class(model=self.model) for _ in range(n)]
            else:
                msg = "Either `df` or `n` must be not None."
                raise Exception(msg)

        agents = p2n.AgentList(model=self.model, objs=agents)

        return agents

    def _get_affiliated_agents(self, agents, dummy_location) -> list:
        return [agent for agent in agents if dummy_location.filter(agent)]

    def _get_mother_group_id(self, agent, dummy_location) -> str:
        if dummy_location.nest() is None:
            return "None"

        else:
            # search for mother location assigned to this agent
            n_mother_locations_found = 0
            for location in agent.locations:
                if isinstance(location, dummy_location.nest()):
                    mother_location = location
                    n_mother_locations_found += 1

            # Check if the number of mother locations is not 1
            if n_mother_locations_found > 1:
                warnings.warn(
                    f"""For agent {agent},
                    {n_mother_locations_found} locations of class
                    {dummy_location.nest()} were found as potential mothers of
                    {dummy_location} in the list of locations.""",
                    stacklevel=2,
                )
            elif n_mother_locations_found == 0:
                return "None"

            return "-".join([str(mother_location.split_value), str(mother_location.group_id)])

    def _get_split_values(
        self,
        agents: list,
        dummy_location,
        allow_nesting: bool = False,
    ) -> list[int | str]:
        all_values = []
        for agent in agents:
            agent_values = utils._to_list(dummy_location.split(agent))

            if allow_nesting:
                # Add mother location's value to the value of the lower level location
                for i, value in enumerate(agent_values):
                    mother_group_id = self._get_mother_group_id(agent, dummy_location)
                    agent_values[i] = "-".join([mother_group_id, str(value)])
                    setattr(agent, f"_TEMP_{dummy_location.type}_mother_group_id", mother_group_id)

            # Temporarely store group values as agent attribute
            # to assign them to the corresponding location group later
            agent._TEMP_split_values = agent_values

            for value in agent_values:
                if value not in all_values:
                    all_values.append(value)

        return all_values

    def _get_stick_value(self, agent, dummy_location):
        stick_value = dummy_location.stick_together(agent)
        if stick_value is None:
            return "None" + str(agent.id)
        else:
            return stick_value

    def _get_groups(self, agents, location_cls) -> list[list]:
        overcrowding_i = 0

        dummy_location = self._create_dummy_location(location_cls)

        n_location_groups_is_fixed = False

        # determine the number of groups needed
        if dummy_location.n_locations is None and dummy_location.n_agents is None:
            n_location_groups = 1
            groups: list[list] = [[]]

        elif dummy_location.n_locations is None and dummy_location.n_agents is not None:
            if dummy_location.overcrowding is None:
                round_function = round
            elif dummy_location.overcrowding is True:
                round_function = math.floor
            elif dummy_location.overcrowding is False:
                round_function = math.ceil
            else:
                # TODO
                raise Exception

            n_location_groups = max(
                round_function(len(agents) / dummy_location.n_agents),
                1,
            )
            groups: list[list] = [[]]

        elif dummy_location.n_locations is not None and dummy_location.n_agents is None:
            n_location_groups = dummy_location.n_locations
            location_cls.n_agents = max(
                math.floor(len(agents) / n_location_groups),
                1,
            )
            groups: list[list] = [[] for _ in range(n_location_groups)]

        elif dummy_location.n_locations is not None and dummy_location.n_agents is not None:
            n_location_groups = dummy_location.n_locations
            n_location_groups_is_fixed = True
            groups: list[list] = [[]]

        else:
            # TODO:
            raise Exception

        stick_values = {self._get_stick_value(agent, dummy_location) for agent in agents}

        # dummy_location = self._create_dummy_location(location_cls)

        # for each group of sticky agents
        for stick_value in stick_values:
            sticky_agents = [
                agent
                for agent in agents
                if self._get_stick_value(agent, dummy_location) == stick_value
            ]

            assigned = False

            for _, group in enumerate(groups):
                # if there are still enough free places available
                if (dummy_location.n_agents is None) or dummy_location.n_agents - len(group) >= len(
                    sticky_agents
                ):
                    # if sum(
                    #    [dummy_location.find(agent) for agent in sticky_agents],
                    # ) == len(sticky_agents):
                    #    # assign agents
                    for agent in sticky_agents:
                        group.append(agent)
                        dummy_location.add_agent(agent)

                    assigned = True
                    break

            if not assigned:
                if len(groups) < n_location_groups:
                    new_group = []
                    dummy_location = self._create_dummy_location(location_cls)
                    # assign agents
                    for agent in sticky_agents:
                        new_group.append(agent)
                        dummy_location.add_agent(agent)

                    groups.append(new_group)

                else:
                    if not dummy_location.only_exact_n_agents and not n_location_groups_is_fixed:
                        for agent in sticky_agents:
                            groups[overcrowding_i].append(agent)
                        overcrowding_i = (overcrowding_i + 1) % len(groups)

        if dummy_location.only_exact_n_agents:
            groups = [group for group in groups if len(group) == dummy_location.n_agents]

        return groups

    def _get_split_value_affiliated_agents(
        self,
        agents: list,
        split_value: int | str,
    ) -> list:
        group_affiliated_agents = [
            agent for agent in agents if split_value in agent._TEMP_split_values
        ]

        return group_affiliated_agents

    def _get_melted_groups(self, agents: list, location_cls) -> list[list]:
        dummy_location = self._create_dummy_location(location_cls)

        # get all mother locations the agents are nested in
        all_mother_group_ids = {
            self._get_mother_group_id(agent, dummy_location) for agent in agents
        }

        # for each mother location
        for mother_group_id in all_mother_group_ids:
            # get agents that are part of this location
            nested_agents = [
                agent
                for agent in agents
                if self._get_mother_group_id(agent, dummy_location) == mother_group_id
            ]

            # a list that stores a list of groups for each location
            # [
            # [[_agent], [_agent], [_agent]], # groups of location 1
            # [[_agent], [_agent]],           # groups of location 2
            # ]
            groups_to_melt_by_location: list[list[list]] = []

            # for each location that shall be melted
            for melt_location_cls in dummy_location.melt():
                # create dummy location
                melt_dummy_location = self._create_dummy_location(melt_location_cls)
                if melt_location_cls.n_locations is None:
                    melt_location_cls.n_locations = location_cls.n_locations

                # get all agents that should be assigned to this location
                # filter by melt_location
                melt_location_affiliated_agents = self._get_affiliated_agents(
                    agents=nested_agents,
                    dummy_location=melt_dummy_location,
                )
                # filter by main_location
                melt_location_affiliated_agents = self._get_affiliated_agents(
                    agents=melt_location_affiliated_agents,
                    dummy_location=dummy_location,
                )

                # get all values for which seperated groups/locations should be created
                melt_split_values = self._get_split_values(
                    agents=melt_location_affiliated_agents,
                    dummy_location=melt_dummy_location,
                    allow_nesting=False,
                )

                for agent in melt_location_affiliated_agents:
                    agent._TEMP_melt_location_weight = melt_dummy_location.weight(agent)

                # for each split value: get groups and collect them in one list for all values
                location_groups_to_melt: list[list] = []
                for melt_split_value in melt_split_values:
                    melt_split_value_affiliated_agents = self._get_split_value_affiliated_agents(
                        agents=melt_location_affiliated_agents,
                        split_value=melt_split_value,
                    )
                    location_groups_to_melt.extend(
                        self._get_groups(
                            agents=melt_split_value_affiliated_agents,
                            location_cls=melt_location_cls,
                        ),
                    )

                groups_to_melt_by_location.append(location_groups_to_melt)

            # Melt groups
            all_melted_groups: list[list] = []
            z = sorted(
                [len(groups_to_melt) for groups_to_melt in groups_to_melt_by_location],
                reverse=True if dummy_location.recycle else False,
            )[0]
            for i in range(z):
                melted_group = []
                for groups_to_melt in groups_to_melt_by_location:
                    if len(groups_to_melt) > 0:
                        if dummy_location.recycle:
                            melted_group.extend(groups_to_melt[i % len(groups_to_melt)])
                        else:
                            try:
                                melted_group.extend(groups_to_melt[i])
                            except IndexError:
                                pass

                all_melted_groups.append(melted_group)

        return all_melted_groups

    def create_locations(
        self,
        location_classes: list,
        agents: list | p2n.AgentList | None = None,
    ) -> p2n.LocationList:
        """Creates location instances and connects them with the given agent population.

        Args:
            location_classes (list): A list of location classes.
            agents (list | p2n.AgentList): A list of agents.

        Returns:
            p2n.LocationList: A list of locations.
        """
        if agents is None:
            agents = self.model.agents

        # self._dummy_model = p2n.Model()
        self._dummy_model.add_agents(agents)

        for location_cls in location_classes:
            dummy_location = self._create_dummy_location(location_cls)
            str_location_cls = dummy_location.type
            for agent in agents:
                setattr(agent, str_location_cls, None)
                setattr(agent, str_location_cls + "_assigned", False)
                setattr(agent, str_location_cls + "_id", None)
                setattr(agent, str_location_cls + "_position", None)
                setattr(agent, str_location_cls + "_head", None)
                setattr(agent, str_location_cls + "_tail", None)

        locations = []

        # for each location class
        for location_cls in location_classes:
            for agent in agents:
                agent._TEMP_melt_location_weight = None

            # create location dummy in order to use the location's methods
            dummy_location = self._create_dummy_location(location_cls)

            str_location_cls = dummy_location.type

            # If nxgraph is used do some checks
            if dummy_location.nxgraph is not None:
                if dummy_location.n_agents is not None:
                    msg = """You cannot define location.n_agents if location.nxgraph is used. 
                        It will be set to the number of nodes in location.nxgraph automatically."""
                    warnings.warn(msg)
                location_cls.n_agents = len(list(dummy_location.nxgraph.nodes))
                dummy_location.n_agents = len(list(dummy_location.nxgraph.nodes))

                if dummy_location.overcrowding is True:
                    msg = """You cannot define location.overcrowding if location.nxgraph is used. 
                        It will be set to `False` automatically."""
                    warnings.warn(msg)
                location_cls.overcrowding = False
                dummy_location.n_agents = False

            # if dummy_location.n_agents is not None and dummy_location.n_agents < 1:
            #    msg = (
            #        f"""{str_location_cls}.n_agents must be `None` or an integer greater than 0."""
            #    )
            #    raise Exception(msg)

            # bridge
            if not dummy_location.melt():
                bridge_values = {
                    dummy_location.bridge(agent)
                    for agent in agents
                    if dummy_location.bridge(agent) is not None
                }

                if len(bridge_values) == 0:
                    pass

                elif len(bridge_values) == 1:
                    msg = f"""{str_location_cls}.bridge() returned only one unique value.
                    {str_location_cls}.bridge() must return at least two unique values in order 
                    to create locations that bring together agents with different values on the 
                    same attribute.
                    """
                    warnings.warn(msg)

                elif len(bridge_values) > 1:
                    if dummy_location.n_agents is not None:
                        msg = f"""You cannot use {str_location_cls}.n_agents and 
                        {str_location_cls}.bridge() at the same time. {str_location_cls}.n_agents
                        is ignored."""
                        warnings.warn(msg)

                    melt_list = []

                    # create one MeltLocation for each bridge_value
                    for bridge_value in bridge_values:

                        def filter(self, agent):
                            return dummy_location.bridge(agent) == self.bridge_value

                        dummy_melt_class = type(
                            f"dummy_meltlocation{str(bridge_value)}",
                            (p2n.MeltLocation,),
                            {
                                "filter": filter,
                                "n_agents": 1,
                                "bridge_value": bridge_value,
                            },
                        )

                        melt_list.append(dummy_melt_class)

                    # set the created MeltLocations as return values of melt()
                    def melt(self):
                        return melt_list

                    location_cls.melt = melt
                    dummy_location = self._create_dummy_location(location_cls)

            if not dummy_location.melt():
                # get all agents that could be assigned to locations of this class
                affiliated_agents = self._get_affiliated_agents(
                    agents=agents,
                    dummy_location=dummy_location,
                )

            else:
                affiliated_agents = []

                for melt_location_cls in dummy_location.melt():
                    melt_dummy_location = self._create_dummy_location(melt_location_cls)
                    affiliated_agents.extend(
                        self._get_affiliated_agents(
                            agents=agents,
                            dummy_location=melt_dummy_location,
                        ),
                    )

            # get all values that are used to split the agents into groups
            split_values = self._get_split_values(
                agents=affiliated_agents,
                dummy_location=dummy_location,
                allow_nesting=True,
            )

            if len(split_values) == 0:
                split_values.append("dummy_split_value")

            group_count = 0

            # for each group split value
            for split_value in split_values:
                split_value_locations = []

                # get all agents with that value
                split_value_affiliated_agents = self._get_split_value_affiliated_agents(
                    agents=affiliated_agents,
                    split_value=split_value,
                )

                # if this location does not glue together other locations
                if not dummy_location.melt():
                    group_lists: list[list] = self._get_groups(
                        agents=split_value_affiliated_agents,
                        location_cls=location_cls,
                    )
                else:
                    group_lists = self._get_melted_groups(
                        agents=split_value_affiliated_agents,
                        location_cls=location_cls,
                    )

                # for each group of agents
                for i, group_list in enumerate(group_lists):
                    group_count += 1

                    dummy_location = self._create_dummy_location(location_cls)
                    dummy_location.agents_ = group_list
                    # dummy_location.add_agents(agents)

                    # dummy_location.group_agents = group_list

                    # get all subgroub values
                    subsplit_values = {
                        agent_subsplit_value
                        for agent in group_list
                        for agent_subsplit_value in utils._to_list(
                            dummy_location._subsplit(agent),
                        )
                    }

                    # for each group of agents assigned to a specific sublocation
                    for j, subsplit_value in enumerate(subsplit_values):
                        # get all subsplit affiliated agents
                        subsplit_affiliated_agents = []

                        # for agent in group_affiliated_agents:
                        for agent in group_list:
                            agent_subsplit_value = utils._to_list(
                                dummy_location._subsplit(agent),
                            )
                            if subsplit_value in agent_subsplit_value:
                                subsplit_affiliated_agents.append(agent)

                        # Build the final location
                        location = location_cls(model=self.model)
                        location.setup()
                        location.split_value = split_value
                        location.subsplit_value = subsplit_value
                        location.group_id = i
                        location.subgroup_id = j

                        split_value_locations.append(location)

                        # Assigning process:
                        for agent in subsplit_affiliated_agents:
                            location.add_agent(agent)

                            weight = (
                                agent._TEMP_melt_location_weight
                                if agent._TEMP_melt_location_weight is not None
                                else location.weight(agent)
                            )

                            location.set_weight(
                                agent=agent,
                                weight=weight,
                            )

                            group_info_str = f"gv={location.split_value},gid={location.group_id}"
                            setattr(agent, str_location_cls, group_info_str)
                            setattr(agent, str_location_cls + "_assigned", True)
                            setattr(agent, str_location_cls + "_id", group_count - 1)
                            setattr(agent, str_location_cls + "_position", group_list.index(agent))
                            setattr(
                                agent,
                                str_location_cls + "_head",
                                True if group_list.index(agent) == 0 else False,
                            )
                            setattr(
                                agent,
                                str_location_cls + "_tail",
                                True if group_list.index(agent) == (len(group_list) - 1) else False,
                            )

                        locations.append(location)

                if (
                    dummy_location.n_locations is not None
                    and not dummy_location.only_exact_n_agents
                ):
                    if len(split_value_locations) < dummy_location.n_locations:
                        for _ in range(
                            int(dummy_location.n_locations - len(split_value_locations))
                        ):
                            location = location_cls(model=self.model)
                            location.setup()
                            location.split_value = split_value
                            location.subsplit_value = None
                            location.group_id = None
                            location.subgroup_id = None

                            locations.append(location)

        locations = p2n.LocationList(model=self.model, objs=locations)

        # execute an action after all locations have been created
        for location in locations:
            location.refine()

        # delete temporary agent attributes
        for agent in self._dummy_model.agents:
            if hasattr(agent, "_TEMP_split_values"):
                del agent._TEMP_split_values

            if hasattr(agent, "_TEMP_melt_location_weight"):
                del agent._TEMP_melt_location_weight

            # for location_class in location_classes:
            #    if hasattr(agent, utils._get_cls_as_str(location_class)):
            #        delattr(agent, utils._get_cls_as_str(location_class))

        # delete temporary location attributes
        # for location in locations:
        #    del location.group_agents

        return locations

    def create(
        self,
        df: pd.DataFrame,
        location_classes: list,
        agent_class: type[p2n.Agent] = p2n.Agent,
        agent_class_attr: None | str = None,
        agent_class_dict: None | dict = None,
        n_agents: int | None = None,
        sample_level: str | None = None,
        sample_weight: str | None = None,
        replace_sample_level_column: bool = True,
    ) -> tuple:
        """Creates agents and locations based on a given dataset.

        Combines the Creator-methods `draw_sample()`, `create_agents()` and `create_locations()`.

        Args:
            df (pd.DataFrame): A data set with individual data that forms the basis for
                the creation of agents. Each row is (potentially) translated into one agent.
                Each column is translated into one agent attribute.
            agent_class (type[p2n.Agent]): The class from which the agent instances are created.
            location_classes (list): A list of classes from which the location instances are
                created.
            n_agents (Optional[int], optional): The number of agents that will be created.
                If `n_agents` is set to None, each row of `df` is translated into exactly one agent.
                Otherwise, rows are randomly drawn (with replacement,
                if `n_agents > len(df)`) from `df` until the number of agents created
                equals `n_agents`.
            sample_level (Optional[str], optional): If `sample_level` is None,
                the rows are sampled individually.
                Otherwise the rows are sampled as groups. `sample_level` defines
                which column of `df` contains the group id.
            sample_weight (Optional[str]): The column of df in which should be used as probability
                weight during sampling.
            replace_sample_level_column (bool): Should the original values of the sample level be
                overwritten by unique values after sampling to avoid duplicates?

        Returns:
            tuple: A list of agents and a list of locations.
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
        agents = self.create_agents(
            df=df_sample,
            agent_class=agent_class,
            agent_class_attr=agent_class_attr,
            agent_class_dict=agent_class_dict,
        )

        # create locations
        locations = self.create_locations(agents=agents, location_classes=location_classes)

        return agents, locations

    def get_df_agents(
        self,
        columns: None | list[str] = None,
        drop_agentpy_columns: bool = True,
    ) -> pd.DataFrame:
        """Returns the latest created population of agents as a dataframe.

        Args:
            columns (list | None): A list of column names that sould be kept.
                All other columns are deleted.
            drop_agentpy_columns (bool): Deletes some columns created by AgentPy.

        Raises:
            Pop2netException: _description_

        Returns:
            pd.DataFrame: A dataframe which contains one row for each
            agent and one column for each agent attribute.
        """
        if self.agents is None:
            msg = "There are no agents."
            raise Pop2netException(msg)

        df = pd.DataFrame([vars(agent) for agent in self.agents])

        if drop_agentpy_columns:
            df = df.drop(
                columns=[
                    "_var_ignore",
                    "id",
                    "type",
                    "log",
                    "model",
                    "p",
                ],
            )

        if columns is not None:
            df = df.loc[:, columns]

        return df
