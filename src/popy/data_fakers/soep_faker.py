from typing import Optional

import faker
import numpy as np
import pandas as pd

from .soep_provider import SOEPProvider


def soep(size: int, seed: Optional[int] = None) -> pd.DataFrame:

    np.random.seed(seed)
    faker.Faker.seed(seed)
    fake = faker.Faker()
    fake.add_provider(SOEPProvider)

    # create correlated variables, dependent on child vs. adult
    cases = []
    try:
        for _ in range(size):
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
