"""Popy. An extension package for location-based simulations based on AgentPy."""

from agentpy import AgentList

from .agent import Agent
from .exceptions import PopyException
#from .environment import Environment
from .location import GridLocation
from .location import LineLocation
from .location import Location
from .inspector import NetworkInspector
from .location import RingLocation
from .location import StarLocation
from .location import TreeLocation
from .model import Model
#from .model import FakeModel
from .sequences import LocationList

__all__ = [
    "AgentList",
    "Agent",
    "PopyException",
    "Location",
    "NetworkInspector",
    #"Environment",
    "LineLocation",
    "RingLocation",
    "GridLocation",
    "TreeLocation",
    "StarLocation",
    "Model",
    #"FakeModel",
    "LocationList",
]