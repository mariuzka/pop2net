"""Base class to create Location objects."""
from __future__ import annotations

from typing import Any

from agentpy.objects import Object
from agentpy.sequences import AgentList

from . import agent as _agent
from . import model as _model

class Location(Object):
    """Base class for location objects."""

    def __init__(self, model: _model.Model) -> None:
        """Location constructor.

        Args:
            model: Model this Location should be associated with.
        """
        super().__init__(model)
        self.model = model

        self.group_id: int | None = None
        self.subgroup_id: int | None = None
        self.group_value: int | str | None = None
        self.subgroup_value: int | str | None = None
        
        self.size: int | None = None
        self.allow_overcrowding: bool = True
        self.n_locations: int | None = None
        self.static_weight: bool = False
        
        # TODO: maybe delete after the creation of all locations
        self.group_agents = []

        self.model.env.add_location(self)

    def setup(self) -> None:
        """~ User interface ~ Use this to set attributes, for instance.

        This method is called automatically by the population maker after creating an instance.
        """

    def add_agent(self, agent: _agent.Agent) -> None:
        """Add the given agent to the graph.

        Args:
            agent: The agent that should be added to the location.
        """
        self.model.env.add_agent_to_location(self, agent)
        self.update_weight(agent)

    @property
    def agents(self) -> AgentList:
        """Return the list of agents affiliated with this location.

        Returns:
            List of agents at this location.
        """
        return self.model.env.agents_of_location(self)

    @property
    def n_affiliated_agents(self) -> int:
        """Return the number of agents currently at this location.

        Returns:
            Number of agents.
        """
        return len(self.agents)

    def remove_agent(self, agent: _agent.Agent) -> None:
        """Removes the given agent from the graph.

        Args:
            agent: Agent that is to be removed.
        """
        self.model.env.remove_agent_from_location(self, agent)

    def neighbors(self, agent: _agent.Agent) -> AgentList:
        """Returns a list of agents which are connected to the given agent via this location.

        Args:
            agent: Agent of whom the neighbors at this location are to be returned.

        Returns:
            AgentList: A list of all agents at this location except the passed agent.
        """
        agents = self.model.env.agents_of_location(self)
        agents.remove(agent)
        return agents

    def join(self, agent: _agent.Agent) -> bool:  # noqa: ARG002
        """~ User interface ~ Check whether the agent is meant to join this type of location.

        This is a boilerplate implementation of this method which always returns True; i.e. all
        agents will always be allowed at this location. Override this method in your own
        implementations as you seem fit.

        Args:
            agent: Agent that should be checked.

        Returns:
            True if the agent is allowed to join the location, False otherwise.
        """
        # TODO: This method name makes little sense. "join" implies that the agent is added to the
        # location once the check passes?
        # -> What is a better name?
        return True

    # TODO: Rename to split()
    def group(self, agent: _agent.Agent) -> float | str | list | None:  # noqa: ARG002
        """~ User interface ~ Allow to create subtypes of this type of location.

        Allows to create subtypes of this type of location if the location instances are created by
        the population maker.

        For each unique value of the given agent attribute one subtype of this
        location type will be created.

        Args:
            agent: Agent of which the agent attribute will be used for subtype creation

        Returns:
            object: _description_
        """
        return None

    # TODO: Rename to subsplit()
    def subgroup(self, agent: _agent.Agent) -> Any:
        return None

    def is_affiliated(self, agent: _agent.Agent) -> bool:
        """Check if the given agent is connected to this location.

        Args:
            agent: Agent to be checked.

        Returns:
            True if agent is affiliated with location, False otherwise
        """
        return agent.id in self.model.env.agents_of_location(self)

    def weight(self, agent: _agent.Agent) -> float:  # noqa: ARG002
        """~ User interface ~ Define the edge weight.

        Defines how the edge weight between an agent and the location is determined.
        This is a boilerplate implementation of this method which always returns 1; i.e. all
        edge weights will be 1. Override this method in your own implementations as you seem fit.

        Args:
            agent: Agent for which the weight should be determined

        Returns:
            The edge weight.
        """
        return 1

    def update_weight(self, agent: _agent.Agent) -> None:
        """Create or update the agent-speific weight.

        Args:
            agent: The agent to be updated.
        """
        self.model.env.g[agent.id][self.id]["weight"] = self.weight(agent)

    def update_weights(self) -> None:
        """Update the weight of every agent on this location."""
        for agent_ in self.agents:
            self.update_weight(agent_)

    def get_weight(self, agent: _agent.Agent) -> float:
        """Return the edge weight between an agent and the location.

        Args:
            agent: Agent of which the edge weight should be returned.

        Returns:
            Edge weight.
        """
        return self.model.env.g[agent.id][self.id]["weight"]

    def project_weights(self, agent1: _agent.Agent, agent2: _agent.Agent) -> float:
        """~ User interface ~ Defines how the weights between two agent are combined.

        Defines how the weights are combined when the edge weight between two agents is determined.
        Can be completely rewritten to have location-specific methods of this kind with the same
        name or can be used as it is in the simulation code.

        Args:
            agent1: First agent of the pair.
            agent2: Second agent of the pair.

        Raises:
            Exception: Raised if `self.weight_projection_function` is not in ["average", "simultan"]

        Returns:
            Combined edge weight.
        """
        return (self.get_weight(agent1) + self.get_weight(agent2)) / 2


    def stick_together(self, agent: _agent.Agent) -> Any:
        """Sticks agents together by attribute.

        Args:
            agent (_agent.Agent): _description_

        Returns:
            Any: _description_
        """
        return agent.id
    
    # TODO: rename this method
    def do_this_after_creation(self):
        pass

    def nest(self):
        return None