---
title: 'Pop2net'
bibliography: paper.bib
---

## Introduction
Agent-based modeling is a scientific method used in fields such as social science, biology, and ecology to simulate the interactions of autonomous agents and study the resulting emergent phenomena.
Relationships between agents, which structure the simulated interactions, are often represented by network graphs.
Since empirical data on networks is rare, most of agent-based models rely on artificially generated networks [@amblard_which_2015].
Consequently, generating a valid network structure at the beginning of a simulation, as well as accessing and modifying it during the simulation, are critical steps that must be managed in almost every agent-based model.

Pop2net is a Python package that bundles many steps related to network generation and management for agent-based modeling using a special approach in dealing with relations between agents:
In Pop2net, relations are represented as a bipartite graph of agents and locations.
Locations act as a contact layer, representing specific contexts through which agents connect.
This makes it easy to generate and to manage custom network structures in an agent-based model.
Pop2net is mainly an extension to the existing agent-based modeling framework AgentPy [@foramitti_agentpy_2021], but can also be used to generate networks for other modeling frameworks.

## Statement of Need

Currently, there are only a few tools exist designed to create and manage networks for agent-based modeling.
General purpose agent-based modeling packages such as Mesa [@kazil_utilizing_2020], AgentPy [@foramitti_agentpy_2021] or Melodie [@yu_melodie_2023] provide basic data types to represent networks, but lack tools to create these network structures.
Existing network generators explicitly designed for agent-based modeling, such as SynthPops (CITE), lack of generalization and are often domain-specific and limited in scope.
Thus, most agent-based models rely on highly abstract network models, e.g. using NetworkX in Python [@hagberg_exploring_2008], and randomly placing agents within these graphs [@amblard_which_2015].
This approach not only generates networks with low realism regarding the edges, but also ignores correlations between agent attributes and network positions.
Custom modifications of these network models to adapt the network to the research design are often complicated and inflexible.

Pop2net aims to fill this gap in the toolbox of agent-based modelers by providing a framework for creating and managing custom network structures while integrating empirical data and traditional network models.
We identify three core features existing software for agent-based modeling is currently missing:

We identify three core features that existing software for agent-based modeling is currently missing:

1. **A bipartite approach to networks.**
    Pop2net implements a bipartite approach to social networks, which simplifies the creation and management of relations between agents in simulation models.
    The approach of creating a network based on agents and locations is not entirely new, but it is already common in epidemiological agent-based models (CITE?).
    However, Pop2net is the first software package to implement this approach in a general package for network generation and management in agent-based modeling.

2. **Scalable and modular network generation.**
    Based on the bipartite approach, Pop2net offers a completely new way of creating networks programmatically and modularly.
    Users can quickly create complex networks based on different location definitions that are translated into network structures.
    Each location definition contains a set of rules for how agents connect, can integrate empirical data as well as classic network models, and can be combined in a modular way.

3. **Integration of survey data.**
    Pop2net is designed to integrate empirical micro-level data of simulated entities into the population and network generation processes.
    Pop2net provides tools to first generate a population of agents based on survey data (or any other micro-level dataset) and then use these empirical attributes when determining the rules for how agents connect via location definitions.
    This enables users to ground network generation in empirical data, even in the absence of detailed micro-level network information.

## Software structure
Model, Agent, and Location are the three core object classes in Pop2net that must be used to create a network that can be utilized in agent-based modeling.
This network can be directly used to run a simulation within Pop2net or exported as a NetworkX object.
Since these core elements of Pop2net are based on AgentPy, Pop2net can be seamlessly integrated into the AgentPy framework and its tools.

The **Model** class is largely identical to the AgentPy Model class, which holds all entities and parameters of the simulation while defining and executing the simulation procedure.
In Pop2net, Agentpy's Model object is extended by the following features:

* A graph object that stores all agents and locations as well as their relationships.
* An agent list and a location list that provide convenient access to agent and location objects.
* Various methods for managing tasks such as connecting agents and locations or exporting the network.

**Agents** are the (inter)acting entities of the simulation.
They extend AgentPy's agent class by adding methods to, for example, access all locations that the agent is associated with, find neighbors within certain location types or connect them to other agents via certain locations.
**Locations** represent the places or contexts in which agents interact.
In Pop2net, every connection between agents must be mediated by a location.

In addition to these three core object classes that enable basic network creation and simulation, Pop2net introduces three object classes that enhance network generation and validation.

The **Creator** class is one of the main contributions of Pop2net.
In combination with the **LocationDesigner** class, it facilitates the flexible creation of agents and locations and their connections.
By defining location types using the LocationDesigner, users can quickly specify, for example, which agents are connected to a location, how many location instances should be created, whether locations are nested within other locations, or how strongly the connection between an agent and a location is weighted.
Based on these definitions, the Creator class generates a bipartite network of agents and locations.
Location types can also incorporate network graphs based on empirical data or generated by NetworkX.
The Creator also provides tools to conveniently facilitate the use of survey data to create the population of agents before establishing the relations between them.

The **Inspector** class provides methods for quick network analysis, such as visualization and the calculation of network measures.

## Example code

## Acknowledgements

## References



