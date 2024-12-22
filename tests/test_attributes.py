from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from maya.api import OpenMaya

from attribs.attributes import (
    Angle,
    Angle2,
    Angle3,
    Angle4,
    Bool,
    Color,
    Compound,
    Curve,
    Distance,
    Distance2,
    Distance3,
    Double,
    Double2,
    Double3,
    Double4,
    DoubleMatrix,
    Enum,
    Float,
    Float2,
    Float3,
    FloatMatrix,
    Long,
    Long2,
    Long3,
    Message,
    Short,
    Short2,
    Short3,
    String,
)
from attribs.create import add_attribute

if TYPE_CHECKING:
    from attribs.base import NumericAttribute, NumericCompoundAttribute


def test_create_message(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = Message("foo")
    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)

    mattribute = cast(OpenMaya.MObject, plug.attribute())
    assert mattribute.apiType() == OpenMaya.MFn.kMessageAttribute


@pytest.mark.parametrize(("attribute_cls"), [FloatMatrix, DoubleMatrix])
def test_create_matrix(
    attribute_cls: type[FloatMatrix | DoubleMatrix],
    network_node: OpenMaya.MFnDependencyNode,
) -> None:
    default = OpenMaya.MMatrix([1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 1, 0, 2, 2, 2, 1])
    attribute = attribute_cls("foo", default=default)
    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)

    mattribute = cast(OpenMaya.MObject, plug.attribute())
    assert mattribute.apiType() == OpenMaya.MFn.kMatrixAttribute

    data = OpenMaya.MFnMatrixData(plug.asMObject())
    assert OpenMaya.MMatrix(data.matrix()).isEquivalent(default)


def test_create_string(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = String("foo", default="foobar", as_filename=True)

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)
    assert plug.asString() == "foobar"

    mobject = cast(OpenMaya.MObject, plug.attribute())
    assert mobject.apiType() == OpenMaya.MFn.kTypedAttribute

    mattr = OpenMaya.MFnTypedAttribute(mobject)
    assert mattr.attrType() == OpenMaya.MFnData.kString
    assert mattr.usedAsFilename is True


def test_create_curve(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = Curve("foo")

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)

    mobject = cast(OpenMaya.MObject, plug.attribute())
    assert mobject.apiType() == OpenMaya.MFn.kTypedAttribute

    mattr = OpenMaya.MFnTypedAttribute(mobject)
    assert mattr.attrType() == OpenMaya.MFnData.kNurbsCurve


def test_create_bool(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = Bool("foo", default=False)

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)
    assert plug.asBool() is False

    mobject = cast(OpenMaya.MObject, plug.attribute())
    assert mobject.apiType() == OpenMaya.MFn.kNumericAttribute

    mattr = OpenMaya.MFnNumericAttribute(mobject)
    assert mattr.numericType() == OpenMaya.MFnNumericData.kBoolean  # type: ignore[attr-defined]
    assert mattr.default is False


def test_create_compound(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = Compound("foo")
    attribute.append(Bool("bar"))

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)

    assert plug.isCompound
    assert plug.numChildren() == 1


def test_create_enum(network_node: OpenMaya.MFnDependencyNode) -> None:
    attribute = Enum("foo", fields={1: "bar", 2: "baz"}, default=2)

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)
    assert plug.asShort() == 2

    mobject = cast(OpenMaya.MObject, plug.attribute())
    assert mobject.apiType() == OpenMaya.MFn.kEnumAttribute


def test_enum_fields_from_list() -> None:
    attribute = Enum("foo", fields=["bar", "baz"])
    assert attribute.fields == {0: "bar", 1: "baz"}


def test_enum_no_fields() -> None:
    attribute = Enum("foo")
    assert not attribute.fields
    assert attribute.default == 0


def test_enum_no_default_return_first_index() -> None:
    attribute = Enum("foo", fields={10: "bar", 20: "baz"})
    assert attribute.default == 10


def test_enum_set_unbound_default_raise_value_error() -> None:
    with pytest.raises(ValueError, match="Invalid index `2`"):
        Enum("foo", fields={1: "bar"}, default=2)

    attribute = Enum("foo", fields={1: "bar"})
    with pytest.raises(ValueError, match="Invalid index `2`"):
        attribute.default = 2


@pytest.mark.parametrize(
    ("attr_cls", "default"),
    [
        (Double, 1.5),
        (Distance, 1.5),
        (Angle, 1.5),
        (Float, 1.5),
        (Long, 1),
        (Short, 1),
    ],
)
def test_create_numeric(
    attr_cls: type[NumericAttribute],
    default: float,
    network_node: OpenMaya.MFnDependencyNode,
) -> None:
    attribute = attr_cls("foo", default=default)

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)
    assert plug.asDouble() == pytest.approx(default)


@pytest.mark.parametrize(
    ("attr_cls", "default"),
    [
        (Double2, (1.5, -2.4)),
        (Double3, (1.5, -2.4, 0.7)),
        (Double4, (1.5, -2.4, 0.7, 123)),
        (Distance2, (1.5, -2.4)),
        (Distance3, (1.5, -2.4, 0.7)),
        (Angle2, (1.5, -2.4)),
        (Angle3, (1.5, -2.4, 0.7)),
        (Angle4, (1.5, -2.4, 0.7, 123)),
        (Float2, (1.5, -2.4)),
        (Float3, (1.5, -2.4, 0.7)),
        (Color, (1.5, -2.4, 0.7)),
        (Long2, (1, -2)),
        (Long3, (1, -2, 0)),
        (Short2, (1, -2)),
        (Short3, (1, -2, 0)),
    ],
)
def test_create_numeric_compound(
    attr_cls: type[NumericCompoundAttribute],
    default: tuple,
    network_node: OpenMaya.MFnDependencyNode,
) -> None:
    attribute = attr_cls("foo", default=default)

    modifier = OpenMaya.MDGModifier()
    plug = add_attribute(network_node, attribute, modifier)

    assert plug.isCompound
    assert plug.numChildren() == len(default)

    children: list[OpenMaya.MPlug] = [plug.child(i) for i in range(plug.numChildren())]
    assert tuple(c.asDouble() for c in children) == pytest.approx(default)
