import agentpy as ap


class Model(ap.Model):
    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)

    def sim_step(self):
        self.agents._visit_locations()
        return super().sim_step()
