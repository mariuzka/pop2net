from typing import Any
from typing import Literal

import faker
import numpy as np
import pandas as pd
import pytest
from faker.providers import BaseProvider


class SOEPProvider(BaseProvider):
    """
    Helps to create Fake Data that is as close to the SOEP as possible.
    Parameters of the random distributions are taken from the original dataset.
    """

    def __init__(self, generator: Any) -> None:
        self.generator = generator
        self.rng = np.random.default_rng()

        # For hhid
        self.hh_child_probs = [
            0.30368745938921377,
            0.23310591293047433,
            0.3468702620749404,
            0.07504873294346978,
            0.02880658436213992,
            0.008203378817413905,
            0.002599090318388564,
            0.0010017327268789257,
            0.00043318171973142733,
            0.00013536928741607104,
            8.122157244964262e-05,
            2.7073857483214208e-05,
        ]
        self.hh_size_dist = lambda: self.rng.poisson(lam=2.673)
        self.hh_n_children_dist = lambda: self._multinomial_select(pvals=self.hh_child_probs)
        self.hh_cur = 0

        # For age
        self.age_adult_dist = lambda: self.rng.normal(loc=46.546, scale=17.399)
        self.age_child_dist = lambda: self.rng.normal(loc=9.554, scale=5.114)

        # For gender
        # small amout of prob left for invalid -1 answer (0.1%)
        self.gender_dist = lambda: self._multinomial_select([0.495, 0.495, 0.01])

        # For work hours per day
        self.work_at_all_dist = lambda: self.rng.binomial(n=1, p=0.554)
        self.work_full_day_dist = lambda: self.rng.binomial(n=1, p=0.188)
        self.work_dist = lambda: self.rng.normal(loc=6.429, scale=2.92)

    def _multinomial_select(self, pvals: list[float]) -> int:
        return np.argmax(self.rng.multinomial(n=1, pvals=pvals))

    def household(self) -> tuple[int, int, int]:

        while (hh_size := self.hh_size_dist()) < 1:
            pass

        if hh_size == 1:
            n_children = 0
        else:
            while (n_children := self.hh_n_children_dist()) >= hh_size:
                pass

        return (self.generator.random_int(), hh_size, n_children)

    def age(self, person: Literal["adult", "child"] = "adult") -> float:

        if person == "child":
            min_age = 0.0
            max_age = 18
            dist = self.age_child_dist
        elif person == "adult":
            min_age = 18
            max_age = 100
            dist = self.age_adult_dist

        # iterate until a positive number
        while not min_age <= (age := dist()) <= max_age:
            pass

        return round(age, 0)

    def work_hours_per_day(self, person: Literal["adult", "child"]) -> float:

        # childs do not work
        if person == "child":
            return 0.0

        # about half of people work at all
        if self.work_at_all_dist() == 0:
            return 0.0

        # of the remaining, about 19% have a full work day (8 hours)
        if self.work_full_day_dist() == 1:
            return 8.0

        # rest is drawn for normal (more like bimodal in SOEP but who cares..)
        while not 0.0 < (hours := self.work_dist()) < 16.0:
            pass

        return round(hours, 6)

    def gender(self) -> float:
        gender = self.gender_dist()
        if gender == 2:
            return -1.0
        return float(gender) + 1.0


def soep_dataset_generator(size: int) -> pd.DataFrame:

    np.random.seed(size)
    faker.Faker.seed(size)
    fake = faker.Faker()
    fake.add_provider(SOEPProvider)

    # create correlated variables, dependent on child vs. adult
    cases = []
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
                break
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
                break
        if len(cases) == size:
            break

    df = pd.DataFrame(cases)
    return df


@pytest.fixture(scope="session")
def soep100():
    return soep_dataset_generator(100)


@pytest.fixture(scope="session")
def soep1000():
    return soep_dataset_generator(1000)


@pytest.fixture(scope="session")
def soep10_000():
    return soep_dataset_generator(10_000)
