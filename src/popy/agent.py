import agentpy as ap

from .exceptions import PopyException
from .sequences import LocationList


class Agent(ap.Agent):
    """This is a Base class to represent agents in the simulation.

    Agents' behavior can be implemented in classes that inherit from this.

    :param ap: _description_
    :type ap: _type_
    """

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self.model = model
        self.locations = LocationList(model)

    def get_contacts(self, weights: bool = False):
        return ap.AgentList(
            self.model,
            [agent for neighbors in self.locations.neighbors(self) for agent in neighbors],  # type: ignore
        )

    def add_location(self, location) -> None:
        """Assigns a location to this agent.

        Args:
            location (:doc:`location`):  Location that is to be added to the agent.

        Raises:
            PopyException: Raised, if the location is already assigned to this agent.
        """

        if location in self.locations:
            raise PopyException("Location already associated with this Agent!")
        self.locations.append(location)
        location.add_agent(self, visit_weight=1)

    # def visit_locations_ORI(self, model) -> None:
    #    self.locations.visit(self)

    def visit_locations(self):

        time_not_at_home = 0

        for location in self.locations:
            if not location.is_home:
                visit_weight = location.get_visit_weight(self) if location.can_visit(self) else 0
                location.graph.g.nodes[self.id]["visit_weight"] = visit_weight
                location.visit_weights[
                    self.id
                ] = visit_weight  # vielleicht einfach in einem Dict speichern, statt als node-attribute?
                time_not_at_home += visit_weight

        time_at_home = (
            24 - time_not_at_home
        )  # HIER MUSS DIE 24 ANPASSBAR SEIN, DA DIE ZEIT NICHT IMMER IN STUNDEN GEMESSEN WIRD UND AUCH EIN TIMESTEP NICHT IMMER EIN TAG SEIN MUSS

        if time_not_at_home > 24:
            raise PopyException("Unrealistic time not at home.")

        for location in self.locations:
            if location.is_home:
                location.graph.g.nodes[self.id]["visit_weight"] = time_at_home
                location.visit_weights[self.id] = time_at_home
                break
