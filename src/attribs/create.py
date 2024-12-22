from __future__ import annotations

from typing import cast

from maya.api import OpenMaya

from attribs.attributes import (
    Bool,
    Color,
    Compound,
    DoubleMatrix,
    Enum,
    FloatMatrix,
    String,
)
from attribs.base import Attribute, NumericAttribute, NumericCompoundAttribute


class LockedNodeError(Exception):
    """Raised when an operation is requested on a locked node."""


def add_attribute(
    node: OpenMaya.MFnDependencyNode,
    attribute: Attribute,
    modifier: OpenMaya.MDGModifier,
) -> OpenMaya.MPlug:
    """Add ``attribute`` to ``node`` and returns it as a `OpenMaya.MPlug`."""
    if node.isLocked:
        raise LockedNodeError(node.uniqueName())

    modifier.addAttribute(node.object(), create_mobject(attribute))
    modifier.doIt()

    # TODO: Attribute.locked property
    stack = [attribute]
    while stack:
        current = stack.pop()
        plug = cast(OpenMaya.MPlug, node.findPlug(current.name, False))  # noqa: FBT003
        plug.isLocked = getattr(current, "locked", False)
        stack.extend(getattr(current, "children", []))

    plug = cast(OpenMaya.MPlug, node.findPlug(attribute.name, False))  # noqa: FBT003

    if isinstance(attribute, (DoubleMatrix, FloatMatrix)):
        value = OpenMaya.MFnMatrixData().create(attribute.default)
        modifier.newPlugValue(plug, value)
        modifier.doIt()

    return plug


def create_mobject(attribute: Attribute) -> OpenMaya.MObject:  # noqa: C901
    """Create a mobject from ``attribute``."""
    mfn = attribute.MFN_CLS()

    mobject: OpenMaya.MObject = mfn.create(*get_mfn_args(attribute))  # type: ignore[attr-defined]

    mfn.keyable = attribute.keyable
    mfn.channelBox = attribute.channel_box
    mfn.hidden = attribute.hidden
    mfn.storable = attribute.storable
    mfn.connectable = attribute.connectable
    mfn.readable = attribute.readable
    mfn.writable = attribute.writable
    # TODO: mfn.array = attribute.array
    mfn.disconnectBehavior = attribute.disconnect_behavior

    if isinstance(attribute, NumericAttribute):
        mfn = cast(OpenMaya.MFnNumericAttribute, mfn)
        if attribute.min is not None:
            mfn.setMin(attribute.min)
        if attribute.max is not None:
            mfn.setMax(attribute.max)
        if attribute.soft_min is not None:
            mfn.setSoftMin(attribute.soft_min)
        if attribute.soft_max is not None:
            mfn.setSoftMax(attribute.soft_max)

    if isinstance(attribute, Enum):
        mfn = cast(OpenMaya.MFnEnumAttribute, mfn)
        for index, field in attribute.fields.items():
            mfn.addField(field, index)

    elif isinstance(attribute, String):
        mfn.usedAsFilename = attribute.as_filename

    elif isinstance(attribute, Color):
        mfn.usedAsColor = True

    elif isinstance(attribute, Compound):
        mfn = cast(OpenMaya.MFnCompoundAttribute, mfn)
        for child in attribute.children:
            mfn.addChild(create_mobject(child))

    return mobject


def get_mfn_args(attribute: Attribute) -> list:
    """Returns the list of arguments to pass to `OpenMaya.MFnAttibute.create`."""
    args: list = [attribute.name, attribute.short_name or attribute.name]

    if isinstance(attribute, NumericCompoundAttribute):
        args.extend(create_mobject(c) for c in attribute.children)
        return args

    if attribute.DATA_TYPE != OpenMaya.MFnData.kInvalid:  # noqa: SIM300
        args.append(attribute.DATA_TYPE)

    if isinstance(attribute, (Bool, Enum)):
        args.append(attribute.default)

    elif isinstance(attribute, String):
        string = OpenMaya.MFnStringData()
        default = cast(OpenMaya.MObject, string.create())
        string.set(attribute.default)
        args.append(default)

    elif isinstance(attribute, NumericAttribute) and attribute.default is not None:
        default = attribute.default
        default = getattr(default, "asUnits", lambda _: default)(attribute.unit)
        args.append(default)

    # NOTE: Matrix also have a `default` property,
    # but `OpenMaya.MFnMatrixAttribute.create`
    # doesn't accept a `default` argument.
    # It must be set after the attribute is created.

    return args
