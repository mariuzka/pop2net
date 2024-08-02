"""Popy. An extension package for location-based simulations based on AgentPy."""

from agentpy import AgentList

from .agent import Agent
from .exceptions import PopyException
from .location import Location, MagicLocation, MeltLocation
from .inspector import NetworkInspector
from .model import Model
from .sequences import LocationList
from .creator import Creator

__all__ = [
    "AgentList",
    "Agent",
    "PopyException",
    "Location",
    "MagicLocation",
    "MeltLocation",
    "NetworkInspector",
    "Model",
    "LocationList",
    "Creator",
]
