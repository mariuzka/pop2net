"""Create a population for the simulation."""

from __future__ import annotations

import itertools
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
        self._dummy_model = p2n.Model(parameters=self.model.p)
        self._temp_agent_attrs = ["_P2NTEMP_split_values", "_P2NTEMP_melt_location_weight"]

    def _create_dummy_location(self, designer) -> p2n.Location:
        lc = designer.location_class
        cls = type(
            "Location" if lc is None else utils._get_cls_as_str(designer.location_class),
            (designer,) if lc is None else (designer, designer.location_class),
            {},  # TODO: warum funktioniert das hier nicht?: {"label": designer.label},
        )
        location = cls(model=self._dummy_model)
        location.label = (
            designer.label if designer.label is not None else utils._get_cls_as_str(designer)
        )
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
        clear: bool = False,
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
            clear (bool): Should the agents already included in the model be removed?

        Returns:
            A list of agents.
        """
        if clear:
            self.model.remove_agents(self.model.agents)

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
        temp_filter_attr = "_P2NTEMP_filter_" + dummy_location.label

        affiliated_agents = []
        for agent in agents:
            if not hasattr(agent, temp_filter_attr):
                setattr(agent, temp_filter_attr, dummy_location.filter(agent))
                self._temp_agent_attrs.append(temp_filter_attr)

            if getattr(agent, temp_filter_attr):
                affiliated_agents.append(agent)

        return affiliated_agents

    def _get_mother_group_id(self, agent, dummy_location) -> str:
        if dummy_location.nest() is None:
            return "None"

        else:
            # search for mother location assigned to this agent
            n_mother_locations_found = 0
            for location in agent.locations:
                if location.label == dummy_location.nest():
                    mother_location = location
                    n_mother_locations_found += 1

            # Check if the number of mother locations is not 1
            if n_mother_locations_found > 1 and self.model.enable_p2n_warnings:
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
                    temp_attr = f"_P2NTEMP_{dummy_location.label}_mother_group_id"
                    setattr(agent, temp_attr, mother_group_id)
                    self._temp_agent_attrs.append(temp_attr)

            # Temporarely store group values as agent attribute
            # to assign them to the corresponding location group later
            agent._P2NTEMP_split_values = agent_values

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

    def _get_groups(self, agents, designer) -> list[list]:
        overcrowding_i = 0

        dummy_location = self._create_dummy_location(designer)

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
            designer.n_agents = max(
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

        # dummy_location = self._create_dummy_location(designer)

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
                    dummy_location = self._create_dummy_location(designer)
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
            agent for agent in agents if split_value in agent._P2NTEMP_split_values
        ]

        return group_affiliated_agents

    def _get_melted_groups(self, agents: list, designer) -> list[list]:
        dummy_location = self._create_dummy_location(designer)

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
            for melt_designer in dummy_location.melt():
                # create dummy location
                melt_dummy_location = self._create_dummy_location(melt_designer)
                if melt_designer.n_locations is None:
                    melt_designer.n_locations = designer.n_locations

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
                    agent._P2NTEMP_melt_location_weight = melt_dummy_location.weight(agent)

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
                            designer=melt_designer,
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

    def _create_designer_mutations(self, location_designers: list) -> list:
        # for each location designer class
        for designer in location_designers:
            # create a dummy location to use the location's methods
            dummy_location = self._create_dummy_location(designer)

            # if the user defined mutations
            if dummy_location.mutate() is not None:
                mutations = []

                # create all possible combinations of the mutation values
                # {key: [1, 2, 3], key2: [4, 5]} -> [{key: 1, key2: 4}, {key: 1, key2: 5}, ...]
                combinations = [
                    dict(zip(dummy_location.mutate().keys(), values))
                    for values in itertools.product(*dummy_location.mutate().values())
                ]

                # create a new location designer class for each combination
                for i, combo in enumerate(combinations):
                    mutation = type(
                        dummy_location.type,
                        (designer,),
                        {
                            **combo,
                            "label": f"{dummy_location.label}{i}",
                        },
                    )
                    mutations.append(mutation)

                # store the mutations in the designer class
                designer._P2NTEMP_mutations = mutations

        # replace the original location designer classes with the mutations
        location_designers_with_mutations = []
        for location_designer in location_designers:
            if hasattr(location_designer, "_P2NTEMP_mutations"):
                location_designers_with_mutations.extend(location_designer._P2NTEMP_mutations)
            else:
                location_designers_with_mutations.append(location_designer)

        return location_designers_with_mutations

    def create_locations(
        self,
        location_designers: list,
        agents: list | p2n.AgentList | None = None,
        clear: bool = False,
        delete_magic_agent_attributes: bool = True,
    ) -> p2n.LocationList:
        """Creates location instances and connects them with the given agent population.

        Args:
            location_designers (list): A list of LocationDesigner classes.
            agents (list | p2n.AgentList): A list of agents.
            clear (bool): Should the locations already included in the model be removed?
            delete_magic_location_attributes (bool): If True, all magic location attributes will be
                removed after the creation of the location instances.
            delete_magic_agent_attribtues (book): If True, all magic agent attributes will be
                removed after the creation of the location instances.

        Returns:
            p2n.LocationList: A list of locations.
        """
        # Create designer mutations
        location_designers = self._create_designer_mutations(location_designers)

        # Check if all location classes have a unique label
        labels = []
        for designer in location_designers:
            dummy_location = self._create_dummy_location(designer)
            if dummy_location.label is None:
                msg = (
                    f"LocationDesigner class {designer} has no label. Please define a unique label."
                )
                raise Pop2netException(msg)
            elif dummy_location.label in labels:
                msg = f"""LocationDesigner class {designer} has a duplicate label. 
                    Please define a unique label."""
                raise Pop2netException(msg)
            else:
                labels.append(dummy_location.label)

        # Remove all locations if clear is True
        if clear:
            self.model.remove_locations(self.model.locations)

        # Use the existing agents in the model if no agents are given if agents is None:
        if agents is None:
            agents = self.model.agents

        # Create a list containing the names of all special location attributes
        # to delete those attributes later
        magic_agent_attributes = []

        # Add the agents to the dummy model
        self._dummy_model.add_agents(agents)

        # Create magic agent attributes for each location designer class
        for designer in location_designers:
            dummy_location = self._create_dummy_location(designer)
            label = dummy_location.label
            for agent in agents:
                setattr(agent, label, None)
                magic_agent_attributes.append(label)

                setattr(agent, label + "_assigned", False)
                magic_agent_attributes.append(label + "_assigned")

                setattr(agent, label + "_id", None)
                magic_agent_attributes.append(label + "_id")

                setattr(agent, label + "_position", None)
                magic_agent_attributes.append(label + "_position")

                setattr(agent, label + "_head", None)
                magic_agent_attributes.append(label + "_head")

                setattr(agent, label + "_tail", None)
                magic_agent_attributes.append(label + "_tail")

        # The list of all created location instances
        locations = []

        # For each designer: start of creation procedure
        for designer in location_designers:
            # Set temporary location weight of MeltLocations to None
            for agent in agents:
                agent._P2NTEMP_melt_location_weight = None

            # create location dummy in order to use the location's methods
            dummy_location = self._create_dummy_location(designer)
            label = dummy_location.label

            # If nxgraph is used do some checks
            if dummy_location.nxgraph is not None:
                if dummy_location.n_agents is not None and self.model.enable_p2n_warnings:
                    msg = """You cannot define location.n_agents if location.nxgraph is used. 
                        It will be set to the number of nodes in location.nxgraph automatically."""
                    warnings.warn(msg)
                designer.n_agents = len(list(dummy_location.nxgraph.nodes))
                dummy_location.n_agents = len(list(dummy_location.nxgraph.nodes))

                if dummy_location.overcrowding is True and self.model.enable_p2n_warnings:
                    msg = """You cannot define location.overcrowding if location.nxgraph is used. 
                        It will be set to `False` automatically."""
                    warnings.warn(msg)
                designer.overcrowding = False
                dummy_location.overcrowding = False

            # check if n_locations and split is used at the same time
            if (
                not all(dummy_location.split(agent) is None for agent in agents)
                and dummy_location.n_locations is not None
            ):
                msg = f"""You cannot use {label}.n_locations and {label}.split() at the same time.
                {label}.n_locations is ignored and set to None."""
                warnings.warn(msg)
                designer.n_locations = None
                dummy_location.n_locations = None

            # bridge
            if not dummy_location.melt():
                bridge_values = {
                    dummy_location.bridge(agent)
                    for agent in self._get_affiliated_agents(
                        agents=agents, dummy_location=dummy_location
                    )
                    if dummy_location.bridge(agent) is not None
                }

                if len(bridge_values) == 0:
                    pass

                elif len(bridge_values) == 1 and self.model.enable_p2n_warnings:
                    msg = f"""{dummy_location.label}.bridge() returned only one unique value.
                    {dummy_location.label}.bridge() must return at least two unique values in order 
                    to create locations that bring together agents with different values on the 
                    same attribute.
                    """
                    warnings.warn(msg)

                elif len(bridge_values) > 1 and self.model.enable_p2n_warnings:
                    if dummy_location.n_agents is not None:
                        msg = f"""You cannot use {label}.n_agents and 
                        {label}.bridge() at the same time. {label}.n_agents
                        is ignored."""
                        warnings.warn(msg)

                    melt_list = []

                    # create one MeltLocation for each bridge_value
                    for bridge_value in bridge_values:

                        def filter(self, agent):
                            return dummy_location.bridge(agent) == self.bridge_value

                        dummy_melt_class = type(
                            f"dummy_meltlocation{str(bridge_value)}",
                            (p2n.MeltLocationDesigner,),
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

                    designer.melt = melt
                    dummy_location = self._create_dummy_location(designer)

            if not dummy_location.melt():
                # get all agents that could be assigned to locations of this class
                affiliated_agents = self._get_affiliated_agents(
                    agents=agents,
                    dummy_location=dummy_location,
                )

            else:
                affiliated_agents = []

                for melt_designer in dummy_location.melt():
                    melt_dummy_location = self._create_dummy_location(melt_designer)
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
                        designer=designer,
                    )
                else:
                    group_lists = self._get_melted_groups(
                        agents=split_value_affiliated_agents,
                        designer=designer,
                    )

                # for each group of agents
                for i, group_list in enumerate(group_lists):
                    group_count += 1

                    dummy_location = self._create_dummy_location(designer)
                    dummy_location.agents_ = group_list

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

                        # inspect the defined magic location class get all methods/attributes
                        # that are not part of magic location class
                        keep_attrs = {}
                        for attr in dir(designer):
                            if attr not in p2n.LocationDesigner.__dict__:
                                keep_attrs[attr] = getattr(designer, attr)

                        # Build the final location
                        if designer.location_class is None:
                            location = type(
                                "Location",
                                (p2n.Location,),
                                keep_attrs,
                            )(model=self.model)

                        else:
                            location = type(
                                utils._get_cls_as_str(designer.location_class),
                                (designer.location_class,),
                                keep_attrs,
                            )(model=self.model)

                        location.label = (
                            designer.label
                            if designer.label is not None
                            else utils._get_cls_as_str(designer)
                        )
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
                                agent._P2NTEMP_melt_location_weight
                                if agent._P2NTEMP_melt_location_weight is not None
                                else location.weight(agent)
                            )

                            location.set_weight(
                                agent=agent,
                                weight=weight,
                            )

                            group_info_str = f"gv={location.split_value},gid={location.group_id}"
                            setattr(agent, label, group_info_str)
                            setattr(agent, label + "_assigned", True)
                            setattr(agent, label + "_id", group_count - 1)
                            setattr(agent, label + "_position", group_list.index(agent))
                            setattr(
                                agent,
                                label + "_head",
                                True if group_list.index(agent) == 0 else False,
                            )
                            setattr(
                                agent,
                                label + "_tail",
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
                            location = designer(model=self.model)
                            location.setup()
                            location.split_value = split_value
                            location.subsplit_value = None
                            location.group_id = None
                            location.subgroup_id = None

                            locations.append(location)

        locations = p2n.LocationList(model=self.model, objs=locations)

        # delete temporary agent attributes
        for agent in self._dummy_model.agents:
            for attr in self._temp_agent_attrs:
                if hasattr(agent, attr):
                    delattr(agent, attr)

        magic_agent_attributes = set(magic_agent_attributes)
        if delete_magic_agent_attributes:
            for attr in magic_agent_attributes:
                for agent in agents:
                    delattr(agent, attr)

        return locations

    def create(
        self,
        df: pd.DataFrame,
        location_designers: list,
        agent_class: type[p2n.Agent] = p2n.Agent,
        agent_class_attr: None | str = None,
        agent_class_dict: None | dict = None,
        n_agents: int | None = None,
        sample_level: str | None = None,
        sample_weight: str | None = None,
        replace_sample_level_column: bool = True,
        clear: bool = False,
        delete_magic_agent_attributes: bool = True,
    ) -> tuple:
        """Creates agents and locations based on a given dataset.

        Combines the Creator-methods `draw_sample()`, `create_agents()` and `create_locations()`.

        Args:
            df (pd.DataFrame): A data set with individual data that forms the basis for
                the creation of agents. Each row is (potentially) translated into one agent.
                Each column is translated into one agent attribute.
            agent_class (type[p2n.Agent]): The class from which the agent instances are created.
            location_designers (list): A list of classes from which the location instances are
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
            clear (bool): Should the agents and locations already included in the model be removed?
            delete_magic_location_attributes (bool): If True, all magic location attributes will be
                removed after the creation of the location instances.
            delete_magic_agent_attributes (bool): If True, all magic agent attributes will be
                removed after the creation of the location instances.

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
            clear=clear,
        )

        # create locations
        locations = self.create_locations(
            agents=agents,
            location_designers=location_designers,
            clear=clear,
            delete_magic_agent_attributes=delete_magic_agent_attributes,
        )

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
