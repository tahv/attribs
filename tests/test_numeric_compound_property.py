from __future__ import annotations

import pytest

from attribs.base import NumericCompoundProperty


def test_numeric_compound_property() -> None:
    class Child:
        _foo = 1

        @property
        def foo(self) -> int:
            return self._foo

        @foo.setter
        def foo(self, value: int) -> None:
            if value == 0:
                raise ValueError(str(value))
            self._foo = value

    class Parent:
        foo: NumericCompoundProperty[tuple[int, int], tuple[int, int]] = (
            NumericCompoundProperty()
        )
        children = (Child(), Child())

    assert Parent().foo == (1, 1)

    attr = Parent()
    attr.foo = (12, 13)
    assert attr.foo == (12, 13)
    assert attr.children[0].foo == 12
    assert attr.children[1].foo == 13

    with pytest.raises(ValueError):
        attr.foo = (10, 0)

    assert attr.foo == (12, 13)
