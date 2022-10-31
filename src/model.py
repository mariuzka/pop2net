import agentpy as ap


class PopyModel(ap.Model):
    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)
        self.locations = []

    def sim_step(self):

        self.t += 1
        self.step()

        self.agents.visit_locations(self)
        # i want this as a hidden loop like above
        # Therefore a LocationList has to be implemented (like the AgentList)
        for location in self.locations:
            location.connect_visitors()

        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False
