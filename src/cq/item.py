from collections import UserDict
from logging import getLogger

__all__ = ['Sentinel', 'Item', 'Pair', 'UpdatingDict', 'MinDict']
LOG = getLogger(__name__)


class Sentinel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class FalseSentinel(Sentinel):
    def __bool__(self):
        return False


class Item:
    """A convenience class for storing attributes"""

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __getattr__(self, item):
        LOG.debug("Missing from f{self}: {item}")
        return FalseSentinel(item)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return vars(self) == vars(other)

    def __hash__(self):
        return 0

    def __lt__(self, other):
        return False

    def __contains__(self, key):
        return key in self.__dict__

    def json(self):
        """Return a dict containing only primitive, json-compatible values"""
        return vars(self)

    def __str__(self):
        return "<" + ";".join(f"{k}={v}" for k, v in vars(self).items()) + ">"

    def __repr__(self):
        return type(self).__name__ + "(" + ", ".join(f"{k}={v!r}" for k, v in vars(self).items()) + ")"

    def copy(self, **kwargs):
        """Make a shallow copy, optionally with some additional updates"""
        new = Item(**vars(self))
        new.__dict__.update(kwargs)
        return new


class Pair(tuple):
    """A pair, compared only on the first item"""
    def __new__(cls, cost, item):
        return tuple.__new__(cls, (cost, item))

    def __eq__(self, other):
        return self[0] == other[0]

    def __lt__(self, other):
        return self[0] < other[0]


class UpdatingDict(UserDict):
    def __init__(self, dict=None, /, fn=lambda old, new: new, default=None, **kwargs):
        self.fn = fn
        self.default = default
        super().__init__(dict, **kwargs)

    def __setitem__(self, key, value):
        if key in self:
            return super().__setitem__(key, self.fn(self[key], value))
        if self.default is None:
            return super().__setitem__(key, value)
        return super().__setitem__(key, self.fn(self.default, value))

    # def update(self, other):

    @staticmethod
    def add_to_set(old, new):
        if old is None:
            return {new}
        if not isinstance(old, set):
            return {old, new}
        return set.union(old, {new})


class MinDict(UpdatingDict):
    def __init__(self, dict=None, /, **kwargs):
        super().__init__(dict, fn=min, **kwargs)
