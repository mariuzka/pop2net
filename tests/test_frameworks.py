import pop2net as p2n
import agentpy as ap
import mesa

N_AGENTS = 2
N_LOCATIONS = 2
N_STEPS = 10

agentlist = {
    "agentpy": ap.AgentList,
    "mesa": mesa.agent.AgentSet,
}

def _test_p2n_with_framework(framework: str):
    if framework == "agentpy":
        framework_ = ap
    elif framework == "mesa":
        framework_ = mesa

    class Model(ap.Model):
        def setup(self):
            self.env = p2n.Environment(model=self, framework=framework)
            
            # create agents and locations
            if framework == "agentpy":
                locations = framework_.AgentList(model=self, objs=N_LOCATIONS, cls=Location)
                agents = framework_.AgentList(model=self, objs=N_AGENTS, cls=Agent)
            elif framework == "mesa":
                locations = Location.create_agents(model=model, n=N_LOCATIONS)
                agents = Agent.create_agents(model=model, n=N_AGENTS)
            else:
                assert False, "Invalid framework."
            
            # add/connect agents and locations
            self.env.add_locations(locations=locations)
            self.env.add_agents(agents=agents)
            for location in self.env.locations:
                location.add_agents(self.env.agents)

        def step(self):
            self.env.agents.increase_x()
            self.env.locations.increase_y()

    class Agent(p2n.Agent, framework_.Agent):
        def setup(self):
            self.x = 0
        
        def increase_x(self):
            self.x += 1
    
    class Location(p2n.Location, framework_.Agent):
        def setup(self):
            self.y = 0
        
        def increase_y(self):
            self.y += 1
    
    # create model
    model = Model()

    # run model
    if framework == "agentpy":
        model.run(steps=N_STEPS)
    elif framework == "mesa":
        for _ in range(N_STEPS):
            model.step()

    # check the number of agents/locations
    assert len(model.env.locations) == N_LOCATIONS
    assert len(model.env.agents) == N_AGENTS

    # check the types of the agents and the agent list
    assert isinstance(model.env.agents, agentlist[framework])
    for agent in model.env.agents:
        assert isinstance(agent, Agent)
        assert isinstance(agent, p2n.Agent)
        assert isinstance(agent, framework_.Agent)
    
    # check the types of the locations and the location list
    assert isinstance(model.env.locations, agentlist[framework])
    for location in model.env.locations:
        assert isinstance(location, Location)
        assert isinstance(location, p2n.Location)
        assert isinstance(location, framework_.Agent)

    # check if the agents/locations-methods have been executed
    assert all([agent.x == N_STEPS for agent in model.env.agents])
    assert all([location.y == N_STEPS for location in model.env.locations])

    # check location.agents
    for location in model.env.locations:
        assert isinstance(location.agents, agentlist[framework])
        assert len(location.agents) == 2

    # check agents.locations
    for agent in model.env.agents:
        assert isinstance(agent.locations, agentlist[framework])
        assert len(agent.locations) == 2

    # check agent.neighbor()
    for agent in model.env.agents:
        assert isinstance(agent.neighbors(), agentlist[framework])
        assert len(agent.neighbors()) == 1
    
    # check agent.shared_locations()
    shared_locations = model.env.agents[0].shared_locations(model.env.agents[1])
    assert len(shared_locations) == 2
    assert isinstance(shared_locations, agentlist[framework])

    # check agentList functionality #TODO
    carl = model.env.agents[0]
    susi = model.env.agents[1]
    carl.name = "Carl"
    susi.name = "Susi"
    
    if framework == "agentpy":
        list_with_carl = model.env.agents.select(model.env.agents.name == "Carl")
    elif framework == "mesa":
        list_with_carl = model.env.agents.select(lambda agent: agent.name == "Carl")

    assert isinstance(list_with_carl, agentlist[framework])
    assert len(list_with_carl) == 1
    assert list_with_carl[0].name == "Carl"

    # check Agent.connect()
    class TestLocation(p2n.Location, framework_.Agent):
        pass
    carl.connect(susi, location_cls=TestLocation)
    assert len(carl.shared_locations(susi, location_labels=["TestLocation"])) == 1
    assert len(model.env.locations.select(model.env.locations.label == "TestLocation")) == 1 #TODO

    # check Agent.disconnect()
    carl.disconnect(susi, location_labels=["TestLocation"], remove_locations=True)
    assert len(carl.shared_locations(susi, location_labels=["TestLocation"])) == 0
    assert len(model.env.locations.select(model.env.locations.label == "TestLocation")) == 0 #TODO

def test_basic_p2n_with_agentpy():
    _test_p2n_with_framework(framework="agentpy")

def test_basic_p2n_with_mesa():
    _test_p2n_with_framework(framework="mesa")
    