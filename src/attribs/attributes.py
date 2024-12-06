from __future__ import annotations

import sys
from types import MappingProxyType
from typing import Sequence, Tuple, Union, cast

from maya.api import OpenMaya

from attribs.base import (
    Attribute,
    AttributeKwargs,
    MatrixProperty,
    NumericAttribute,
    NumericCompoundAttribute,
)

if sys.version_info < (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack


class Message(Attribute):
    """Message attribute.

    Used to declare relationships between nodes.

    Doesn't contain or transmit any data.
    Its only purpose is to declare relationships between nodes
    by connecting 2 messages plugs together.
    """

    MFN_CLS = OpenMaya.MFnMessageAttribute


class DoubleMatrix(Attribute):
    """64-bit double precision ``OpenMaya.MMatrix`` attribute."""

    MFN_CLS = OpenMaya.MFnMatrixAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnMatrixAttribute.kDouble)

    default = MatrixProperty()

    def __init__(
        self,
        name: str,
        *,
        default: Sequence[float]
        | OpenMaya.MMatrix
        | OpenMaya.MTransformationMatrix
        | None = None,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        setattr(self, "default", default)  # noqa: B010


class FloatMatrix(Attribute):
    """32-bit single precision ``OpenMaya.MMatrix`` attribute."""

    MFN_CLS = OpenMaya.MFnMatrixAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnMatrixAttribute.kFloat)

    default = MatrixProperty()

    def __init__(
        self,
        name: str,
        *,
        default: Sequence[float]
        | OpenMaya.MMatrix
        | OpenMaya.MTransformationMatrix
        | None = None,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        setattr(self, "default", default)  # noqa: B010


class String(Attribute):
    """String attribute."""

    MFN_CLS = OpenMaya.MFnTypedAttribute
    DATA_TYPE = OpenMaya.MFnData.kString

    def __init__(
        self,
        name: str,
        *,
        default: str = "",
        as_filename: bool = False,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        self.as_filename: bool = as_filename
        self.default: str = default


class Curve(Attribute):
    """Curve attribute."""

    MFN_CLS = OpenMaya.MFnTypedAttribute
    DATA_TYPE = OpenMaya.MFnData.kNurbsCurve


class Bool(Attribute):
    """Boolean attribute."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.kBoolean)

    def __init__(
        self,
        name: str,
        *,
        default: bool = False,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        self.default: bool = default


class Compound(Attribute):
    """Container of attributes.

    A Compound attribute allow the grouping of related attributes into a larger unit.
    """

    MFN_CLS = OpenMaya.MFnCompoundAttribute

    def __init__(
        self,
        name: str,
        *,
        children: Sequence[Attribute] = (),
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        self._children: list[Attribute] = list(children)

    def append(self, attribute: Attribute) -> None:  # noqa: D102
        self._children.append(attribute)

    @property
    def children(self) -> tuple[Attribute, ...]:  # noqa: D102
        return tuple(self._children)


class Enum(Attribute):
    """Enum attribute."""

    MFN_CLS = OpenMaya.MFnEnumAttribute

    def __init__(
        self,
        name: str,
        *,
        fields: dict[int, str] | list[str] | None = None,
        default: int | None = None,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        self._fields: dict[int, str] = {}

        if isinstance(fields, list):
            for index, field in enumerate(fields):
                self._fields[index] = field

        elif isinstance(fields, dict):
            for index, field in fields.items():
                self._fields[index] = field

        self._default: int | None = None
        if default is not None:
            self.default = default

    @property
    def fields(self) -> MappingProxyType[int, str]:  # noqa: D102
        return MappingProxyType(self._fields)

    @property
    def default(self) -> int:
        """Default index."""
        if self._default is not None:
            return self._default
        if self._fields:
            return min(self._fields.keys())
        return 0

    @default.setter
    def default(self, value: int) -> None:
        if value not in self._fields:
            message = f"Invalid index `{value}`"
            raise ValueError(message)
        self._default = value


class Double(NumericAttribute[float, None]):
    """64-bit double precision attribute."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.kDouble)
    NUMERIC_CLS = float
    DEFAULT_UNIT = None


class Double2(
    NumericCompoundAttribute[
        Tuple[Double, Double],
        Tuple[float, float],
        Tuple[Union[float, None], Union[float, None]],
        None,
    ],
):
    """Numeric compound of 2 `Double` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Double)
    CHILD_CLS = Double
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = None


class Double3(
    NumericCompoundAttribute[
        Tuple[Double, Double, Double],
        Tuple[float, float, float],
        Tuple[Union[float, None], Union[float, None], Union[float, None]],
        None,
    ],
):
    """Numeric compound of 3 `Double` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Double)
    CHILD_CLS = Double
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = None


class Double4(
    NumericCompoundAttribute[
        Tuple[Double, Double, Double, Double],
        Tuple[float, float, float, float],
        Tuple[
            Union[float, None],
            Union[float, None],
            Union[float, None],
            Union[float, None],
        ],
        None,
    ],
):
    """Numeric compound of 4 `Double` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k4Double)
    CHILD_CLS = Double
    CHILD_SUFFIXES = ("X", "Y", "Z", "W")
    DEFAULT_UNIT = None


# TODO: Scale ?
# TODO: Quaternion ?


class Distance(NumericAttribute[OpenMaya.MDistance, int]):
    """`OpenMaya.MDistance` attribute."""

    MFN_CLS = OpenMaya.MFnUnitAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnUnitAttribute.kDistance)
    NUMERIC_CLS = OpenMaya.MDistance
    DEFAULT_UNIT = OpenMaya.MDistance.kCentimeters


class Distance2(
    NumericCompoundAttribute[
        Tuple[Distance, Distance],
        Tuple[OpenMaya.MDistance, OpenMaya.MDistance],
        Tuple[
            Union[float, None, OpenMaya.MDistance],
            Union[float, None, OpenMaya.MDistance],
        ],
        int,
    ],
):
    """Numeric compound of 2 `Distance` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Double)
    CHILD_CLS = Distance
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = OpenMaya.MDistance.kCentimeters


