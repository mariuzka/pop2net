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
    """Creates and connects actors and locations."""

    def __init__(
        self,
        env: p2n.Environment,
        seed: int = None,
    ) -> None:
        """Instantiate a creator for a specific model.

        Args:
            seed (int, optional): A seed for reproducibility. Defaults to 999.
        """
        self.env = env
        self.seed = seed
        self.rng = random.Random(seed)
        self._temp_actor_attrs = ["_P2NTEMP_split_values", "_P2NTEMP_melt_location_weight"]
        self.model = self.env.model

    def _create_dummy_location(self, designer) -> p2n.Location:
        # TODO: Organize this code better

        if self.env.framework is None:
            if designer.location_class is None:
                # case 1: no framework & default location class
                dummy_location_class = type("Location", (designer,), {})
            else:
                # case 2: no framework & custom location class
                location_name = utils._get_cls_as_str(designer.location_class)
                dummy_location_class = type(location_name, (designer, designer.location_class), {})

            dummy_location = dummy_location_class()
            dummy_location.model = (
                self.model
            )  # if no model was passed to the env, this is just None

        else:
            if designer.location_class is None:
                # case 3: framework & default location class
                dummy_location_class = type("Location", (designer, self.env._framework.Agent), {})
            else:
                # case 4: framework & custom location class
                location_name = utils._get_cls_as_str(designer.location_class)
                dummy_location_class = type(location_name, (designer, designer.location_class), {})
            dummy_location = dummy_location_class(model=self.model)

        dummy_location.label = (
            designer.label if designer.label is not None else utils._get_cls_as_str(designer)
        )
        dummy_location.setup()
        return dummy_location

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

    def create_actors(
        self,
        actor_class=None,
        actor_class_attr: None | str = None,
        actor_class_dict: None | dict = None,
        df: pd.DataFrame | None = None,
        n: int | None = None,
        clear: bool = False,
    ):
        """Creates actors from a pandas DataFrame.

        Creates one actor-instance of the given actor-class for each row of the given df,
        if df is not None.
        All columns of the df are added as instance attributes containing the row-specific values
        of the specific column.
        If df is None and n is not None, n default actors without any additional attributes are
        created.

        Args:
            actor_class: A class to instantiate all actors with. Every column in the DataFrame will
                result in an attribute of the actors.
            df: The DataFrame from which the actors should be created from.
            n: The number of actors that should be created. Defaults to None.
            clear (bool): Should the actors already included in the model be removed?

        Returns:
            A list of actors.
        """
        if clear:
            self.env.remove_actors(self.env.actors)

        # if no actor class was provided
        if actor_class is None:
            # if no framework ist used, use default actor class
            if self.env.framework is None:
                actor_class = p2n.Actor

            # if a framework is used, create mixed actor class
            else:

                class MixedActor(p2n.Actor, self.env._framework.Agent):
                    pass

                actor_class = MixedActor

        if df is not None:
            df = df.copy()

            # create one actor for each row in df
            actors = []
            for _, row in df.iterrows():
                if actor_class_dict is None:
                    if self.env.framework is None:
                        actor = actor_class()
                        actor.model = (
                            self.model
                        )  # if no model was passed to the env, this is just None
                    else:
                        actor = actor_class(model=self.model)
                else:
                    actor = actor_class_dict[row[actor_class_attr]](model=self.model)

                for col_name in df.columns:
                    if col_name == "id":
                        msg = "You are not allowed to set an actor attribute called `id`."
                        raise Exception(msg)
                    else:
                        setattr(actor, col_name, row[col_name])
                actors.append(actor)

        else:
            if n is not None:
                if self.model is None:
                    actors = [actor_class() for _ in range(n)]
                else:
                    actors = [actor_class(model=self.model) for _ in range(n)]

            else:
                msg = "Either `df` or `n` must be not None."
                raise Exception(msg)

        # add actors to environment
        self.env.add_actors(actors)

        return self.env._to_framework(actors)

    def _get_affiliated_actors(self, actors, dummy_location) -> list:
        temp_filter_attr = "_P2NTEMP_filter_" + dummy_location.label
        self._temp_actor_attrs.append(temp_filter_attr)

        affiliated_actors = []
        for actor in actors:
            if not hasattr(actor, temp_filter_attr):
                setattr(actor, temp_filter_attr, dummy_location.filter(actor))
                self._temp_actor_attrs.append(temp_filter_attr)

            if getattr(actor, temp_filter_attr):
                affiliated_actors.append(actor)

        return affiliated_actors

    def _get_mother_group_id(self, actor, dummy_location) -> str:
        if dummy_location.nest() is None:
            return "None"

        else:
            # search for mother location assigned to this actor
            n_mother_locations_found = 0
            for location in actor.locations:
                if location.label == dummy_location.nest():
                    mother_location = location
                    n_mother_locations_found += 1

            # Check if the number of mother locations is not 1
            if n_mother_locations_found > 1 and self.env.enable_p2n_warnings:
                warnings.warn(
                    f"""For actor {actor},
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
        actors: list,
        dummy_location,
        allow_nesting: bool = False,
    ) -> list[int | str]:
        all_values = []
        for actor in actors:
            actor_values = utils._to_list(dummy_location.split(actor))

            if allow_nesting:
                # Add mother location's value to the value of the lower level location
                for i, value in enumerate(actor_values):
                    mother_group_id = self._get_mother_group_id(actor, dummy_location)
                    actor_values[i] = "-".join([mother_group_id, str(value)])
                    temp_attr = f"_P2NTEMP_{dummy_location.label}_mother_group_id"
                    setattr(actor, temp_attr, mother_group_id)
                    self._temp_actor_attrs.append(temp_attr)

            # Temporarely store group values as actor attribute
            # to assign them to the corresponding location group later
            actor._P2NTEMP_split_values = actor_values

            for value in actor_values:
                if value not in all_values:
                    all_values.append(value)

        return all_values

    def _get_stick_value(self, actor, dummy_location):
        stick_value = dummy_location.stick_together(actor)
        if stick_value is None:
            return "None" + str(actor.id_p2n)
        else:
            return stick_value

    def _get_groups(self, actors, designer) -> list[list]:
        overcrowding_i = 0

        dummy_location = self._create_dummy_location(designer)

        n_location_groups_is_fixed = False

        # determine the number of groups needed
        if dummy_location.n_locations is None and dummy_location.n_actors is None:
            n_location_groups = 1
            groups: list[list] = [[]]

        elif dummy_location.n_locations is None and dummy_location.n_actors is not None:
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
                round_function(len(actors) / dummy_location.n_actors),
                1,
            )
            groups: list[list] = [[]]

        elif dummy_location.n_locations is not None and dummy_location.n_actors is None:
            n_location_groups = dummy_location.n_locations
            designer._P2NTEMP_ori_n_actors = dummy_location.n_actors
            designer.n_actors = max(
                math.floor(len(actors) / n_location_groups),
                1,
            )

            groups: list[list] = [[] for _ in range(n_location_groups)]

        elif dummy_location.n_locations is not None and dummy_location.n_actors is not None:
            n_location_groups = dummy_location.n_locations
            n_location_groups_is_fixed = True
            groups: list[list] = [[]]

        else:
            # TODO:
            raise Exception

        stick_values = {self._get_stick_value(actor, dummy_location) for actor in actors}

        # dummy_location = self._create_dummy_location(designer)

        # for each group of sticky actors
        for stick_value in stick_values:
            sticky_actors = [
                actor
                for actor in actors
                if self._get_stick_value(actor, dummy_location) == stick_value
            ]

            assigned = False

            for _, group in enumerate(groups):
                # if there are still enough free places available
                if (dummy_location.n_actors is None) or dummy_location.n_actors - len(group) >= len(
                    sticky_actors
                ):
                    # if sum(
                    #    [dummy_location.find(actor) for actor in sticky_actors],
                    # ) == len(sticky_actors):
                    #    # assign actors
                    for actor in sticky_actors:
                        group.append(actor)
                        # dummy_location.add_actor(actor)

                    assigned = True
                    break

            if not assigned:
                if len(groups) < n_location_groups:
                    new_group = []
                    dummy_location = self._create_dummy_location(designer)
                    # assign actors
                    for actor in sticky_actors:
                        new_group.append(actor)
                        # dummy_location.add_actor(actor)

                    groups.append(new_group)

                else:
                    if not dummy_location.only_exact_n_actors and not n_location_groups_is_fixed:
                        for actor in sticky_actors:
                            groups[overcrowding_i].append(actor)
                        overcrowding_i = (overcrowding_i + 1) % len(groups)

        if dummy_location.only_exact_n_actors:
            groups = [group for group in groups if len(group) == dummy_location.n_actors]

        return groups

    def _get_split_value_affiliated_actors(
        self,
        actors: list,
        split_value: int | str,
    ) -> list:
        group_affiliated_actors = [
            actor for actor in actors if split_value in actor._P2NTEMP_split_values
        ]

        return group_affiliated_actors

    def _get_melted_groups(self, actors: list, designer) -> list[list]:
        dummy_location = self._create_dummy_location(designer)

        # get all mother locations the actors are nested in
        all_mother_group_ids = {
            self._get_mother_group_id(actor, dummy_location) for actor in actors
        }

        # for each mother location
        for mother_group_id in all_mother_group_ids:
            # get actors that are part of this location
            nested_actors = [
                actor
                for actor in actors
                if self._get_mother_group_id(actor, dummy_location) == mother_group_id
            ]

            # a list that stores a list of groups for each location
            # [
            # [[_actor], [_actor], [_actor]], # groups of location 1
            # [[_actor], [_actor]],           # groups of location 2
            # ]
            groups_to_melt_by_location: list[list[list]] = []

            # for each location that shall be melted
            for melt_designer in dummy_location.melt():
                # create dummy location
                melt_dummy_location = self._create_dummy_location(melt_designer)
                if melt_designer.n_locations is None:
                    melt_designer.n_locations = designer.n_locations

                # get all actors that should be assigned to this location
                # filter by melt_location
                melt_location_affiliated_actors = self._get_affiliated_actors(
                    actors=nested_actors,
                    dummy_location=melt_dummy_location,
                )
                # filter by main_location
                melt_location_affiliated_actors = self._get_affiliated_actors(
                    actors=melt_location_affiliated_actors,
                    dummy_location=dummy_location,
                )

                # get all values for which separated groups/locations should be created
                melt_split_values = self._get_split_values(
                    actors=melt_location_affiliated_actors,
                    dummy_location=melt_dummy_location,
                    allow_nesting=False,
                )

                for actor in melt_location_affiliated_actors:
                    actor._P2NTEMP_melt_location_weight = melt_dummy_location.weight(actor)
                    self._temp_actor_attrs.append("_P2NTEMP_melt_location_weight")

                # for each split value: get groups and collect them in one list for all values
                location_groups_to_melt: list[list] = []
                for melt_split_value in melt_split_values:
                    melt_split_value_affiliated_actors = self._get_split_value_affiliated_actors(
                        actors=melt_location_affiliated_actors,
                        split_value=melt_split_value,
                    )
                    location_groups_to_melt.extend(
                        self._get_groups(
                            actors=melt_split_value_affiliated_actors,
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
        actors: list | p2n.ActorList | None = None,
        clear: bool = False,
        delete_magic_actor_attributes: bool = True,
    ) -> p2n.LocationList:
        """Creates location instances and connects them with the given actor population.

        Args:
            location_designers (list): A list of LocationDesigner classes.
            actors (list | p2n.ActorList): A list of actors.
            clear (bool): Should the locations already included in the model be removed?
            delete_magic_location_attributes (bool): If True, all magic location attributes will be
                removed after the creation of the location instances.
            delete_magic_actor_attribtues (book): If True, all magic actor attributes will be
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
            self.env.remove_locations(self.env.locations)

        # Use the existing actors in the model if no actors are given if actors is None:
        if actors is None:
            actors = self.env.actors

        # Create a list containing the names of all special location attributes
        # to delete those attributes later
        magic_actor_attributes = []

        # Create magic actor attributes for each location designer class
        for designer in location_designers:
            dummy_location = self._create_dummy_location(designer)
            label = dummy_location.label
            for actor in actors:
                setattr(actor, label, None)
                magic_actor_attributes.append(label)

                setattr(actor, label + "_assigned", False)
                magic_actor_attributes.append(label + "_assigned")

                setattr(actor, label + "_id", None)
                magic_actor_attributes.append(label + "_id")

                setattr(actor, label + "_position", None)
                magic_actor_attributes.append(label + "_position")

                setattr(actor, label + "_head", None)
                magic_actor_attributes.append(label + "_head")

                setattr(actor, label + "_tail", None)
                magic_actor_attributes.append(label + "_tail")

        # The list of all created location instances
        locations = []

        # For each designer: start of creation procedure
        for designer in location_designers:
            # Set temporary location weight of MeltLocations to None
            for actor in actors:
                actor._P2NTEMP_melt_location_weight = None

            # create location dummy in order to use the location's methods
            dummy_location = self._create_dummy_location(designer)
            label = dummy_location.label

            # If nxgraph is used do some checks
            if dummy_location.nxgraph is not None:
                if dummy_location.n_actors is not None and self.env.enable_p2n_warnings:
                    msg = """You cannot define location.n_actors if location.nxgraph is used. 
                        It will be set to the number of nodes in location.nxgraph automatically."""
                    warnings.warn(msg)
                designer.n_actors = len(list(dummy_location.nxgraph.nodes))
                dummy_location.n_actors = len(list(dummy_location.nxgraph.nodes))

                if dummy_location.overcrowding is True and self.env.enable_p2n_warnings:
                    msg = """You cannot define location.overcrowding if location.nxgraph is used. 
                        It will be set to `False` automatically."""
                    warnings.warn(msg)
                designer.overcrowding = False
                dummy_location.overcrowding = False

            # check if n_locations and split is used at the same time
            if (
                not all(dummy_location.split(actor) is None for actor in actors)
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
                    dummy_location.bridge(actor)
                    for actor in self._get_affiliated_actors(
                        actors=actors, dummy_location=dummy_location
                    )
                    if dummy_location.bridge(actor) is not None
                }

                if len(bridge_values) == 0:
                    pass

                elif len(bridge_values) == 1 and self.env.enable_p2n_warnings:
                    msg = f"""{dummy_location.label}.bridge() returned only one unique value.
                    {dummy_location.label}.bridge() must return at least two unique values in order 
                    to create locations that bring together actors with different values on the 
                    same attribute.
                    """
                    warnings.warn(msg)

                elif len(bridge_values) > 1 and self.env.enable_p2n_warnings:
                    if dummy_location.n_actors is not None:
                        msg = f"""You cannot use {label}.n_actors and 
                        {label}.bridge() at the same time. {label}.n_actors
                        is ignored."""
                        warnings.warn(msg)

                    melt_list = []

                    # create one MeltLocation for each bridge_value
                    for bridge_value in bridge_values:

                        def filter(self, actor):
                            return dummy_location.bridge(actor) == self.bridge_value

                        dummy_melt_class = type(
                            f"dummy_meltlocation{str(bridge_value)}",
                            (p2n.MeltLocationDesigner,),
                            {
                                "filter": filter,
                                "n_actors": 1,
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
                # get all actors that could be assigned to locations of this class
                affiliated_actors = self._get_affiliated_actors(
                    actors=actors,
                    dummy_location=dummy_location,
                )

            else:
                affiliated_actors = []

                for melt_designer in dummy_location.melt():
                    melt_dummy_location = self._create_dummy_location(melt_designer)
                    affiliated_actors.extend(
                        self._get_affiliated_actors(
                            actors=actors,
                            dummy_location=melt_dummy_location,
                        ),
                    )

            # get all values that are used to split the actors into groups
            split_values = self._get_split_values(
                actors=affiliated_actors,
                dummy_location=dummy_location,
                allow_nesting=True,
            )

            if len(split_values) == 0:
                split_values.append("dummy_split_value")

            group_count = 0

            # for each group split value
            for split_value in split_values:
                split_value_locations = []

                # get all actors with that value
                split_value_affiliated_actors = self._get_split_value_affiliated_actors(
                    actors=affiliated_actors,
                    split_value=split_value,
                )

                # if this location does not glue together other locations
                if not dummy_location.melt():
                    group_lists: list[list] = self._get_groups(
                        actors=split_value_affiliated_actors,
                        designer=designer,
                    )
                else:
                    group_lists = self._get_melted_groups(
                        actors=split_value_affiliated_actors,
                        designer=designer,
                    )

                # for each group of actors
                for i, group_list in enumerate(group_lists):
                    group_count += 1

                    dummy_location = self._create_dummy_location(designer)
                    dummy_location.actors_ = group_list

                    # get all subgroub values
                    subsplit_values = {
                        actor_subsplit_value
                        for actor in group_list
                        for actor_subsplit_value in utils._to_list(
                            dummy_location._subsplit(actor),
                        )
                    }

                    # for each group of actors assigned to a specific sublocation
                    for j, subsplit_value in enumerate(subsplit_values):
                        # get all subsplit affiliated actors
                        subsplit_affiliated_actors = []

                        # for actor in group_affiliated_actors:
                        for actor in group_list:
                            actor_subsplit_value = utils._to_list(
                                dummy_location._subsplit(actor),
                            )
                            if subsplit_value in actor_subsplit_value:
                                subsplit_affiliated_actors.append(actor)

                        # inspect the defined magic location class get all methods/attributes
                        # that are not part of magic location class
                        keep_attrs = {}
                        for attr in dir(designer):
                            if attr not in p2n.LocationDesigner.__dict__:
                                keep_attrs[attr] = getattr(designer, attr)

                        # Create the final location class
                        if designer.location_class is None:
                            if self.env.framework is None:
                                location_class = type(
                                    "Location",
                                    (p2n.Location,),
                                    keep_attrs,
                                )

                            else:
                                location_class = type(
                                    "Location",
                                    (
                                        p2n.Location,
                                        self.env._framework.Agent,
                                    ),  # inherit from framework.Actor
                                    keep_attrs,
                                )

                        else:
                            location_class = type(
                                utils._get_cls_as_str(designer.location_class),
                                (designer.location_class,),
                                keep_attrs,
                            )

                        # Create the final location instance
                        if self.env.framework is None:
                            location = location_class()
                        else:
                            location = location_class(model=self.env.model)

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

                        self.env.add_location(location=location)

                        split_value_locations.append(location)

                        # Assigning process:
                        # The if-statement below is just a quick fix to handle .n_actors == 0.
                        # TODO: Fix this earlier in the code
                        if dummy_location.n_actors is None or dummy_location.n_actors > 0:
                            for actor in subsplit_affiliated_actors:
                                location.add_actor(actor)

                                weight = (
                                    actor._P2NTEMP_melt_location_weight
                                    if actor._P2NTEMP_melt_location_weight is not None
                                    else location.weight(actor)
                                )

                                location.set_weight(
                                    actor=actor,
                                    weight=weight,
                                )

                                group_info_str = (
                                    f"gv={location.split_value},gid={location.group_id}"
                                )
                                setattr(actor, label, group_info_str)
                                setattr(actor, label + "_assigned", True)
                                setattr(actor, label + "_id", group_count - 1)
                                setattr(actor, label + "_position", group_list.index(actor))
                                setattr(
                                    actor,
                                    label + "_head",
                                    True if group_list.index(actor) == 0 else False,
                                )
                                setattr(
                                    actor,
                                    label + "_tail",
                                    True
                                    if group_list.index(actor) == (len(group_list) - 1)
                                    else False,
                                )

                            locations.append(location)

                if (
                    dummy_location.n_locations is not None
                    and not dummy_location.only_exact_n_actors
                ):
                    if len(split_value_locations) < dummy_location.n_locations:
                        for _ in range(
                            int(dummy_location.n_locations - len(split_value_locations))
                        ):
                            location = designer()
                            location.setup()
                            location.split_value = split_value
                            location.subsplit_value = None
                            location.group_id = None
                            location.subgroup_id = None

                            self.env.add_location(location=location)
                            locations.append(location)

        # Reset location_designer.n_actors if it was changed
        for designer in location_designers:
            if hasattr(designer, "_P2NTEMP_ori_n_actors"):
                designer.n_actors = designer._P2NTEMP_ori_n_actors
                delattr(designer, "_P2NTEMP_ori_n_actors")

        # delete temporary actor attributes
        for actor in actors:
            for attr in self._temp_actor_attrs:
                if hasattr(actor, attr):
                    delattr(actor, attr)

        magic_actor_attributes = set(magic_actor_attributes)
        if delete_magic_actor_attributes:
            for attr in magic_actor_attributes:
                for actor in actors:
                    delattr(actor, attr)

        return self.env._to_framework(locations)

    def create(
        self,
        df: pd.DataFrame,
        location_designers: list,
        actor_class: type[p2n.Actor] = p2n.Actor,
        actor_class_attr: None | str = None,
        actor_class_dict: None | dict = None,
        n_actors: int | None = None,
        sample_level: str | None = None,
        sample_weight: str | None = None,
        replace_sample_level_column: bool = True,
        clear: bool = False,
        delete_magic_actor_attributes: bool = True,
    ) -> tuple:
        """Creates actors and locations based on a given dataset.

        Combines the Creator-methods `draw_sample()`, `create_actors()` and `create_locations()`.

        Args:
            df (pd.DataFrame): A data set with individual data that forms the basis for
                the creation of actors. Each row is (potentially) translated into one actor.
                Each column is translated into one actor attribute.
            actor_class (type[p2n.Actor]): The class from which the actor instances are created.
            location_designers (list): A list of classes from which the location instances are
                created.
            n_actors (Optional[int], optional): The number of actors that will be created.
                If `n_actors` is set to None, each row of `df` is translated into exactly one actor.
                Otherwise, rows are randomly drawn (with replacement,
                if `n_actors > len(df)`) from `df` until the number of actors created
                equals `n_actors`.
            sample_level (Optional[str], optional): If `sample_level` is None,
                the rows are sampled individually.
                Otherwise the rows are sampled as groups. `sample_level` defines
                which column of `df` contains the group id.
            sample_weight (Optional[str]): The column of df in which should be used as probability
                weight during sampling.
            replace_sample_level_column (bool): Should the original values of the sample level be
                overwritten by unique values after sampling to avoid duplicates?
            clear (bool): Should the actors and locations already included in the model be removed?
            delete_magic_location_attributes (bool): If True, all magic location attributes will be
                removed after the creation of the location instances.
            delete_magic_actor_attributes (bool): If True, all magic actor attributes will be
                removed after the creation of the location instances.

        Returns:
            tuple: A list of actors and a list of locations.
        """
        # draw a sample from dataset
        df_sample = self.draw_sample(
            df=df,
            n=n_actors,
            sample_level=sample_level,
            sample_weight=sample_weight,
            replace_sample_level_column=replace_sample_level_column,
        )

        # create actors
        actors = self.create_actors(
            df=df_sample,
            actor_class=actor_class,
            actor_class_attr=actor_class_attr,
            actor_class_dict=actor_class_dict,
            clear=clear,
        )

        # create locations
        locations = self.create_locations(
            actors=actors,
            location_designers=location_designers,
            clear=clear,
            delete_magic_actor_attributes=delete_magic_actor_attributes,
        )

        return actors, locations

    def get_df_actors(
        self,
        columns: None | list[str] = None,
        drop_agentpy_columns: bool = True,
    ) -> pd.DataFrame:
        """Returns the latest created population of actors as a dataframe.

        Args:
            columns (list | None): A list of column names that sould be kept.
                All other columns are deleted.
            drop_agentpy_columns (bool): Deletes some columns created by agentpy.

        Raises:
            Pop2netException: _description_

        Returns:
            pd.DataFrame: A dataframe which contains one row for each
            actor and one column for each actor attribute.
        """
        if self.actors is None:
            msg = "There are no actors."
            raise Pop2netException(msg)

        df = pd.DataFrame([vars(actor) for actor in self.actors])

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
