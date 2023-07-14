from typing import Dict
from typing import Optional

import networkx as nx
from agentpy.objects import Object
from agentpy.sequences import AgentList


class Location(Object):
    def __init__(self, model) -> None:
        super().__init__(model)
        self.model = model

        self.subtype: object = None
        self.size: Optional[int] = None
        self.static_weight: bool = False
        self.weight_projection_function: str = "average"
        self.weight_projection_denominator: float = 1

        self.model.env.add_location(self)

    def setup(self) -> None:
        """
        ~ User interface ~

        This method is called automatically by the population maker after creating an instance.
        Can be used to set attributes, for instance.
        """
        pass

    def add_agent(self, agent) -> None:
        """
        Adds the given agent to the graph.
        """
        if not self.join(agent):
            return
        self.model.env.add_agent_to_location(self, agent)
        self.update_weight(agent)

    @property
    def agents(self) -> AgentList:
        """
        Returns the list of agents affiliated with this location.
        """
        return self.model.env.agents_of_location(self)

    @property
    def n_affiliated_agents(self) -> int:
        return len(self.agents)

    def remove_agent(self, agent) -> None:
        """
        Removes the given agent from the graph.
        """
        self.model.env.remove_agent_from_location(self, agent)

    def neighbors(self, agent) -> AgentList:
        """
        Returns a list of agents which are connected to the given agent via this location.
        """
        agents = self.model.env.agents_of_location(self)
        agents.remove(agent)
        return agents

    def join(self, agent) -> bool:
        """
        ~ User interface ~

        Checks whether the agent is meant to join this type of location.
        """
        return True

    def group(self, agent) -> object:
        """
        ~ User interface ~

        Allows to create subtypes of this type of location if the location instances are create by the population maker.
        For each unique value of the given agent attribute one subtype of this location type will be created.
        """
        return None

    def is_affiliated(self, agent) -> bool:
        """
        Checks if the given agent is connected to this location.
        """
        return agent.id in self.model.env.agents_of_location(self)

    def weight(self, agent) -> float:
        """
        ~ User interface ~

        Defines how the edge weight between an agent and the location is determined.
        """
        return 1

    def update_weight(self, agent) -> None:
        """
        Creates or updates the agent-speific weight.
        """
        self.model.env.g[agent.id][self.id]["weight"] = self.weight(agent)

    def update_weights(self) -> None:
        """
        Update the weight of every agent on this location.
        """
        for agent in self.agents:
            self.update_weight(agent)

    def get_weight(self, agent) -> float:
        """
        Returns the edge weight between an agent and the location.
        """
        return self.model.env.g[agent.id][self.id]["weight"]

    def contact_weight(
        self,
        agent1,
        agent2,
    ) -> float:
        """
        ~ User interface ~

        Defines how the weights are combined when the edge weight between two agent is determined.
        Can be completely rewritten to have location-specific methods of this kind with the same name or can be used as it is in the simulation code.
        """

        if self.weight_projection_function == "average":
            return self.contact_weight_average(agent1, agent2)

        elif self.weight_projection_function == "simultan":
            return self.contact_weight_simultan(agent1, agent2)

        else:
            raise Exception(
                f"There is no method to combine the weights which is called {self.weight_projection_function}.",
            )

    def contact_weight_average(self, agent1, agent2) -> float:
        """
        Determines the average amount of time the two agents are at the location simultaneously.
        """
        return (self.get_weight(agent1) * self.get_weight(agent2)) / (
            self.weight_projection_denominator * self.weight_projection_denominator
        )

    def contact_weight_simultan(self, agent1, agent2) -> float:
        """
        Determines the maximum amount of time which the two agents could be at this location at the same time.
        """
        return (
            min(self.get_weight(agent1), self.get_weight(agent2))
            / self.weight_projection_denominator
        )
