# ruff: noqa: D102, D105, D107
"""Agentpy Lists Module.

Content: Lists for objects, environments, and agents.

BSD 3-Clause License

Copyright (c) 2020-2021 Joël Foramitti

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import annotations

from collections.abc import Sequence

from . import location


class LocationSequence:
    """Base class for agenpty sequences."""

    def __repr__(self):
        """Return a REPL representation of LocationSequence.

        Returns:
            str: REPL representation.
        """
        len_ = len(list(self))
        s = "s" if len_ != 1 else ""
        return f"{type(self).__name__} ({len_} object{s})"

    def __getattr__(self, name):
        """Return callable list of attributes."""
        if name[0] == "_":  # Private variables are looked up normally
            # Gives numpy conversion correct error for __array_struct__ lookup
            super().__getattr__(name)
        else:
            return AttrIter(self, attr=name)

    def _set(self, key, value):
        object.__setattr__(self, key, value)

    @staticmethod
    def _obj_gen(model, n, cls, *args, **kwargs):
        """Generate objects for sequence."""
        if cls is None:
            cls = location.Location

        if args != ():
            msg = (
                "Sequences no longer accept extra arguments without a keyword. "
                f"Please assign a keyword to the following arguments: {args}"
            )
            raise Exception(
                msg,
            )

        for i in range(n):
            # AttrIter values get broadcasted among agents
            i_kwargs = {
                k: arg[i] if isinstance(arg, AttrIter) else arg for k, arg in kwargs.items()
            }
            yield cls(model, **i_kwargs)


# Attribute List ------------------------------------------------------------ #


class AttrIter(LocationSequence, Sequence):
    """Iterator over an attribute of objects in a sequence.

    Length, items access, and representation work like with a normal list.
    Calls are forwarded to each entry and return a list of return values.
    Boolean operators are applied to each entry and return a list of bools.
    Arithmetic operators are applied to each entry and return a new list.
    If applied to another `AttrList`, the first entry of the first list
    will be matched with the first entry of the second list, and so on.
    Else, the same value will be applied to each entry of the list.
    See :class:`AgentList` for examples.
    """

    def __init__(self, source, attr=None):
        """_summary_.

        Args:
            source (_type_): _description_
            attr (_type_, optional): _description_. Defaults to None.
        """
        self.source = source
        self.attr = attr

    def __repr__(self):
        """Return a REPL representation of LocationSequence.

        Returns:
            str: REPL representation.
        """
        return repr(list(self))

    @staticmethod
    def _iter_attr(a, s):
        for o in s:
            yield getattr(o, a)

    def __iter__(self):
        """Iterate through source list based on attribute."""
        if self.attr:
            return self._iter_attr(self.attr, self.source)
        else:
            return iter(self.source)

    def __len__(self):
        return len(self.source)

    def __getitem__(self, key):
        """Get item from source list."""
        if self.attr:
            return getattr(self.source[key], self.attr)
        else:
            return self.source[key]

    def __setitem__(self, key, value):
        """Set item to source list."""
        if self.attr:
            setattr(self.source[key], self.attr, value)
        else:
            self.source[key] = value

    def __call__(self, *args, **kwargs):
        return AttrIter([func_obj(*args, **kwargs) for func_obj in self])

    def __eq__(self, other):
        return [obj == other for obj in self]

    def __ne__(self, other):
        return [obj != other for obj in self]

    def __lt__(self, other):
        return [obj < other for obj in self]

    def __le__(self, other):
        return [obj <= other for obj in self]

    def __gt__(self, other):
        return [obj > other for obj in self]

    def __ge__(self, other):
        return [obj >= other for obj in self]

    def __add__(self, v):
        if isinstance(v, AttrIter):
            return AttrIter([x + y for x, y in zip(self, v)])
        else:
            return AttrIter([x + v for x in self])

    def __sub__(self, v):
        if isinstance(v, AttrIter):
            return AttrIter([x - y for x, y in zip(self, v)])
        else:
            return AttrIter([x - v for x in self])

    def __mul__(self, v):
        if isinstance(v, AttrIter):
            return AttrIter([x * y for x, y in zip(self, v)])
        else:
            return AttrIter([x * v for x in self])

    def __truediv__(self, v):
        if isinstance(v, AttrIter):
            return AttrIter([x / y for x, y in zip(self, v)])
        else:
            return AttrIter([x / v for x in self])

    def __iadd__(self, v):
        return self + v

    def __isub__(self, v):
        return self - v

    def __imul__(self, v):
        return self * v

    def __itruediv__(self, v):
        return self / v


class LocationList(LocationSequence, list):
    """List of agentpy objects.

    Attribute calls and assignments are applied to all agents
    and return an :class:`AttrIter` with the attributes of each agent.
    This also works for method calls, which returns a list of return values.
    Arithmetic operators can further be used to manipulate agent attributes,
    and boolean operators can be used to filter the list based on agents'
    attributes. Standard :class:`list` methods can also be used.

    Arguments:
        model (Model): The model instance.
        objs (int or Sequence, optional):
            An integer number of new objects to be created,
            or a sequence of existing objects (default empty).
        cls (type, optional): Class for the creation of new objects.
        **kwargs:
            Keyword arguments are forwarded
            to the constructor of the new objects.
            Keyword arguments with sequences of type :class:`AttrIter` will be
            broadcasted, meaning that the first value will be assigned
            to the first object, the second to the second, and so forth.
            Otherwise, the same value will be assigned to all objects.

    Examples:
        Prepare an :class:`AgentList` with three agents::

            >>> model = ap.Model()
            >>> agents = model.add_agents(3)
            >>> agents
            AgentList [3 agents]

        The assignment operator can be used to set a variable for each agent.
        When the variable is called, an :class:`AttrList` is returned::

            >>> agents.x = 1
            >>> agents.x
            AttrList of 'x': [1, 1, 1]

        One can also set different variables for each agent
        by passing another :class:`AttrList`::

            >>> agents.y = ap.AttrIter([1, 2, 3])
            >>> agents.y
            AttrList of 'y': [1, 2, 3]

        Arithmetic operators can be used in a similar way.
        If an :class:`AttrList` is passed, different values are used for
        each agent. Otherwise, the same value is used for all agents::

            >>> agents.x = agents.x + agents.y
            >>> agents.x
            AttrList of 'x': [2, 3, 4]

            >>> agents.x *= 2
            >>> agents.x
            AttrList of 'x': [4, 6, 8]

        Attributes of specific agents can be changed through setting items::

            >>> agents.x[2] = 10
            >>> agents.x
            AttrList of 'x': [4, 6, 10]

        Boolean operators can be used to select a subset of agents::

            >>> subset = agents(agents.x > 5)
            >>> subset
            AgentList [2 agents]

            >>> subset.x
            AttrList of attribute 'x': [6, 8]
    """

    def __init__(self, model, objs=(), cls=None, *args, **kwargs):
        if isinstance(objs, int):
            objs = self._obj_gen(model, objs, cls, *args, **kwargs)
        super().__init__(objs)
        super().__setattr__("model", model)
        super().__setattr__("ndim", 1)

    def __setattr__(self, name, value):
        if isinstance(value, AttrIter):
            # Apply each value to each agent
            for obj, v in zip(self, value):
                setattr(obj, name, v)
        else:
            # Apply single value to all agents
            for obj in self:
                setattr(obj, name, value)

    def __add__(self, other):
        agents = LocationList(self.model, self)
        agents.extend(other)
        return agents

    def select(self, selection):
        """Returns a new :class:`AgentList` based on `selection`.

        Arguments:
            selection (list of bool): List with same length as the agent list.
                Positions that return True will be selected.
        """
        return LocationList(self.model, [a for a, s in zip(self, selection) if s])

    def sort(self, var_key, reverse=False):
        """Sorts the list in-place, and returns self.

        Arguments:
            var_key (str): Attribute of the lists' objects, based on which
                the list will be sorted from lowest value to highest.
            reverse (bool, optional): Reverse sorting (default False).
        """
        super().sort(key=lambda x: x[var_key], reverse=reverse)
        return self

    def shuffle(self):
        """Shuffles the list in-place, and returns self."""
        self.model.random.shuffle(self)
        return self
