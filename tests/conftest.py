import faker
import numpy as np
import pandas as pd
import pytest

from src.fakers.soep import SOEPProvider


def soep_dataset_generator(size: int) -> pd.DataFrame:

    np.random.seed(size)
    faker.Faker.seed(size)
    fake = faker.Faker()
    fake.add_provider(SOEPProvider)

    # create correlated variables, dependent on child vs. adult
    cases = []
    try:
        for _ in range(1, size + 1):
            hh_id, hh_size, n_children = fake.household()
            n_adults = hh_size - n_children
            for _ in range(n_adults):
                case = {
                    "pid": fake.unique.random_int(min=1, max=size * 10),
                    "hid": hh_id,
                    "age": fake.age(person="adult"),
                    "gender": fake.gender(),
                    "work_hours_day": fake.work_hours_per_day(person="adult"),
                }
                cases.append(case)
                if len(cases) == size:
                    raise StopIteration
            for _ in range(n_children):
                case = {
                    "pid": fake.unique.random_int(min=1, max=size * 10),
                    "hid": hh_id,
                    "age": fake.age(person="child"),
                    "gender": fake.gender(),
                    "work_hours_day": fake.work_hours_per_day(person="child"),
                }
                cases.append(case)
                if len(cases) == size:
                    raise StopIteration
    except StopIteration:
        pass

    df = pd.DataFrame(cases)
    return df


@pytest.fixture(scope="session")
def soep10():
    return soep_dataset_generator(10)


@pytest.fixture(scope="session")
def soep100():
    return soep_dataset_generator(100)


@pytest.fixture(scope="session")
def soep1000():
    return soep_dataset_generator(1000)


@pytest.fixture(scope="session")
def soep10_000():
    return soep_dataset_generator(10_000)
