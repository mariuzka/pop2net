import pytest

import pop2net as p2n


@pytest.fixture
def model():
    model = p2n.Model()
    creator = p2n.Creator(model)

    class MutationLocation(p2n.LocationDesigner):
        mutated = 0

        def mutate(self):
            return {"mutated": [1, 2, 3]}

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MutationLocation])
    return model


def test_n_locations(model):
    assert len(model.locations) == 3


def test_mutated_values(model):
    for location in model.locations:
        assert location.mutated in [1, 2, 3]


def test_label_name(model):
    for location in model.locations:
        assert location.label.endswith("mutated" + str(location.mutated))
