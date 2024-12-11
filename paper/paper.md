# Introduction
Agent-based modeling is a scientific method used in fields such as social sciences, biology, and ecology to simulate the interactions of autonomous agents. 
Relationships between agents, which structure these interactions, are often represented by network graphs. 
Since empirical data on networks is rare, the majority of agent-based models rely on artificially generated networks.
Consequently, generating a valid network structure at the beginning of a simulation, as well as accessing and modifying it during the simulation, are critical steps that must be managed in almost every agent-based model.

Currently, only a few tools are explicitly designed for this purpose.
Most agent-based models use highly abstract network models (e.g., using NetworkX in Python) and randomly place agents within these graphs.
This approach not only ignores correlations between an agent's attributes and its network position, but also reduces the realism of the relations between agents.
Moreover, generating custom networks or making modifications often becomes complicated and inflexible.
On the other hand, network generators for agent-based modeling, such as XXX, tend to be domain-specific and limited in scope.

Pop2net aims to provide an alternative approach by bundling all steps related to network generation and management into a single package.
In Pop2net, relationships between agents are represented through a bipartite graph of agents and locations.
Locations act as contact layers, representing specific contexts through which agents connect.
Pop2net offers a simple syntax to define and combine different location types, enabling the generation of network structures as compounds of multiple contact layers.

# Statement of Need
Pop2net complements existing tools for agent-based modeling in Python with the following features:

## Flexible Network Design:
Using Pop2net's LocationDesigner and Creator classes, agent-based modelers can generate custom network structures in a simple and flexible way by defining different location types.
Location type definitions specify, for example, which agents are connected to a location, how many location instances should be created, whether locations are nested within others, or how strongly the connection between an agent and a location is weighted.
Based on these definitions, the Creator class generates a bipartite network of agents and locations.
Thanks to its modular design, Pop2net allows for easy modification and scaling of network structures.
Location types can also incorporate network graphs based on empirical data or generated via NetworkX.

## Integration of Empirical Micro-Level Data:
Pop2net is designed to integrate empirical micro-level data of simulated entities into the population and network generation processes
The Creator class provides tools to first generate a population of agents based on survey data (or any other micro-level dataset) and then use these empirical attributes when defining location types.
This enables users to ground network generation in empirical data, even in the absence of detailed micro-level network information.

## Enhanced Relationship Management During Simulations:
The bipartite network structure in Pop2net simplifies relationship management during simulations.
Each location type represents a specific class of relationships between agents, making it easy to target or modify specific relationship types.
For example, users can simulate the closure of schools or focus on interactions within a particular context.
This approach also makes conceptualizing network structures more intuitive by framing them as agents meeting other agents via specific locations.

## Seamless Integration with AgentPy and Other Frameworks:
Pop2net extends AgentPy by seamlessly integrating its features.
Networks built with Pop2net can be directly used for simulations within AgentPy.
Additionally, users can integrate Pop2net objects into custom simulation frameworks or export the generated networks as NetworkX graphs, either in their bipartite form or as a pure agent-level projection.

## Network Analysis Tools:
Pop2net includes tools for quickly analyzing the features of generated networks.
These tools ensure that the generated networks meet the intended specifications and proportions.

# Software structure
Technically, Pop2net is a fork of AgentPy that modifies some of AgentPy's core object classes and adds additional object classes to the existing framework.

In Pop2net, the core object classes that must be used are the model, agents, and locations.\
The model class is largely identical to the AgentPy model class, which holds all entities and parameters of the simulation while defining and executing the simulation procedure. In Pop2net, the model object is extended by the following features:

* A graph object that stores all agents and locations as well as their relationships.
* An agent list and a location list, which provide convenient access to agent and location objects.
* Various methods for managing tasks such as connecting agents and locations or exporting the network.

Agents are the (inter)acting entities of the simulation. 
They extend AgentPy's agent class by adding methods to, for example, find neighbors within specific types of locations or connect with other agents through specific locations.

Locations represent the places or contexts where agents interact.
In Pop2net, every connection between agents must be mediated by a location.

In addition to these three core object classes, which enable basic network creation and simulation, Pop2net introduces three additional object classes that enhance network generation and validation.
The Creator, in combination with the LocationDesigner, facilitates the flexible creation of agents and locations and their connections as defined by the LocationDesigner class.
The Inspector class provides methods for quick network analysis, such as visualization and the calculation of network measures.




![](software_structure.png)


# Example code

# Acknowledgements 

# References
