from __future__ import annotations

import networkx as nx

from pop2net.location import Location
import pop2net.utils as utils

from . import agent as _agent
from . import model as _model


class LocationDesigner(Location):
    """Helper class to create locations from inside the Creator."""

    label: str | None = None
    location_class: type | None = None
    location_name: str | None = None

    n_agents: int | None = None
    overcrowding: bool = None
    only_exact_n_agents: bool = False
    n_locations: int | None = None
    static_weight: bool = False
    recycle: bool = True
    nxgraph: nx.Graph | None = None

    def __init__(self, model: _model.Model) -> None:
        """Create a helper class to create locations.

        Args:
            model (_model.Model):  The model.
        """
        super().__init__(model)
        self.group_id: int | None = None
        self.subgroup_id: int | None = None
        self.group_value: int | str | None = None
        self.subgroup_value: int | str | None = None

    def setup(self) -> None:
        """Use this method to set instance attributes, for instance.

        This method is called automatically by the creator after creating an instance.
        """

    def filter(self, agent: _agent.Agent) -> bool:  # noqa: ARG002
        """Check whether the agent is meant to join this type of location.

        This is a boilerplate implementation of this method which always returns True; i.e. all
        agents will always be allowed at this location. Override this method in your own
        implementations as you seem fit.

        Args:
            agent: The agent that is currently processed by the Creator.

        Returns:
            True if the agent is allowed to join the location, False otherwise.
        """
        return True

    def bridge(self, agent: _agent.Agent) -> float | str | list | None:  # noqa: ARG002
        """Create locations with one agent for each unique value returned.

        Cannot be used in combination with melt().

        Args:
            agent (_agent.Agent): The agent that is currently processed by the Creator.

        Returns:
            float | str | list | None:
                The value which is used to assign agents to location instances.
        """
        return None

    def split(self, agent: _agent.Agent) -> float | str | list | None:  # noqa: ARG002
        """Creates seperate location instances for each unique returned value.

        Args:
            agent: The agent that is currently processed by the Creator.

        Returns:
            float | str | list | None:
                The value(s) that determine(s) to which location instance the agent is assigned.
        """
        return None

    def stick_together(self, agent: _agent.Agent) -> float | str:
        """Assigns agents with a shared value on an attribute to the same location instance.

        Args:
            agent (_agent.Agent): The agent that is currently processed by the Creator.

        Returns:
            float | str: A value that defines the groups of agents.
        """
        return agent.id

    def nest(self) -> type[Location] | None:
        """Nests this location class into another location class.

        Ensures that the agents assigned to the same instance of this location class
        are also assigned to the same instance of the returned location class.

        Returns:
           type[Location] | None: The location class in which this location class should be nested.
        """
        return None

    def melt(self) -> list[Location] | tuple[Location]:
        """Allows to assign agents with different attribute values to the same location.

        Merges the agents assigned to the instances of the returned location classes
        into one instance of this location class.

        Returns:
            None | list | tuple: A list or tuple of location classes.
        """
        return []

    def refine(self):
        """An action that is performed after all location instances have been created."""
        pass

    def _subsplit(self, agent: _agent.Agent) -> str | float | list | None:  # noqa: ARG002
        """Splits a location instance into sub-instances to create a certain network structure.

        Args:
            agent (_agent.Agent): The agent that is currently processed by the Creator.

        Returns:
            str | float | None: A value or a list of values that represent specific sub-instances.
        """
        if self.nxgraph is None:
            return None
        else:
            node_indices = list(self.nxgraph.nodes)
            agent_pos = self.agents_.index(agent)

            if agent_pos <= len(node_indices) - 1:
                node_index = node_indices[agent_pos]

                return [
                    utils._join_positions(pos1=node_index, pos2=neighbor)
                    for neighbor in self.nxgraph.neighbors(node_index)
                ]

            else:
                return None

    def mutate(self) -> None | dict[str:list]:
        """Creates new versions of this location designer with different attributes.

        Returns:
            dict: A dictionary that specifies the values for each mutation.
        """
        return None


class MeltLocationDesigner(Location):
    """Helper class to melt locations."""

    label: str | None = None

    location_class: type | None = None
    location_name: str | None = None
    n_agents: int | None = None
    overcrowding: bool | None = None
    only_exact_n_agents: bool = False
    n_locations: int | None = None

    def filter(self, agent: _agent.Agent) -> bool:  # noqa: ARG002
        """Check whether the agent is meant to join this type of location.

        This is a boilerplate implementation of this method which always returns True; i.e. all
        agents will always be allowed at this location. Override this method in your own
        implementations as you seem fit.

        Args:
            agent: The agent that is currently processed by the Creator.

        Returns:
            True if the agent is allowed to join the location, False otherwise.
        """
        return True

    def stick_together(self, agent: _agent.Agent) -> float | str:
        """Assigns agents with a shared value on an attribute to the same location instance.

        Args:
            agent (_agent.Agent): The agent that is currently processed by the Creator.

        Returns:
            float | str: A value that defines the groups of agents.
        """
        return agent.id

    def split(self, agent: _agent.Agent) -> float | str | list | None:  # noqa: ARG002
        """Creates seperate location instances for each unique returned value.

        Args:
            agent: The agent that is currently processed by the Creator.

        Returns:
            float | str | list | None: The value(s) that determine(s) to which location instance
                the agent is assigned.
        """
        return None

    def weight(self, agent: _agent.Agent) -> float | None:  # noqa: ARG002
        """Defines the edge weight between the agent and the location instance.

        Defines how the edge weight between an agent and the location is determined.
        This is a boilerplate implementation of this method which always returns 1; i.e. all
        edge weights will be 1. Override this method in your own implementations as you seem fit.

        Args:
            agent: The agent that is currently processed by the Creator.

        Returns:
            The edge weight.
        """
        return None
