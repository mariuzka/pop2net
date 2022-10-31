import random
import statistics as stats
from collections import deque
from typing import List

import agentpy as ap


class BaseAgent(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self._contacts = set()
        self._contact_diary = []
        self._locations = dict()
        self._hours_not_at_home: List[int] = []

    @property
    def _n_agents_ever_met(self) -> int:
        return len(self._contacts)

    @property
    def _mean_hours_not_at_home(self) -> float:
        return stats.mean(self._hours_not_at_home)

    @property
    def _max_hours_not_at_home(self) -> int:
        return max(self._hours_not_at_home)

    def _add_contact(self, contact):
        self._contact_diary.append(contact)

    def _clean_diary(self):
        self._contact_diary = []

    def _visit_locations(self, model):
        """
        Agent visits all its locations and writes its visit in the locations' daily guest books,
        if the corresponding visiting conditions are met.
        """

        # the number of hours the agent spends at other locations than home
        hours_not_at_home = 0

        # for each location category the agent has in its dictionary of locations
        for category in self._locations:
            if category != "home":

                # get the condition that determines whether the agent visits this location today
                cond = self._locations[category]["visit_condition"]

                # if there is no condition or the condition is already True
                #  or a given condition(environment, agent) that was checked is True
                if cond is None or cond is True or cond(model, self):
                    # choose a location-object from the category
                    # (most of the time it is just one object)
                    location = random.choice(self._locations[category]["objects"])

                    # get the number of hours the agent spends at the location
                    hours = self._locations[category]["n_hours_per_visit"]

                    # only if the agent spends time at the location, it gets registered as a
                    # visitor at the location
                    if hours > 0:
                        location.visitors_of_the_day.append((self, hours))
                        hours_not_at_home += hours

        self.hours_not_at_home.append(hours_not_at_home)

        # if the agent has any hours at home, register him as an visitor at the home location
        hours_at_home = 24 - hours_not_at_home
        if hours_at_home > 0:
            self.home_location.visitors_of_the_day.append([self, hours_at_home])
