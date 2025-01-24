---
title: 'Pop2net'
bibliography: paper.bib
---


## Introduction

Agent-based modeling is a scientific method used in fields such as social science, biology, and ecology to simulate the interactions of autonomous agents and study the resulting emergent phenomena.
The relationships between agents that structure the simulated interactions are often represented by network graphs.
Since empirical data on networks is rare, most of agent-based models rely on artificially generated networks [@amblard_which_2015].
Consequently, generating a valid network structure at the beginning of a simulation, as well as accessing and modifying it during the simulation, are critical steps that must be managed in almost any agent-based model.

Pop2net is a Python package that combines many steps related to network generation and management for agent-based modeling using a bipartite approach:
In Pop2net, relations are represented as a graph of agents and locations.
Locations act as a contact layer, representing specific contexts through which agents connect.
This makes it easy to generate and manage custom network structures in an agent-based model.
Pop2net is mainly an extension to the existing agent-based modeling framework AgentPy [@foramitti_agentpy_2021], but it can also be used to generate networks for other modeling frameworks.


## Statement of Need

Currently, there are only a few tools designed to create and manage networks for agent-based modeling.
General-purpose agent-based modeling packages such as Mesa [@kazil_utilizing_2020], AgentPy [@foramitti_agentpy_2021] or Melodie [@yu_melodie_2023], provide basic data types to represent networks, but they lack tools to create these network structures and do not provide bipartite graphs.
Existing network generators explicitly designed for agent-based modeling, such as SynthPops (CITE), lack generalization and are often domain-specific and limited in scope.
Thus, most agent-based models rely on highly abstract network models, e.g., using NetworkX in Python [@hagberg_exploring_2008] and randomly placing agents within these graphs [@amblard_which_2015].
This approach generates networks with low realism and custom modifications to adapt the network to the research design are often complicated and inflexible.

Pop2net aims to fill this gap in the toolbox of agent-based modelers by providing a framework for creating and managing custom network structures while having the possibility to integrate empirical data and traditional network models.
We identify three core features of Pop2net that existing software for agent-based modeling is currently missing:

1. **A bipartite approach to networks.**
    Pop2net implements a bipartite approach to networks, which simplifies the creation and management of relations between agents in simulation models.
    The approach of creating a network based on agents and locations is not entirely new, but it is already common in epidemiological agent-based models (CITE?).
    However, Pop2net is the first software package to implement this approach in a general package for network generation and management in agent-based modeling.

2. **Scalable and modular network generation.**
    Based on the bipartite approach, Pop2net offers an innovative way of creating networks programmatically and modularly.
    Users can quickly create complex networks based on different location definitions that are translated into network structures.
    Each location definition contains a set of rules for how agents connect and can integrate empirical data as well as classic network models.

3. **Convenient integration of micro-level data.**
    Pop2net is designed to integrate empirical micro-level data, e.g. from surveys, into the population and network generation processes.
    The empirical micro-level data can be used to generate a population of agents and then refer to the empirical attributes when determining the rules of how agents connect via location definitions.
    This enables users---especially from the social sciences---to ground network generation in empirical data, even in the absence of detailed network data.


## Software structure

Pop2net's components can be categorized into three sectors.

1. **Mandatory base classes.**
    The first sector contains the three object classes---Model, Agent, and Location---that must always be used to facilitate the bipartite network structure of Pop2net.
    The Model class is largely identical to the AgentPy Model class, which holds all entities and parameters of the simulation while defining and executing the simulation procedure.
    In Pop2net, Agentpy's Model object is extended by the following features:

    * A graph object that stores all agents and locations as well as their relationships.
    * An agent list and a location list that provide convenient access to agent and location objects.
    * Various methods for managing tasks such as connecting agents and locations or exporting the network.

    Agents are the (inter)acting entities of the simulation.
    They extend AgentPy's agent class by adding methods to, for example, access all locations that the agent is associated with, find neighbors within certain location types, or connect them to other agents via certain locations.
    Locations represent the places or contexts in which agents interact.
    In Pop2net, every connection between agents must be mediated by a location.

    Model, Agent, and Location replace the corresponding classes from AgentPy and introduce a strict bipartite interaction structure.
    They can be used to directly run a simulation in Pop2net, but can also be combined with the remaining AgentPy classes, for instance the Experiment class, to get the convenient AgentPy experience when running multiple simulations.

2. **Network generators.**
    The classes Creator and LocationDesigner are the tools in Pop2net that enable the user to generate custom (bipartite) networks.
    By defining location types using the LocationDesigner, users can quickly specify, for example, which agents are connected to a location, how many location instances should be created, whether locations are nested within other locations, or how strongly the connection between an agent and a location is weighted.
    Based on these definitions, the Creator class generates a bipartite network of agents and locations which can be directly used in a simulation or be exported in NetworkX format.
    The Creator provides convenient methods to generate agents and their attributes directly from empirical micro-level data, e.g. survey data.
    Those empirically created attributes support the creation of realistic network structures by including them in the location definitions, for instance, the age or the household of the agents.
    Location types can also incorporate network graphs based on empirical data or generated by NetworkX.

3. **Inspection tools.**
    The NetworkInspector class provides methods for quick network analysis, such as visualization and the calculation of network measures.

## Documentation

To make Pop2net as user-friendly as possible, we also provide comprehensive documentation.
This not only describes the package's API, but also provides detailed tutorials that explain how to create agents, locations and networks using interactive network diagrams and simulations with sample data sets.[^1]

[^1]: The tutorials are available at: [https://mariuzka.github.io/pop2net/section_introduction.html](https://mariuzka.github.io/pop2net/section_introduction.html)

## Acknowledgements

We acknowledge the support of the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation under the DFG reference number UP 31/1) for the Stuttgart Research Focus Interchange Forum for Reflecting on Intelligent Systems (IRIS).

## References
