import inspect
import typing
from dataclasses import dataclass

_T = typing.TypeVar("_T")


def modelclass(cls: typing.Type[_T]) -> typing.Type[_T]:
    cls = dataclass(cls)
    type_hints = typing.get_type_hints(cls)
    attributes = [
        a
        for a in type_hints.keys()
        if not a.startswith("__") and not inspect.isroutine(getattr(cls, a, None))
    ]

    def init(self, *args, **kwargs):
        for i, a in enumerate(args):
            if i < len(attributes):
                self.__dict__[attributes[i]] = a
        for k, v in kwargs.items():
            if k in attributes:
                self.__dict__[k] = v

    cls.__init__ = init  # type: ignore[assignment]

    return cls
