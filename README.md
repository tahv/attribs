# attribs

An experimental Python library for creating Maya Attributes.

## Installation

Install attribs with pip:

```bash
pip install maya-attribs
```

## Quickstart

Use `attribs.add_attribute` to create an new attributes
on an `OpenMaya.MFnDependencyNode`.
This function also returns the newly created `OpenMaya.MPlug`.

```python
from maya import cmds
from maya.api import OpenMaya
import attribs

def create_node(node_type: str) -> OpenMaya.MObject:
    name = cmds.createNode(node_type)
    return OpenMaya.MSelectionList().add(name).getDependNode(0)

node = OpenMaya.MFnDependencyNode(create_node("transform"))
modifier = OpenMaya.MDGModifier()

attribute = attribs.Bool("foo", default=False)

plug = attribs.add_attribute(node, attribute, modifier=modifier)
```

Set attribute flags either as keyword argument or later as properties.

```python
from maya import cmds
from maya.api import OpenMaya
import attribs

def create_node(node_type: str) -> OpenMaya.MObject:
    name = cmds.createNode(node_type)
    return OpenMaya.MSelectionList().add(name).getDependNode(0)

node = OpenMaya.MFnDependencyNode(create_node("transform"))
modifier = OpenMaya.MDGModifier()

attribute = attribs.Double3(
    "MyDouble", 
    default=(1.0, 2.0, 3.0), 
    channel_box=True,
)
attribute.keyable = True

plug = attribs.add_attribute(node, attribute, modifier=modifier)
```

Compounds are also supported.

```python
from maya import cmds
from maya.api import OpenMaya
import attribs

def create_node(node_type: str) -> OpenMaya.MObject:
    name = cmds.createNode(node_type)
    return OpenMaya.MSelectionList().add(name).getDependNode(0)

node = OpenMaya.MFnDependencyNode(create_node("transform"))
modifier = OpenMaya.MDGModifier()

attribute = attribs.Compound("foo")
attribute.append(attribs.Bool("bar"))
attribute.append(attribs.String("baz"))

plug = attribs.add_attribute(node, attribute, modifier=modifier)
```
