.. pop2net documentation master file, created by
   sphinx-quickstart on Wed Nov 30 12:19:20 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pop2net's documentation!
===================================

Agent-based modeling (ABM) is a scientific method used in fields such as social science, biology, and ecology to simulate interactions of autonomous agents and study the resulting emergent phenomena.
The relationships between agents, which structure the simulated interactions, are often represented by network graphs.
Since empirical data on networks is rare, most agent-based models rely on artificially generated networks.
Consequently, generating a valid network structure at the beginning of a simulation is critical.
Addtionally, accessing and modifying the network during the simulation are steps that must be managed in almost any agent-based model.

**Pop2net** is a Python package that combines many steps related to network generation and management for ABM using a bipartite approach.
Bipartite networks consist of two distinct types of entities where edges are only formed between entities of different types.
In Pop2net, relationships are represented as bipartite networks connecting *actors* and *locations*.
When two actors are linked to the same location, they are considered connected through that shared location.
In this way, locations serve as a contact layer between actors, representing places where interactions occur or contexts that facilitate actor connections.
The aim of Pop2net's bipartite approach to relations is to simplify the generation and management of realistic network structures in ABM.
Due to its possible integration into `Mesa <https://mesa.readthedocs.io/latest/>`_ and `AgentPy <https://agentpy.readthedocs.io/en/latest/>`_ , networks built with Pop2net can be directly used to run simulations.
Pop2net also offers tools to create populations of agents based on empirical micro-data and to validate network properties.

The following figure provides an overview of the workflow to generate networks using Pop2net:

.. image:: ../paper/img/flowchart.png
  :width: 800
  :alt: Alternative text



.. toctree::
   :maxdepth: 1
   :caption: Contents:

   section_introduction
   installation
   api/index
   section_examples
   developers
