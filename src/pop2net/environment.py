"""The environment class. It encapsulates the full simulation."""

from __future__ import annotations

import itertools
import typing
import warnings

import networkx as nx

if typing.TYPE_CHECKING:
    from . import actor as _actor
    from . import location as _location

import pop2net as p2n


class Environment:
    """Class that organizes actors and locations."""

    def __init__(self, model=None, framework: str | None = None, enable_p2n_warnings=True):
        """Initialize a new environment.

        Args:
            model (agentpy.Model | mesa.Model, optional): A simulation model. Defaults to None.
            framework (str | None, optional): The ABM-framework you you want to use.
                Options are: "agentpy" & "mesa". Defaults to None.
            enable_p2n_warnings (bool, optional): Should pop2net warnings be shown? Defaults to True.

        Raises:
            ValueError: _description_
        """
        # settings
        self.framework: str | None = framework
        self._framework = None
        self.enable_p2n_warnings = enable_p2n_warnings

        # import framework dependencies, if required
        if self.framework is None:
            pass
        elif self.framework == "agentpy":
            import agentpy

            self._framework = agentpy
        elif self.framework == "mesa":
            import mesa

            self._framework = mesa
        else:
            raise ValueError(f"Invalid framework selected: {self.framework}")

        # connected objects
        self.model = model
        self.g = nx.Graph()

        # TODO: should we add creator and inspector as attributes?
        # self.creator = Creator(env=self)
        # self.inspector = NetworkInspector(env=self)

        # a unique id that is added to the objects of this environment
        self._fresh_id = 0

    def _attach_fresh_id(self, obj):
        obj.id_p2n = self._fresh_id
        self._fresh_id += 1

    def _to_framework(self, objects):
        if self.framework is None:
            return objects
        elif self.framework == "agentpy":
            return self._framework.AgentList(model=self.model, objs=objects)
        elif self.framework == "mesa":
            return self._framework.agent.AgentSet(agents=objects, random=self.model.random)
        else:
            raise ValueError("Invalid framework.")

    @property
    def actors(self) -> list:
        """Show a iterable view of all actors in the environment.

        Important: While you can make changes to the objects in this list, you
        cannot modify this attribute itself. Instead you have to use methods like
        Environment.add_actor() or Environment.remove_actor(), for instance.

        Returns:
            list: A non-mutable list of all actors in the environment.
        """
        return self._to_framework(
            [data["_obj"] for _, data in self.g.nodes(data=True) if data["bipartite"] == 0]
        )

    @property
    def locations(self) -> list:
        """Show a iterable view of all locations in the environment.

        Important: While you can make changes to the objects in this list, you
        cannot modify this attribute itself. Instead you have to use methods like
        Environment.add_location() or Environment.remove_location(), for instance.

        Returns:
            LocationList: a non-mutable LocationList of all locations in the environment.
        """
        return self._to_framework(
            [data["_obj"] for _, data in self.g.nodes(data=True) if data["bipartite"] == 1]
        )

    # TODO: def add_obj as a common parent method for add_actor & add_location
    def add_actor(self, actor: _actor.Actor) -> None:
        """Add an actor to the environment.

        The added actor will have no connections to other actors or locatons by default.
        If the actor is already in the current environment, this methods does nothing.

        Args:
            actor: Actor to be added to the environment.
        """
        if actor.id_p2n is None:
            self._attach_fresh_id(actor)

        if not self.g.has_node(actor.id_p2n):
            self.g.add_node(actor.id_p2n, bipartite=0, _obj=actor)
            actor.env = self

    def add_actors(self, actors: list) -> None:
        """Add actors to the environment.

        Args:
            actors (list): A list of the actors to be added.
        """
        for actor in actors:
            self.add_actor(actor)

    def add_location(self, location: _location.Location) -> None:
        """Add a location to the environment.

        The added location will have no connections to other actors or locatons by default.
        If the location is already in the current environment, this methods does nothing.

        Args:
            location: Location to be added to the environment.
        """
        if location.id_p2n is None:
            self._attach_fresh_id(location)

        if not self.g.has_node(location.id_p2n):
            self.g.add_node(location.id_p2n, bipartite=1, _obj=location)
            location.env = self

    def add_locations(self, locations: list) -> None:
        """Add multiple locations to the environment at once.

        Args:
            locations (list): An iterable over multiple locations.
        """
        for location in locations:
            self.add_location(location)

    def add_actor_to_location(
        self,
        location: _location.Location,
        actor: _actor.Actor,
        weight: float | None = None,
        **kwargs,
    ) -> None:
        """Add an actor to a specific location.

        Both the actor and the location have to be defined beforehand. All additional keyword
        arguments will be edge attributes for this connection.

        Args:
            location: Location the actor is to be added to.
            actor: Actor to be added to the location.
            weight: An optional weight for the connection.
            **kwargs: Additional edge attributes.

        Raises:
            Exception: Raised if the location does not exist in the environment.
            Exception: Raised if the actor does not exist in the environment.
        """
        # TODO: Create custom exceptions
        if not self.g.has_node(location.id_p2n):
            msg = f"Location {location} does not exist in Environment!"
            raise Exception(msg)
        if not self.g.has_node(actor.id_p2n):
            msg = f"Actor {actor} does not exist in Environment!"
            raise Exception(msg)

        self.g.add_edge(actor.id_p2n, location.id_p2n, **kwargs)
        self.set_weight(actor=actor, location=location, weight=weight)

    def remove_actor(self, actor: _actor.Actor) -> None:
        """Remove an actor from the environment.

        If the actor does not exist in the environment, this method does nothing.

        Args:
            actor: Actor to be removed.
        """
        if self.g.has_node(actor.id_p2n):
            self.g.remove_node(actor.id_p2n)

    def remove_actors(self, actors: list[_actor.Actor]) -> None:
        """Remove multiple actors from the environment at once.

        Args:
            actors (list): An iterable over multiple actors.
        """
        for actor in actors:
            self.remove_actor(actor)

    def remove_location(self, location: _location.Location) -> None:
        """Remove a location from the environment.

        If the location does not exist in the environment, this method does nothing.

        Args:
            location: Location to be removed.
        """
        if self.g.has_node(location.id_p2n):
            self.g.remove_node(location.id_p2n)

    def remove_locations(self, locations: list[_location.Location]) -> None:
        """Remove multiple locations at once.

        Args:
            locations (list): An iterable over locations.
        """
        for location in locations:
            self.remove_location(location)

    def remove_actor_from_location(
        self,
        location: _location.Location,
        actor: _actor.Actor,
    ) -> None:
        """Remove an actor from a location.

        Args:
            location: Location, the actor is to be removed from.
            actor: Actor to be disassociated with the location.

        Raises:
            Exception: Raised if the location does not exist in the environment.
            Exception: Raised if the actor does not exist in the environment.
        """
        # TODO: use custom exceptions
        if not self.g.has_node(location.id_p2n):
            msg = f"Location {location} does not exist in Environment!"
            raise Exception(msg)
        if not self.g.has_node(actor.id_p2n):
            msg = f"Actor {actor} does not exist in Environment!"
            raise Exception(msg)

        if self.g.has_edge(actor.id_p2n, location.id_p2n):
            self.g.remove_edge(actor.id_p2n, location.id_p2n)

    def actors_of_location(self, location: _location.Location):
        """Return the list of actors associated with a specific location.

        Args:
            location: The desired location.

        Returns:
            A list of actors.
        """
        nodes = self.g.neighbors(location.id_p2n)
        actors = [
            self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 0
        ]
        return self._to_framework(actors)

    def locations_of_actor(self, actor: _actor.Actor) -> list[_location.Location]:
        """Return the list of locations associated with a specific actor.

        Args:
            actor: The desired actor.

        Returns:
            A list of locations.
        """
        nodes = self.g.neighbors(actor.id_p2n)
        locations = [
            self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 1
        ]
        return self._to_framework(locations)

    def neighbors_of_actor(
        self,
        actor: _actor.Actor,
        location_labels: list | None = None,
    ) -> list[_actor.Actor]:
        """Return a list of neighboring actors for a specific actor.

        The locations to be considered can be defined with location_labels.

        Args:
            actor: Actor of whom the neighbors are to be returned.
            location_labels: A list of location_labels.

        Returns:
            The list of neighbors for the specified actor.
        """
        if location_labels:
            locations = (
                node
                for node in self.g.neighbors(actor.id_p2n)
                if self.g.nodes[node]["bipartite"] == 1
                and self.g.nodes[node]["_obj"].label in location_labels
            )
        else:
            locations = (
                node
                for node in self.g.neighbors(actor.id_p2n)
                if self.g.nodes[node]["bipartite"] == 1
            )

        neighbor_actors = {
            actor_id
            for location_id in locations
            for actor_id in self.g.neighbors(location_id)
            if self.g.nodes[actor_id]["bipartite"] == 0
        }

        return self._to_framework(
            [
                self.g.nodes[actor_id]["_obj"]
                for actor_id in neighbor_actors
                if actor_id != actor.id_p2n
            ]
        )

    def _objects_between_objects(self, object1, object2) -> list:
        paths = list(
            nx.all_simple_paths(
                G=self.g,
                source=object1.id_p2n,
                target=object2.id_p2n,
                cutoff=2,
            ),
        )
        return [self.g.nodes[path[1]]["_obj"] for path in paths]

    def locations_between_actors(
        self, actor1, actor2, location_labels: list[str] | None = None
    ) -> list:
        """Return all locations that connects two actors.

        Args:
            actor1 (Actor): Actor 1.
            actor2 (Actor): Actor 2.
            location_labels (tuple, optional): Constrain the locations to the following types.
                Defaults to None.

        Returns:
            LocationList: A list of locations.
        """
        locations = self._objects_between_objects(object1=actor1, object2=actor2)

        if location_labels is not None:
            locations = [location for location in locations if location.label in location_labels]

        return self._to_framework(locations)

    def actors_between_locations(
        self, location1, location2, actor_types: list[str] | None = None
    ) -> list:
        """Return all actors between two locations.

        Args:
            location1 (Location): Location 1.
            location2 (Location): Location 2.
            actor_types (tuple, optional): Constrain the actors to the following types.
                Defaults to None.

        Returns:
            List: A list of actors.
        """
        actors = self._objects_between_objects(location1, location2)

        if actor_types is not None:
            actors = [actor for actor in actors if actor.type in actor_types]

        return self._to_framework(actors)

    def set_weight(self, actor, location, weight: float | None = None) -> None:
        """Set the weight of an actor at a location.

        If weight is None the method location.weight() will be used to generate a weight.

        Args:
            actor (Actor): The actor.
            location (Location): The location.
            weight (int): The weight
        """
        self.g[actor.id_p2n][location.id_p2n]["weight"] = (
            location.weight(actor) if weight is None else weight
        )

    def get_weight(self, actor, location) -> int:
        """Get the weight of an actor at a location.

        Args:
            actor (Actor): The actor.
            location (Location): The location.

        Returns:
            int: The weight.
        """
        return self.g[actor.id_p2n][location.id_p2n]["weight"]

    def connect_actors(self, actors: list, location_cls: type, weight: float | None = None):
        """Connects multiple actors via an instance of a given location class.

        Args:
            actors (list): A list of actors.
            location_cls (type): The location class that is used to create a location instance.
            weight (float | None): The edge weight between the actors and the location.
                Defaults to None.
        """
        if location_cls is None:
            if self.framework is None:
                location_cls = p2n.Location
            else:

                class Location(p2n.Location, self._framework.Agent):
                    pass

                location_cls = Location

        if self.model is None:
            location = location_cls()
        else:
            location = location_cls(model=self.model)

        self.add_location(location=location)
        location.add_actors(actors=actors, weight=weight)

    def disconnect_actors(
        self,
        actors: list,
        location_labels: list | None = None,
        remove_locations: bool = False,
    ):
        """Disconnects actors by removing them from shared locations.

        If a list of location types is given, only shared locations of the given types are
        considered. Turn on `remove_locations` in order to not only remove the given actors from the
        given location instance but also to remove the location instance from the environment.
        Use this method with care because removing actors from locations also disconnects those
        actors from all other actors connected to the location. Removing the location instance from
        the environment could have even more sideeffects to those actors still connected with this
        location!

        Args:
            actors (list): A list of actors.
            location_labels (list | None, optional): A list of location types to specify which
            shared locations are considered. Defaults to None.
            remove_locations (bool, optional): A bool that determines whether the shared locations
                shall be removed from the environment. Defaults to False.
        """
        pairs = list(itertools.combinations(actors, 2))

        shared_locations = []

        for actor1, actor2 in pairs:
            shared_locations.extend(
                self.locations_between_actors(
                    actor1=actor1,
                    actor2=actor2,
                    location_labels=location_labels,
                )
            )

        shared_locations = set(shared_locations)

        for location in shared_locations:
            warn = False
            for actor in location.actors:
                if actor not in actors:
                    warn = True
                    break

            if warn and self.enable_p2n_warnings:
                msg = "There are other actors at the location from which you have removed actors."
                warnings.warn(msg)

            location.remove_actors(actors)

            if remove_locations:
                self.remove_location(location=location)

                if warn and self.enable_p2n_warnings:
                    msg = "You have removed a location to which other actors were still connected."
                    warnings.warn(msg)

    def export_bipartite_network(
        self,
        actor_attrs: list | None = None,
        location_attrs: list | None = None,
    ) -> nx.graph:
        graph = self.g.copy()

        for i in graph:
            if graph.nodes[i]["bipartite"] == 0:
                if actor_attrs is not None:
                    for actor_attr in actor_attrs:
                        graph.nodes[i][actor_attr] = getattr(graph.nodes[i]["_obj"], actor_attr)

            elif graph.nodes[i]["bipartite"] == 1:
                if location_attrs is not None:
                    for location_attr in location_attrs:
                        graph.nodes[i][location_attr] = getattr(
                            graph.nodes[i]["_obj"], location_attr
                        )

            del graph.nodes[i]["_obj"]
        return graph

    def export_actor_network(
        self,
        node_attrs: list | None = None,
        include_0_weights: bool = True,
    ) -> nx.Graph:
        """Creates a projection of the environment's bipartite network.

        Args:
            node_attrs: A list of actor attributes
            include_0_weights: Should edges with weight 0 be displayed?

        Returns:
            A weighted graph created from a environment's actor list. Actors are connected if they are
            neighbors in the environment. Their connecting edge include the contact_weight as "weight"
            attribute.
        """
        graph = nx.Graph()

        # create nodes
        for actor in self.actors:
            if not graph.has_node(actor.id_p2n):
                node_attr_dict = (
                    {node_attr: vars(actor)[node_attr] for node_attr in node_attrs}
                    if node_attrs is not None
                    else {}
                )
                graph.add_node(actor.id_p2n, **node_attr_dict)

        # create edges
        for actor in self.actors:
            for actor_v in actor.neighbors():
                if not graph.has_edge(actor.id_p2n, actor_v.id_p2n):
                    weight = actor.get_actor_weight(actor_v)
                    if include_0_weights or weight > 0:
                        graph.add_edge(actor.id_p2n, actor_v.id_p2n, weight=weight)

        return graph

    def update_weights(self, location_labels: list | None = None) -> None:
        """Updates the edge weights between actors and locations.

        If you only want to update the weights of specific types of locations
        specify those types in location_labels.

        Args:
            location_labels (list | None, optional): A list of location classes that specifiy for
                which location types the weights should be updated.
                If location_labels is None all locations are considered. Defaults to None.
        """
        for location in (
            self.locations
            if location_labels is None
            else [location for location in self.locations if location.label in location_labels]
        ):
            for actor in location.actors:
                location.set_weight(actor=actor, weight=location.weight(actor=actor))
