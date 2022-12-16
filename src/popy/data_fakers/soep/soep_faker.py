from typing import Dict
from typing import List
from typing import Optional

import faker
import numpy as np
import pandas as pd

from . import constants as c
from .soep_provider import SOEPProvider


def soep(size: int, seed: Optional[int] = None) -> pd.DataFrame:

    np.random.seed(seed)
    faker.Faker.seed(seed)
    fake = faker.Faker()
    fake.add_provider(SOEPProvider)

    # create correlated variables, dependent on child vs. adult
    cases: List[Dict] = []
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
