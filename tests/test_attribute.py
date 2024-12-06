from __future__ import annotations

import pytest
from maya.api import OpenMaya

from attribs.base import Attribute


@pytest.mark.parametrize(
    ("attr", "expected"),
    [
        ("affects_appearence", False),
        ("affects_world_space", False),
        ("cached", True),
        ("channel_box", False),
        ("connectable", True),
        ("disconnect_behavior", OpenMaya.MFnAttribute.kNothing),
        ("hidden", False),
        ("indeterminant", False),
        ("index_matters", True),
        ("internal", False),
        ("keyable", False),
        ("readable", True),
        ("render_source", False),
        ("storable", True),
        ("writable", True),
    ],
)
def test_attribute_defaults(attr: str, expected: object) -> None:
    assert getattr(Attribute("foo"), attr) == expected
