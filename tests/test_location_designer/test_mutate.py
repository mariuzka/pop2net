import pytest

import pop2net as p2n


@pytest.fixture
def model():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class NormalLocation(p2n.LocationDesigner):
        pass

    class NormalLocation2(p2n.LocationDesigner):
        pass

    class MutationLocation(p2n.LocationDesigner):
        def mutate(self):
            return {"mutated1": [1, 2, 3], "mutated2": ["x", "y", "z"]}

    creator.create_agents(n=10)
    creator.create_locations(
        location_designers=[
            NormalLocation,
            MutationLocation,
            NormalLocation2,
        ]
    )
    return model


def test_n_locations(model):
    assert len(model.locations) == 11


def test_positions_and_labels(model):
    assert model.locations[0].label == "NormalLocation"
    assert model.locations[1].label == "MutationLocation0"
    assert model.locations[5].label == "MutationLocation4"
    assert model.locations[9].label == "MutationLocation8"
    assert model.locations[10].label == "NormalLocation2"


def test_mutated_values(model):
    assert model.locations[1].mutated1 == 1
    assert model.locations[1].mutated2 == "x"

    assert model.locations[5].mutated1 == 2
    assert model.locations[5].mutated2 == "y"

    assert model.locations[9].mutated1 == 3
    assert model.locations[9].mutated2 == "z"
