import pop2net as p2n


def test_1():
    # basic test+refine
    model = p2n.Model()
    creator = p2n.Creator(model)


    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"


    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Partnership(p2n.MagicLocation):
        couple_id = 1
        recycle = False

        def bridge(self, agent):
            print(self.couple_id)
            return agent.gender
        

        def refine(self):
            for agent in self.agents:
                agent.couple_id = Partnership.couple_id
            Partnership.couple_id += 1

    creator.create_locations(location_classes=[Partnership])
    
    assert len(model.locations) == 2
    assert len(model.agents) == 5

    for i, location in enumerate(model.locations, start=1):
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1
        assert all(agent.couple_id == i for agent in location.agents)
        assert [agent.couple_id for agent in location.agents].count(i) == 2

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 1


def test_2():
    # recyle=True+refine
    model = p2n.Model()
    creator = p2n.Creator(model)


    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"


    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Partnership(p2n.MagicLocation):
        couple_id = 1
        recycle = True

        def bridge(self, agent):
            return agent.gender
        
        def refine(self):
            for agent in self.agents:
                if hasattr(agent, "couple_id"):
                    agent.couple_id.append(Partnership.couple_id)
                else:
                    agent.couple_id = [Partnership.couple_id]
            Partnership.couple_id += 1

    creator.create_locations(location_classes=[Partnership])

    assert len(model.locations) == 3
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1

    assert len(model.agents[3].couple_id) == 2
    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 1
    assert len(model.agents[3].locations) == 2
    assert len(model.agents[4].locations) == 1