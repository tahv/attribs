from __future__ import annotations

import pytest
from maya.api import OpenMaya

from attribs.base import MayaNumeric, NumericProperty


@pytest.mark.parametrize(
    ("numeric_cls", "unit", "value", "expected"),
    [
        pytest.param(float, None, 1.2, 1.2, id="float"),
        pytest.param(float, None, None, None, id="None"),
        pytest.param(
            OpenMaya.MAngle,
            OpenMaya.MAngle.kDegrees,
            OpenMaya.MAngle(0, OpenMaya.MAngle.kRadians),
            OpenMaya.MAngle(0, OpenMaya.MAngle.kDegrees),
            id="MAngle-radians-to-degrees",
        ),
        pytest.param(
            OpenMaya.MAngle,
            OpenMaya.MAngle.kRadians,
            OpenMaya.MAngle(0, OpenMaya.MAngle.kRadians),
            OpenMaya.MAngle(0, OpenMaya.MAngle.kRadians),
            id="MAngle-radians-to-radians",
        ),
        pytest.param(
            OpenMaya.MAngle,
            OpenMaya.MAngle.kRadians,
            OpenMaya.MAngle(0, OpenMaya.MAngle.kDegrees),
            OpenMaya.MAngle(0, OpenMaya.MAngle.kRadians),
            id="MAngle-degrees-to-radians",
        ),
        pytest.param(
            OpenMaya.MAngle,
            OpenMaya.MAngle.kRadians,
            0,
            OpenMaya.MAngle(0, OpenMaya.MAngle.kRadians),
            id="float-to-MAngle",
        ),
    ],
)
def test_numeric_property_convert_value(
    numeric_cls: type[MayaNumeric],
    unit: int | None,
    value: MayaNumeric | None,
    expected: MayaNumeric | None,
) -> None:
    prop: NumericProperty[MayaNumeric] = NumericProperty()
    obj = type(
        "Foo",
        (),
        {"bar": prop, "NUMERIC_CLS": numeric_cls, "unit": unit},
    )()

    prop.__set__(obj, value)

    result = prop.__get__(obj, obj.__class__)

    if isinstance(expected, (float, int)):
        assert result == expected
    elif expected is None:
        assert result is None
    else:
        assert result.value == expected.value
        assert result.unit == expected.unit
