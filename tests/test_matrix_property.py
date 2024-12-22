from __future__ import annotations

from typing import Any

import pytest
from maya.api import OpenMaya

from attribs.base import MatrixProperty


def test_matrix_property_default_returns_identity_mmatrix() -> None:
    prop = MatrixProperty()
    obj = type("Foo", (), {"bar": prop})()
    assert prop.__get__(obj, obj.__class__) == OpenMaya.MMatrix.kIdentity


@pytest.mark.parametrize(
    ("value"),
    [
        pytest.param(
            [1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 1, 0, 2, 2, 2, 1],
            id="List",
        ),
        pytest.param(
            OpenMaya.MMatrix([1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 1, 0, 2, 2, 2, 1]),
            id="MMatrix",
        ),
        pytest.param(
            OpenMaya.MTransformationMatrix(
                OpenMaya.MMatrix([1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 1, 0, 2, 2, 2, 1]),
            ),
            id="MTransformationMatrix",
        ),
    ],
)
def test_matrix_property_set_convert_to_mmatrix(value: Any) -> None:  # noqa: ANN401
    prop = MatrixProperty()
    obj = type("Foo", (), {"bar": prop})()

    prop.__set__(obj, value)

    expected = OpenMaya.MMatrix([1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 1, 0, 2, 2, 2, 1])
    result = prop.__get__(obj, obj.__class__)

    assert result.isEquivalent(expected)


def test_matrix_property_set_wrong_type_raise_type_error() -> None:
    prop = MatrixProperty()
    obj = type("Foo", (), {"bar": prop})()

    with pytest.raises(TypeError):
        prop.__set__(obj, 1)  # type: ignore[arg-type]


def test_matrix_property_set_invalid_sequence_raise_value_error() -> None:
    prop = MatrixProperty()
    obj = type("Foo", (), {"bar": prop})()

    with pytest.raises(ValueError):
        prop.__set__(obj, [1])
