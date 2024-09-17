============
About Pop2net
============

Interactions between agents are the key elements of agent-based models.
Thus, the interaction structure in such models must be implemented with care.
When appropriate empirical network data are unavailable, which is often the case, simulation models must rely on network models.
However, in many cases, the classic network models (for instance, random networks, small world networks, etc.) are too abstract to create valid interaction structures.
Existing network generators can be a solution, but they often are domain-specific or do not offer enough control over the network generation.
To fill the gap between often unavailable network data and too abstract network models, we introduce the Python package Pop2net.

Pop2net offers a new way to quickly create detailed network models that can be used for agent-based simulations.
In Pop2net, you create networks by formulating rules for which agents come together in which context and in which way.
For this, Pop2net relies on the concept of contact layers. 
Contact layers act as virtual locations where agents meet.
Pop2net provides a simple syntax to define, for instance, who gets assigned to a certain location and how edges are formed within a location.
Creating networks using contact layers is not new, but is already known from epidemiological agent-based models, for example.
However, Pop2net is the first software package that makes this approach of network generation usable in a general and domain-unspecific framework.

The main output of Pop2net is a bipartite network: a population of agents linked through contact layers.
This linked population can be used directly in an agent-based model or exported in networkX format, for instance.
For the former option, Pop2net behaves as a plugin for the general agent-based modeling framework `AgentPy <https://agentpy.readthedocs.io/en/latest/>`_ .
Pop2net also makes it possible to create the population of agents from empirical individual data easily.
This allows the user to tie the desired properties of the network structure to empirical agent attributes.

It is important to understand, that Pop2net is not a *population synthesizer*.
The main purpose of Pop2net is to connect agents via contact layers to easily generate a valid interaction structure for agent-based models.
Pop2net does not create any original data on the agent-level.
All the data Pop2net uses to create agents must be given by the user.
However, Pop2net makes it very easy to transform (empirical or artificial) micro-level data into agent populations of any size by providing convenient sampling tools.
In addition, Pop2net includes tools to inspect the network properties and compare it to empirical data.

The following figure provides an overview of the workflow to generate networks using Pop2net:

.. image:: popy_overview.png
  :width: 800
  :alt: Alternative text
