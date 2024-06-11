from typing import Any, Iterable, Optional, Self, override, overload

from pygame import Rect
from pygame.sprite import Group as BaseGroup
from pygame.sprite import Sprite


class Group[S: Sprite](BaseGroup):
    spritedict: dict[S, Optional[Rect]]
    lostsprites: list[Rect]

    @override
    def __init__(self, *sprites: S | "Group[S]" | Iterable[S]) -> None:
        self.spritedict = {}
        self.lostsprites = []
        self.add(*sprites)

    @override
    def sprites(self) -> list[S]:
        return list(self.spritedict)

    def add_internal(self, sprite: S) -> None: # type: ignore
        self.spritedict[sprite] = None

    @override
    def remove_internal(self, sprite: S) -> None:
        if lost_rect := self.spritedict[sprite]:
            self.lostsprites.append(lost_rect)
        del self.spritedict[sprite]

    @override
    def has_internal(self, sprite: S) -> bool:
        return sprite in self.spritedict

    @override
    def copy(self: Self) -> Self:
        return self.__class__(self.sprites())

    @override
    def __contains__(self, item: S) -> bool:
        return self.has(item)

    @override
    @overload
    def add(self, *sprites: S) -> None: ...

    @override
    @overload
    def add(self, *sprites: "Group[S]") -> None: ...

    @override
    @overload
    def add(self, *sprites: Iterable[S]) -> None: ...

    @override
    @overload
    def add(self, *sprites: S | "Group[S]" | Iterable[S]) -> None: ...

    @override
    def add(self, *sprites: S | "Group[S]" | Iterable[S]) -> None:
        return super().add(*sprites)

    @override
    @overload
    def remove(self, *sprites: S) -> None: ...

    @override
    @overload
    def remove(self, *sprites: "Group[S]") -> None: ...

    @override
    @overload
    def remove(self, *sprites: Iterable[S]) -> None: ...

    @override
    @overload
    def remove(self, *sprites: S | "Group[S]" | Iterable[S]) -> None: ...

    @override
    def remove(self, *sprites: S | "Group[S]" | Iterable[S]) -> None:
        return super().remove(*sprites)

    @override
    @overload
    def has(self, *sprites: S) -> bool: ...

    @override
    @overload
    def has(self, *sprites: "Group[S]") -> bool: ...

    @override
    @overload
    def has(self, *sprites: Iterable[S]) -> bool: ...

    @override
    @overload
    def has(self, *sprites: S | "Group[S]" | Iterable[S]) -> bool: ...

    @override
    def has(self, *sprites: S | "Group[S]" | Iterable[S]) -> bool:
        return super().has(*sprites)

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        for sprite in self.sprites():
            sprite.update(*args, **kwargs)
