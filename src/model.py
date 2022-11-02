import agentpy as ap

from .sequences import LocationList


class Model(ap.Model):
    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)

    def sim_step(self):

        self.t += 1
        self.step()
        self.population.update()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False
