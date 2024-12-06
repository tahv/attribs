from __future__ import annotations

import sys
from typing import (
    ClassVar,
    Generic,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from maya.api import OpenMaya

if sys.version_info < (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict


MayaNumeric = Union[float, OpenMaya.MAngle, OpenMaya.MDistance, OpenMaya.MTime]
NT = TypeVar("NT", bound=MayaNumeric)
UT = TypeVar("UT", bound=Union[int, None])


NCA = TypeVar(
    "NCA",
    bound=(
        Union[
            Tuple[
                "NumericAttribute",
                "NumericAttribute",
            ],
            Tuple[
                "NumericAttribute",
                "NumericAttribute",
                "NumericAttribute",
            ],
            Tuple[
                "NumericAttribute",
                "NumericAttribute",
                "NumericAttribute",
                "NumericAttribute",
            ],
        ]
    ),
)
"""Children type of NumericCompound."""

NCGT = TypeVar(
    "NCGT",
    bound=(
        Union[
            Tuple[
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
            ],
            Tuple[
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
            ],
            Tuple[
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
                Union[MayaNumeric, None],
            ],
        ]
    ),
)
"""NumericCompound getter type."""

NCST = TypeVar(
    "NCST",
    bound=(
        Union[
            Tuple[
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
            ],
            Tuple[
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
            ],
            Tuple[
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
                Union[MayaNumeric, float, None],
            ],
        ]
    ),
)
"""NumericCompound setter Type."""

GT = TypeVar("GT")
"""Generic getter type for NumericCompoundProperty."""

ST = TypeVar("ST")
"""Generic setter type for NumericCompoundProperty."""


class AttributeKwargs(TypedDict, total=False):
    """`Attribute` keyword arguments."""

    affects_appearence: bool
    affects_world_space: bool
    # TODO: array: bool = False
    cached: bool
    short_name: str
    channel_box: bool
    connectable: bool
    # TODO: dynamic (read only property)
    # TODO: extension (read only property)
    disconnect_behavior: Literal[0, 1, 2]
    hidden: bool
    indeterminant: bool
    index_matters: bool
    internal: bool  # TODO: more doc
    # TODO: is_proxy_attribute
    keyable: bool
    # TODO: self.parent = parent
    readable: bool
    render_source: bool  # TODO: more doc
    storable: bool
    # TODO: used_as_color: in Color attribute
    # TODO: uses_array_data_builder: bool = False (in Array attr)
    # TODO: world_space - on array ?
    writable: bool


class Attribute:
    """Attributes base class.

    Child class must implement `MFN_CLS` and `DATA_TYPE`.
    """

    MFN_CLS: ClassVar[type[OpenMaya.MFnAttribute]] = OpenMaya.MFnAttribute
    DATA_TYPE: ClassVar[int] = OpenMaya.MFnData.kInvalid

    def __init__(self, name: str, **kwargs: Unpack[AttributeKwargs]) -> None:
        self.name = name

        self.short_name: str | None = kwargs.pop("short_name", None)
        """Attribute short name.

        If the attribute has no short name then its long name will be used.
        """

        self.affects_appearence: bool = kwargs.pop("affects_appearence", False)
        """Attribute affects appearence of object when rendered in viewport."""

        self.affects_world_space: bool = kwargs.pop("affects_world_space", False)
        """Attribute affects the node world space matrix. DAG nodes only."""

        # TODO: array: bool = False

        self.cached: bool = kwargs.pop("cached", True)
        """Should this attribute value be cached locally in the node data block.

        Caching a node locally causes a copy of the attribute value
        for the node to be cached with the node.
        This removes the need to traverse through the graph
        to get the value each time it is requested.

        Caching give a speed increase at the cost of more memory.
        """

        self.channel_box: bool = kwargs.pop("channel_box", False)
        """Should the attribute appear in the channel box when the node is selected.

        Attributes will appear in the channel box if their `channel_box` flag is set
        or if they are `keyable`.
        """

        self.connectable: bool = kwargs.pop("connectable", True)
        """Should this attribute allow dependency graph connections.

        If the attribute is `connectable`, the `readable` and `writable` properties
        will indicate what types of connections are accepted.
        """

        self.disconnect_behavior: Literal[0, 1, 2] = kwargs.pop(
            "disconnect_behavior",
            OpenMaya.MFnAttribute.kNothing,  # type: ignore[typeddict-item]
        )  # type: ignore[assignment]
        """Behavior when this attribute gets disconnected.

        Possible values:
            - ``OpenMaya.MFnAttribute.kDelete`` (``0``):
                Delete array element (`array` attributes only).
            - ``OpenMaya.MFnAttribute.kReset`` (``1``):
                Reset the attribute to its default value.
            - ``OpenMaya.MFnAttribute.kNothing`` (``2``):
                Do nothing to the attribute value.
        """

        self.hidden: bool = kwargs.pop("hidden", False)
        """Should this attribute not be displayed in the Attribute Editor."""

        self.indeterminant: bool = kwargs.pop("indeterminant", False)
        """Whether the attribute may be used during evaluation.

        This attribute may not always be used when computing the attributes which
        are dependent upon it.

        This property is mainly used on rendering nodes to indicate that some
        attribute are not always used.
        """

        self.index_matters: bool = kwargs.pop("index_matters", True)
        """Whether the user must specify an index when connecting to this attribute.

        - If `False`, ``connectAttr -nextAvailable`` can be used with this attribute.
        - If `True`, then an explicit index must be provided.

        If the destination attribute has set the indexMatters to be False with
        this flag specified, a connection is made to the next available index,
        no index need be specified.

        This only affect array attributes which are not `readable`,
        like destination attributes.
        """

        self.internal: bool = kwargs.pop("internal", False)
        """Will the node handle the attribute data storage itself,
        outside of the node data block.
        """

        # TODO: is_proxy_attribute

        self.keyable: bool = kwargs.pop("keyable", False)
        """Keys can be set on the attribute."""

        # TODO: self.parent = parent

        self.readable: bool = kwargs.pop("readable", True)
        """Attribute can be used as the source in a dependency graph connection."""

        self.render_source: bool = kwargs.pop("render_source", False)
        """Attribute is used on rendering nodes to override rendering sampler info."""

        self.storable: bool = kwargs.pop("storable", True)
        """Should the attribute value be stored when the node is written to file."""

        # TODO: used_as_color: in Color attribute
        # TODO: used_as_filename: in FIleName attribute
        # TODO: uses_array_data_builder: bool = False (in Array attr)
        # TODO: world_space - on array ?

        self.writable: bool = kwargs.pop("writable", True)
        """Is the attribute writable.

        If an attribute is writable, then it can be used as the destination in
        a dependency graph connection.
        """


class MatrixProperty:
    """Matrix property."""

    def __init__(self) -> None:
        self._default: OpenMaya.MMatrix = OpenMaya.MMatrix.kIdentity

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name

    @overload
    def __get__(self, obj: None, objtype: None) -> None: ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> OpenMaya.MMatrix: ...

    def __get__(
        self,
        obj: object | None,
        objtype: type[object] | None = None,
    ) -> OpenMaya.MMatrix | None:
        return obj.__dict__.get(self.name, self._default)  # type: ignore[no-any-return]

    def __set__(
        self,
        obj: object,
        value: Sequence[float] | OpenMaya.MMatrix | OpenMaya.MTransformationMatrix,
    ) -> None:
        if isinstance(value, Sequence):
            try:
                value = OpenMaya.MMatrix(value)
            except ValueError:
                if len(value) != 16:  # noqa: PLR2004
                    message = f"Expected 16 floats, got {len(value)}"
                    raise ValueError(message) from None
                raise
        elif isinstance(value, OpenMaya.MTransformationMatrix):
            value = value.asMatrix()
        if not isinstance(value, OpenMaya.MMatrix):
            raise TypeError(type(value))
        obj.__dict__[self.name] = value


class NumericProperty(Generic[NT]):
    """`NumericAttribute` property."""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name

    @overload
    def __get__(self, obj: None, objtype: None) -> None: ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> NT | None: ...

    def __get__(
        self,
        obj: object | None,
        objtype: type[object] | None = None,
    ) -> NT | None:
        return obj.__dict__.get(self.name)

    def __set__(self, obj: object, value: float | NT | None) -> None:
        if value is None:
            obj.__dict__[self.name] = None
            return

        numeric_cls = cast("type[NT]", getattr(obj, "NUMERIC_CLS", float))
        unit = cast("int | None", getattr(obj, "unit", None))

        if issubclass(numeric_cls, (float, int)):
            obj.__dict__[self.name] = numeric_cls(value)  # type: ignore[arg-type]
            return

        if not isinstance(value, numeric_cls):
            args = [unit] if unit is not None else []
            converted = numeric_cls(value, *args)
        elif unit is not None and value.unit != unit:
            converted = numeric_cls(value.asUnits(unit), unit)
        else:
            converted = value

        obj.__dict__[self.name] = converted


class NumericAttribute(Attribute, Generic[NT, UT]):
    """Base class for Maya Numeric Attributes.

    Child class must implement `MFN_CLS`, `DATA_TYPE`, `NUMERIC_CLS` and `DEFAULT_UNIT`.
    """

    NUMERIC_CLS: ClassVar[type[MayaNumeric]]
    DEFAULT_UNIT: ClassVar[int | None]

    default = NumericProperty[NT]()
    min = NumericProperty[NT]()
    max = NumericProperty[NT]()
    soft_min = NumericProperty[NT]()
    soft_max = NumericProperty[NT]()

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        *,
        default: NT | float | None = None,
        min: NT | float | None = None,  # noqa: A002
        max: NT | float | None = None,  # noqa: A002
        soft_min: NT | float | None = None,
        soft_max: NT | float | None = None,
        unit: UT | None = None,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)
        self.unit: UT = unit if unit is not None else self.DEFAULT_UNIT  # type: ignore[assignment]
        setattr(self, "default", default)  # noqa: B010
        setattr(self, "min", min)  # noqa: B010
        setattr(self, "max", max)  # noqa: B010
        setattr(self, "soft_min", soft_min)  # noqa: B010
        setattr(self, "soft_max", soft_max)  # noqa: B010


class NumericCompoundProperty(Generic[GT, ST]):
    """Attribute numeric compound property."""

    def __init__(self, child_attr: str | None = None) -> None:
        self._child_attr: str | None = child_attr

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name

    @property
    def child_attr(self) -> str:  # noqa: D102
        return self._child_attr or self.name

    def get_children(self, obj: object) -> tuple[NumericAttribute, ...]:  # noqa: D102
        return getattr(obj, "children", ())

    @overload
    def __get__(self, obj: None, objtype: None) -> None: ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> GT: ...

    def __get__(
        self,
        obj: object | None,
        objtype: type[object] | None = None,
    ) -> GT | None:
        result = []
        for c in self.get_children(obj):
            value = getattr(c, self.child_attr, None)
            result.append(value)
        return tuple(result)  # type: ignore[return-value]

    def __set__(self, obj: object, value: ST) -> None:
        backup: list[tuple[object, object]] = []

        children = self.get_children(obj)

        if value is None:
            value = tuple(None for _ in children)  # type: ignore[assignment]

        for child, val in zip(children, value):  # type: ignore[call-overload]
            bckp_val = getattr(child, self.child_attr)
            try:
                setattr(child, self.child_attr, val)
            except Exception:
                for backup_child, backup_value in backup:
                    setattr(backup_child, self.child_attr, backup_value)
                raise
            else:
                backup.append((child, bckp_val))


class NumericCompoundAttribute(Attribute, Generic[NCA, NCGT, NCST, UT]):
    """Base class for Maya Numeric Compound Attributes.

    Child class must implement `MFN_CLS`, `DATA_TYPE`, `CHILD_CLS`, `CHILD_SUFFIXES`
    and `DEFAULT_UNIT`.
    """

    CHILD_CLS: ClassVar[type[NumericAttribute]]
    CHILD_SUFFIXES: ClassVar[tuple[str, ...]]
    DEFAULT_UNIT: ClassVar[int | None]

    default = NumericCompoundProperty[NCGT, NCST]()
    min = NumericCompoundProperty[NCGT, NCST]()
    max = NumericCompoundProperty[NCGT, NCST]()
    soft_min = NumericCompoundProperty[NCGT, NCST]()
    soft_max = NumericCompoundProperty[NCGT, NCST]()

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        *,
        default: NCST | None = None,
        min: NCST | None = None,  # noqa: A002
        max: NCST | None = None,  # noqa: A002
        soft_min: NCST | None = None,
        soft_max: NCST | None = None,
        unit: UT | None = None,
        **kwargs: Unpack[AttributeKwargs],
    ) -> None:
        super().__init__(name, **kwargs)

        children: list[NumericAttribute] = []
        for s in self.CHILD_SUFFIXES:
            children.append(self.CHILD_CLS(f"{name}{s}"))  # noqa: PERF401
        self.children: NCA = tuple(children)  # type: ignore[assignment]

        self.unit: UT = unit if unit is not None else self.DEFAULT_UNIT  # type: ignore[assignment]
        setattr(self, "default", default)  # noqa: B010
        setattr(self, "min", min)  # noqa: B010
        setattr(self, "max", max)  # noqa: B010
        setattr(self, "soft_min", soft_min)  # noqa: B010
        setattr(self, "soft_max", soft_max)  # noqa: B010
