import agentpy as ap

from .sequences import LocationList


class Model(ap.Model):
    """Class the encapsulates a full simluation.

    This very closely follows the logic of the :class:`agentpy.Model` package.

    Args:
        See :agentpy.Model: for more information.
    """

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)

    def sim_step(self):

        self.t += 1

        self.agents.visit_locations()
        self.step()
        # self.population.update()
        self.update()
        self.locations.visit_weights = {}

        if self.t >= self._steps:  # type: ignore
            self.running = False
