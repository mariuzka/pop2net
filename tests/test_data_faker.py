import pytest


@pytest.mark.parametrize(
    "soep_fixture,size",
    [
        ("soep100", 100),
        ("soep1000", 1000),
        ("soep10_000", 10_000),
    ],
)
def test_dataframe_size(soep_fixture, size, request):
    print(soep_fixture)
    soep = request.getfixturevalue(soep_fixture)
    assert len(soep) == size


@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_pid_unique(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    assert soep.pid.nunique() == len(soep)


@pytest.mark.parametrize("soep_fixture", ["soep100", "soep1000", "soep10_000"])
def test_children_not_working(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    n_hours = soep.loc[soep.age < 18, "work_hours_day"].sum()
    assert n_hours == 0


@pytest.mark.parametrize("soep_fixture", ["soep1000", "soep10_000"])
def test_all_genders_used(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    assert set(soep.gender) == {1.0, 2.0, -1.0}
