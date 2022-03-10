from typing import Callable, Collection, Hashable, Iterable, TypeVar


T = TypeVar("T")


def unique(iterable: Iterable[T], key: Callable[[T], Hashable]) -> Collection[T]:
    return {key(item): item for item in iterable}.values()
