"""The model class. It encapsulates the full simulation."""
from __future__ import annotations

import agentpy as ap

from popy.environment import Environment

class Model(ap.Model):
    """Class the encapsulates a full simluation.

    This very closely follows the logic of the :class:`agentpy.Model` package. See
    :class:`agentpy.Model` for more information.
    """

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        """Initiate a simulation.

        Args:
            parameters (dict, optional): An optional parameter dict that is passed to
            :class:`agentpy.Model`. Defaults to None.
            _run_id (int, optional): An optional _run_id that is passed to :class:`agentpy.Model`.
            Defaults to None.
            **kwargs: Optional parameters that are all passed to :class:`agentpy.Model`.
        """
        super().__init__(parameters, _run_id, **kwargs)
        self.env = Environment(self)

    def sim_step(self) -> None:
        """Do 1 step in the simulation."""
        self.t += 1

        for location in [location for location in self.locations if not location.static_weight]:
            location.update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False