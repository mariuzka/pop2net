"""Base class to create Actor objects."""

from __future__ import annotations

import typing
import warnings

if typing.TYPE_CHECKING:
    from . import location as _location


class Actor:
    """This is a Base class to represent actors in the simulation.

    Actors' behavior can be implemented in classes that inherit from this.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Actor Constructor."""
        self.env = None
        self.id_p2n = None
        self.model = None
        self.type = type(self).__name__

        super().__init__(*args, **kwargs)

    def neighbors(self, location_labels: list[str] | None = None) -> list:
        """Return all neighbors of an actor.

        Convenience method that returns all neighbors over all locations this actor is currently
        located in. The locations to be considered can be defined with location_labels.

        Args:
            location_labels: A list of location_labels.

        Returns:
            All actors co-located with this actor over all locations.
        """
        return self.env.neighbors_of_actor(self, location_labels=location_labels)

    def shared_locations(self, actor, location_labels: list[str] | None = None) -> list:
        """Returns all locations that this actor shares with another actor.
        Use location_labels to specify which type of locations should be included in the search
        for shared locations.

        Args:
            actor (p2n.Actor): The other actor.
            location_labels (list[str] | None, optional): A list of location_labels. Defaults to None.

        Returns:
            list: Shared locations.
        """
        return self.env.locations_between_actors(
            actor1=self,
            actor2=actor,
            location_labels=location_labels,
        )

    def add_location(self, location: _location.Location, weight: float | None = None) -> None:
        """Add this actor to a given location.
        If weight is None, it will be set to 1.

        Args:
            location: Add actor to this location.
            weight (float | None): The edge weight between the actor and the location.
                Defaults to None.
        """
        self.env.add_actor_to_location(actor=self, location=location, weight=weight)

    def add_locations(self, locations: list, weight: float | None = None) -> None:
        """Add this actor to multiple locations.

        Args:
            locations (list): Add the actor to these locations.
            weight (float | None): The edge weight between the actor and the location.
                Defaults to None.
        """
        for location in locations:
            self.add_location(location=location, weight=weight)

    def remove_location(self, location: _location.Location) -> None:
        """Remove this actor from a given location.

        Args:
            location: Remove actor from this location.
        """
        self.env.remove_actor_from_location(self, location)

    def remove_locations(self, locations: list) -> None:
        """Remove this Actor from the given locations.

        Args:
            locations (list): A list of location instances.
        """
        for location in locations:
            self.remove_location(location)

    @property
    def locations(self) -> list:
        """Returns a list of locations that this actor is associated with.

        Returns:
            A list of locations.
        """
        return self.env.locations_of_actor(self)

    @property
    def location_labels(self) -> list[str]:
        """Returns a list of labels of the locations this actor is associated with.

        Returns:
            list[str]: A list of location labels.
        """
        return [location.label for location in self.locations]

    def get_actor_weight(self, actor: Actor, location_labels: list | None = None) -> float:
        """Returns the edge weight between this actor and a given other actor.

        This is summed over all shared locations.

        Args:
            actor: The other actor.
            location_labels (list): A list of location classes to specify the type of locations
                which are considered.

        Returns:
            A weight of the contact between the two actors.
        """
        weight = 0
        for location in self.shared_locations(actor=actor, location_labels=location_labels):
            weight += location.project_weights(actor1=self, actor2=actor)
        return weight

    def get_location_weight(self, location) -> float:
        """Return the edge weight between this actor and a given location.

        Args:
            location (_type_): A location.

        Returns:
            float: The edge weight.
        """
        return self.env.get_weight(actor=self, location=location)

    def connect(self, actor: Actor, location_cls: _location = None, weight: float | None = None):
        """Connects this actor with a given other actor via an instance of a given location class.
        If location_cls is None, the default pop2net.Location class is used to create a new location
        instance. If weight is None, it will be set to 1.

        Args:
            actor (p2n.Actor): An actor to connect with.
            location_cls (type): The location class that is used to create a location instance.
            weight(float | None): The edge weight between the actors and the location.
                Defaults to None.
        """
        self.env.connect_actors(actors=[self, actor], location_cls=location_cls, weight=weight)

    def disconnect(
        self,
        neighbor: Actor,
        location_labels: list | None = None,
        remove_self=True,
        remove_neighbor=True,
        remove_locations: bool = False,
    ):
        """Disconnects this actor from a given other actor by removing them from shared locations.

        If a list of location types is given, only shared locations of the given types are
        considered. Turn on `remove_locations` in order to not only remove the actors from the
        given location instance but also to remove the location instance from the model.  Keep in
        mind that this may affect other actors that are still connected with the location instance.

        Args:
            neighbor (Actor): An actor to disconnect from.
            location_labels (list | None, optional): A list of location types to specify which
            shared locations are considered. Defaults to None.
            remove_self (bool): Should the actor be removed from the shared locations?
                Defaults to True.
            remove_neighbor (bool): Should the neighbor be removed from the shared locations?
                Defaults to True.
            remove_locations (bool, optional): A bool that determines whether the shared locations
                shall be removed from the model. Defaults to False.
        """
        shared_locations = self.shared_locations(
            actor=neighbor,
            location_labels=location_labels,
        )

        for location in shared_locations:
            warn = False
            for actor in location.actors:
                if actor not in [self, neighbor]:
                    warn = True
                    break

            if remove_self:
                location.remove_actor(self)

                if warn:
                    msg = (
                        "There are other actors at the location from which you have removed actors."
                    )
                    warnings.warn(msg)

            if remove_neighbor:
                location.remove_actor(neighbor)

                if warn:
                    msg = (
                        "There are other actors at the location from which you have removed actors."
                    )
                    warnings.warn(msg)

            if remove_locations:
                self.env.remove_location(location)

                if warn:
                    msg = "You have removed a location to which other actors were still connected."
                    warnings.warn(msg)
