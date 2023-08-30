"""Base class to create Location objects."""
from typing import Optional

from agentpy.objects import Object
from agentpy.sequences import AgentList

class Location(Object):
    """Base class for location objects."""

    def __init__(self, model) -> None:
        """Location constructor.

        Args:
            model (Model): Model this Location should be associated with.
        """
        super().__init__(model)
        self.model = model

        self.subtype: object = None
        self.size: Optional[int] = None
        self.static_weight: bool = False
        self.weight_projection_function: str = "average"
        self.weight_projection_denominator: float = 1

        self.model.env.add_location(self)

    def setup(self) -> None:
        """~ User interface ~ Use this to set attributes, for instance.

        This method is called automatically by the population maker after creating an instance.
        """

    def add_agent(self, agent) -> None:
        """Add the given agent to the graph.

        Args:
            agent (Agent): The agent that should be added to the location.
        """
        if not self.join(agent):
            return
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
            int: Number of agents.
        """
        return len(self.agents)

    def remove_agent(self, agent) -> None:
        """Removes the given agent from the graph.

        Args:
            agent (Agent): Agent that is to be removed.
        """
        self.model.env.remove_agent_from_location(self, agent)

    def neighbors(self, agent) -> AgentList:
        """Returns a list of agents which are connected to the given agent via this location.

        Args:
            agent (Agent): Agent of whom the neighbors at this location are to be returned.

        Returns:
            AgentList: A list of all agents at this location except the passed agent.
        """
        agents = self.model.env.agents_of_location(self)
        agents.remove(agent)
        return agents

    def join(self, agent) -> bool:  # noqa: ARG002
        """~ User interface ~ Check whether the agent is meant to join this type of location.

        This is a boilerplate implementation of this method which always returns True; i.e. all
        agents will always be allowed at this location. Override this method in your own
        implementations as you seem fit.

        Args:
            agent (Agent): Agent that should be checked.

        Returns:
            bool: True if the agent is allowed to join the location, False otherwise.
        """
        # TODO: This method name makes little sense. "join" implies that the agent is added to the
        # location once the check passes?
        return True

    def group(self, agent) -> object:  # noqa: ARG002
        """~ User interface ~ Allow to create subtypes of this type of location.

        Allows to create subtypes of this type of location if the location instances are created by
        the population maker.

        For each unique value of the given agent attribute one subtype of this
        location type will be created.

        Args:
            agent (Agent): Agent of which the agent attribute will be used for subtype creation

        Returns:
            object: _description_
        """
        # TODO: No clue what this return value is supposed to be..
        return None

    def is_affiliated(self, agent) -> bool:
        """Check if the given agent is connected to this location.

        Args:
            agent (Agent): Agent to be checked.

        Returns:
            True if agent is affiliated with location, False otherwise
        """
        return agent.id in self.model.env.agents_of_location(self)

    def weight(self, agent) -> float:  # noqa: ARG002
        """~ User interface ~ Define the edge weight.

        Defines how the edge weight between an agent and the location is determined.
        This is a boilerplate implementation of this method which always returns 1; i.e. all
        edge weights will be 1. Override this method in your own implementations as you seem fit.

        Args:
            agent (Agent): Agent for which the weight should be determined

        Returns:
            The edge weight.
        """
        return 1

    def update_weight(self, agent) -> None:
        """Create or update the agent-speific weight.

        Args:
            agent (Agent): The agent to be updated.
        """
        self.model.env.g[agent.id][self.id]["weight"] = self.weight(agent)

    def update_weights(self) -> None:
        """Update the weight of every agent on this location."""
        for agent in self.agents:
            self.update_weight(agent)

    def get_weight(self, agent) -> float:
        """Return the edge weight between an agent and the location.

        Args:
            agent (Agent): Agent of which the edge weight should be returned.

        Returns:
            Edge weight.
        """
        return self.model.env.g[agent.id][self.id]["weight"]

    def contact_weight(self, agent1, agent2) -> float:
        """~ User interface ~ Defines how the weights between two agent are combined.

        Defines how the weights are combined when the edge weight between two agents is determined.
        Can be completely rewritten to have location-specific methods of this kind with the same
        name or can be used as it is in the simulation code.

        Args:
            agent1 (Agent): First agent of the pair.
            agent2 (Agent): Second agent of the pair.

        Raises:
            Exception: Raised if `self.weight_projection_function` is not in ["average", "simultan"]

        Returns:
            Combined edge weight.
        """
        # TODO: use custom exception
        # TODO: Exception should be raised in __init__ not here... or passed as parameter.
        if self.weight_projection_function == "average":
            return self.contact_weight_average(agent1, agent2)

        elif self.weight_projection_function == "simultan":
            return self.contact_weight_simultan(agent1, agent2)

        else:
            msg = (
                "There is no method to combine the weights which is called "
                f"{self.weight_projection_function}."
            )
            raise Exception(
                msg,
            )

    def contact_weight_average(self, agent1, agent2) -> float:
        """Determine the average amount of time the two agents are at the location simultaneously.

        Args:
            agent1 (Agent): First agent of the pair.
            agent2 (Agent): Second agent of the pair.

        Returns:
            Average time.
        """
        return (self.get_weight(agent1) * self.get_weight(agent2)) / (
            self.weight_projection_denominator * self.weight_projection_denominator
        )

    def contact_weight_simultan(self, agent1, agent2) -> float:
        """Determine max time two agents could be at this location.

        Determine the maximum amount of time which the two agents could be at this location at
        the same time.

        Args:
            agent1 (Agent): First agent of the pair.
            agent2 (Agent): Second agent of the pair.

        Returns:
            Max time.
        """
        return (
            min(self.get_weight(agent1), self.get_weight(agent2))
            / self.weight_projection_denominator
        )
