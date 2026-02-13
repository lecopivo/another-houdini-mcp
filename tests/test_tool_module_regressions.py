"""Regression tests for root tool_modules behaviors."""

from pathlib import Path
import sys
import types

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tool_modules.hda_utils import geometry_stats
import tool_modules.set_hda_parm_default as set_hda_parm_default_mod


class _Attr:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name


class _GeoWithVertexCount:
    def points(self):
        return [object()] * 3

    def prims(self):
        return [object()] * 2

    def vertexCount(self):
        return 9

    def pointAttribs(self):
        return [_Attr("P")]

    def primAttribs(self):
        return [_Attr("name")]

    def globalAttribs(self):
        return [_Attr("foo")]


class _GeoWithIntrinsicOnly:
    def points(self):
        return [object()]

    def prims(self):
        return [object()]

    def intrinsicValue(self, name):
        if name == "vertexcount":
            return 7
        raise KeyError(name)

    def pointAttribs(self):
        return []

    def primAttribs(self):
        return []

    def globalAttribs(self):
        return []


class _SopNode:
    def __init__(self, geo):
        self._geo = geo

    def geometry(self):
        return self._geo

    def path(self):
        return "/obj/test/OUT"


class _FakeTemplate:
    def __init__(self, parm_type, default_value, num_components=1, persist=True):
        self._parm_type = parm_type
        self._default_value = default_value
        self._num_components = num_components
        self._persist = persist

    def type(self):
        return self._parm_type

    def numComponents(self):
        return self._num_components

    def setDefaultValue(self, value):
        if self._persist:
            self._default_value = value

    def defaultValue(self):
        return self._default_value


class _FakeParmTemplateGroup:
    def __init__(self, templates):
        self._templates = dict(templates)

    def find(self, name):
        return self._templates.get(name)

    def replace(self, name, template):
        self._templates[name] = template


class _FakeDefinition:
    def __init__(self, ptg):
        self._ptg = ptg

    def parmTemplateGroup(self):
        return self._ptg

    def setParmTemplateGroup(self, ptg):
        self._ptg = ptg

    def nodeTypeName(self):
        return "fake::hda::1.0"


class _FakeNode:
    def __init__(self):
        self.synced = 0

    def matchCurrentDefinition(self):
        self.synced += 1


class _FakeHou:
    parmTemplateType = types.SimpleNamespace(
        Toggle="toggle",
        Menu="menu",
        Int="int",
        String="string",
    )


def test_geometry_stats_uses_vertex_count_when_vertices_missing():
    stats = geometry_stats(_SopNode(_GeoWithVertexCount()), _FakeHou())
    assert stats["points"] == 3
    assert stats["prims"] == 2
    assert stats["vertices"] == 9
    assert stats["point_attributes"] == ["P"]


def test_geometry_stats_falls_back_to_intrinsic_vertexcount():
    stats = geometry_stats(_SopNode(_GeoWithIntrinsicOnly()), _FakeHou())
    assert stats["vertices"] == 7


def test_set_hda_parm_default_raises_if_default_does_not_persist(monkeypatch):
    template = _FakeTemplate(
        parm_type="float",
        default_value=(0.0, 0.0, 0.0),
        num_components=3,
        persist=False,
    )
    definition = _FakeDefinition(_FakeParmTemplateGroup({"t": template}))
    node = _FakeNode()

    monkeypatch.setattr(
        set_hda_parm_default_mod,
        "resolve_hda_definition",
        lambda params, hou: (node, definition),
    )

    with pytest.raises(ValueError, match="did not persist"):
        set_hda_parm_default_mod.execute_plugin(
            {
                "node_path": "/obj/fake1",
                "param_name": "t",
                "default_value": "1.25",
                "sync_instance": True,
            },
            server=None,
            hou=_FakeHou(),
        )


def test_set_hda_parm_default_updates_editable_parm(monkeypatch):
    template = _FakeTemplate(
        parm_type="float",
        default_value=(0.0,),
        num_components=1,
        persist=True,
    )
    definition = _FakeDefinition(_FakeParmTemplateGroup({"scale": template}))
    node = _FakeNode()

    monkeypatch.setattr(
        set_hda_parm_default_mod,
        "resolve_hda_definition",
        lambda params, hou: (node, definition),
    )

    result = set_hda_parm_default_mod.execute_plugin(
        {
            "node_path": "/obj/fake1",
            "param_name": "scale",
            "default_value": "2.5",
            "sync_instance": True,
        },
        server=None,
        hou=_FakeHou(),
    )

    assert result["definition_name"] == "fake::hda::1.0"
    assert definition.parmTemplateGroup().find("scale").defaultValue() == (2.5,)
    assert node.synced == 1
