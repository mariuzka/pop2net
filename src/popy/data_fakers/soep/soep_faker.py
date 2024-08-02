"""Faker of SOEP Data.

SOEP is the socio-economic panel. A long lifed panel study.
"""
# TODO: extend docstring.

from typing import Optional

import faker
import numpy as np
import pandas as pd

from .soep_provider import SOEPProvider


def soep(size: int, seed: Optional[int] = None) -> pd.DataFrame:
    """Create a pandas DataFrame with faked SOEP data.

    Args:
        size (int): Minimum number of people in the dataset.
        seed (Optional[int], optional): Optional seed. Defaults to None.

    Returns:
        pd.DataFrame: A fake SEOP dataset.
    """
    np.random.seed(seed)
    faker.Faker.seed(seed)
    fake = faker.Faker()
    fake.add_provider(SOEPProvider)

    # create correlated variables, dependent on child vs. adult
    cases: list[dict] = []
    try:
        while len(cases) < size:
            for person in fake.household_persons():
                person["pid"] = fake.unique.random_int(min=1, max=size * 10)
                cases.append(person)
                if len(cases) == size:
                    raise StopIteration
    except StopIteration:
        pass

    df = pd.DataFrame(cases)
    return df
