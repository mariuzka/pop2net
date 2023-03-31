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
    assert set(soep.gender) == {"male", "female", "other"}


@pytest.mark.parametrize("soep_fixture", ["soep1000", "soep10_000"])
def test_gender_distribution(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    ratio = len(soep[soep.gender == "male"]) / len(soep)
    assert abs(ratio - 0.5) < 0.05


@pytest.mark.parametrize("soep_fixture", ["soep1000", "soep10_000"])
def test_work_hours_zero(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)
    ratio = len(soep[soep.work_hours_day == 0]) / len(soep)

    # this amount should have work hours == 0
    assert abs(ratio - 0.614786) < 0.1


@pytest.mark.parametrize("soep_fixture", ["soep1000", "soep10_000"])
def test_nace2_distribution_no_work(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)

    # children do not work, therefore should not have nace2
    assert soep[soep.age < 18].nace2_division.eq(-2).all()

    # non-working indivudals should not have nace2
    assert soep[soep.work_hours_day == 0].nace2_division.eq(-2).all()


@pytest.mark.parametrize("soep_fixture", ["soep1000", "soep10_000"])
def test_nace2_distribution_work(soep_fixture, request):
    soep = request.getfixturevalue(soep_fixture)

    # roughly half the population should not have nace2
    ratio = len(soep[soep.nace2_division == -2]) / len(soep)
    assert abs(ratio - 0.5) < 0.1

    # 20% of the working population should not have nace2
    ratio = len(soep[soep.nace2_division == -2]) / len(soep)
    assert abs(ratio - 0.5) < 0.1
