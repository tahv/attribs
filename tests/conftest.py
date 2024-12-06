from __future__ import annotations

from typing import TYPE_CHECKING, Generator

import pytest

from tests.test_attributes import cast

if TYPE_CHECKING:
    from maya.api import OpenMaya


@pytest.fixture(scope="session", autouse=True)
def initialize_maya_session() -> Generator[None, None, None]:
    """Initialize Maya standalone."""
    import maya.standalone

    maya.standalone.initialize()

    yield

    maya.standalone.uninitialize()


@pytest.fixture(autouse=True)
def new_maya_scene() -> None:
    """Create a new file and restore default FBX options before each test."""
    from maya import cmds

    cmds.file(new=True, force=True)  # type: ignore[call-arg]


@pytest.fixture
def network_node() -> Generator[OpenMaya.MFnDependencyNode, None, None]:
    """Create a `network` node for the duration of the test."""
    from maya.api import OpenMaya

    modifier = OpenMaya.MDGModifier()
    node = _create_dependency_node("network", modifier)

    yield OpenMaya.MFnDependencyNode(node)

    modifier.deleteNode(node)
    modifier.doIt()


def _create_dependency_node(
    node_type: str,
    modifier: OpenMaya.MDGModifier,
    *,
    name: str | None = None,
) -> OpenMaya.MObject:
    from maya.api import OpenMaya

    node_mob = cast(OpenMaya.MObject, modifier.createNode(node_type))
    if name is not None:
        modifier.renameNode(node_mob, name)
    modifier.doIt()
    return node_mob


def _create_dag_node(
    node_type: str,
    modifier: OpenMaya.MDagModifier,
    *,
    name: str | None = None,
    parent: OpenMaya.MObject | None = None,
) -> OpenMaya.MObject:
    from maya.api import OpenMaya

    args = [node_type, parent] if parent is not None else [node_type]
    node_mob = cast(OpenMaya.MObject, modifier.createNode(*args))
    if name is not None:
        modifier.renameNode(node_mob, name)
    modifier.doIt()
    # TODO: If a shape gets created, this return the shape, not the transform.
    return node_mob