class Distance3(
    NumericCompoundAttribute[
        Tuple[Distance, Distance, Distance],
        Tuple[OpenMaya.MDistance, OpenMaya.MDistance, OpenMaya.MDistance],
        Tuple[
            Union[float, None, OpenMaya.MDistance],
            Union[float, None, OpenMaya.MDistance],
            Union[float, None, OpenMaya.MDistance],
        ],
        int,
    ],
):
    """Numeric compound of 3 `Distance` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Double)
    CHILD_CLS = Distance
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = OpenMaya.MDistance.kCentimeters


class Angle(NumericAttribute[OpenMaya.MAngle, int]):
    """`OpenMaya.MAngle` attribute."""

    MFN_CLS = OpenMaya.MFnUnitAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnUnitAttribute.kAngle)
    NUMERIC_CLS = OpenMaya.MAngle
    DEFAULT_UNIT = OpenMaya.MAngle.kDegrees


class Angle2(
    NumericCompoundAttribute[
        Tuple[Angle, Angle],
        Tuple[OpenMaya.MAngle, OpenMaya.MAngle],
        Tuple[
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
        ],
        int,
    ],
):
    """Numeric compound of 2 `Angle` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Double)
    CHILD_CLS = Angle
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = OpenMaya.MAngle.kDegrees


class Angle3(
    NumericCompoundAttribute[
        Tuple[Angle, Angle, Angle],
        Tuple[OpenMaya.MAngle, OpenMaya.MAngle, OpenMaya.MAngle],
        Tuple[
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
        ],
        int,
    ],
):
    """Numeric compound of 3 `Angle` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Double)
    CHILD_CLS = Angle
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = OpenMaya.MAngle.kDegrees


class Angle4(
    NumericCompoundAttribute[
        Tuple[Angle, Angle, Angle, Angle],
        Tuple[OpenMaya.MAngle, OpenMaya.MAngle, OpenMaya.MAngle, OpenMaya.MAngle],
        Tuple[
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
            Union[float, None, OpenMaya.MAngle],
        ],
        int,
    ],
):
    """Numeric compound of 4 `Angle` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k4Double)
    CHILD_CLS = Angle
    CHILD_SUFFIXES = ("X", "Y", "Z", "W")
    DEFAULT_UNIT = OpenMaya.MAngle.kDegrees


class Float(NumericAttribute[float, None]):
    """32-bit single precision attribute."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.kFloat)
    NUMERIC_CLS = float
    DEFAULT_UNIT = None


class Float2(
    NumericCompoundAttribute[
        Tuple[Float, Float],
        Tuple[float, float],
        Tuple[Union[float, None], Union[float, None]],
        None,
    ],
):
    """Numeric compound of 2 `Float` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Float)
    CHILD_CLS = Float
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = None


class Float3(
    NumericCompoundAttribute[
        Tuple[Float, Float, Float],
        Tuple[float, float, float],
        Tuple[Union[float, None], Union[float, None], Union[float, None]],
        None,
    ],
):
    """Numeric compound of 3 `Float` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Float)
    CHILD_CLS = Float
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = None


class Color(
    NumericCompoundAttribute[
        Tuple[Float, Float, Float],
        Tuple[float, float, float],
        Tuple[Union[float, None], Union[float, None], Union[float, None]],
        None,
    ],
):
    """Numeric compound of 3 `Float` attributes with suffixes ``R, G, B``.

    Displayed with a color picker in the Attribute Editor.
    """

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Float)
    CHILD_CLS = Float
    CHILD_SUFFIXES = ("R", "G", "B")
    DEFAULT_UNIT = None


class Long(NumericAttribute[int, None]):
    """32-bit integer attribute."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.kLong)
    NUMERIC_CLS = int
    DEFAULT_UNIT = None


class Long2(
    NumericCompoundAttribute[
        Tuple[Long, Long],
        Tuple[int, int],
        Tuple[Union[int, None], Union[int, None]],
        None,
    ],
):
    """Numeric compound of 2 `Long` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Long)
    CHILD_CLS = Long
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = None


class Long3(
    NumericCompoundAttribute[
        Tuple[Long, Long, Long],
        Tuple[int, int, int],
        Tuple[Union[int, None], Union[int, None], Union[int, None]],
        None,
    ],
):
    """Numeric compound of 3 `Long` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Long)
    CHILD_CLS = Long
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = None


class Short(NumericAttribute[int, None]):
    """16-bit integer attribute."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.kShort)
    NUMERIC_CLS = int
    DEFAULT_UNIT = None


class Short2(
    NumericCompoundAttribute[
        Tuple[Short, Short],
        Tuple[int, int],
        Tuple[Union[int, None], Union[int, None]],
        None,
    ],
):
    """Numeric compound of 2 `Short` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k2Short)
    CHILD_CLS = Short
    CHILD_SUFFIXES = ("X", "Y")
    DEFAULT_UNIT = None


class Short3(
    NumericCompoundAttribute[
        Tuple[Short, Short, Short],
        Tuple[int, int, int],
        Tuple[Union[int, None], Union[int, None], Union[int, None]],
        None,
    ],
):
    """Numeric compound of 3 `Short` attributes."""

    MFN_CLS = OpenMaya.MFnNumericAttribute
    DATA_TYPE = cast(int, OpenMaya.MFnNumericData.k3Short)
    CHILD_CLS = Short
    CHILD_SUFFIXES = ("X", "Y", "Z")
    DEFAULT_UNIT = None
