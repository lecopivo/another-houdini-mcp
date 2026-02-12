"""Shared helpers for HDA resolution and parameter-template conversion."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


def resolve_hda_definition(params: Dict[str, Any], hou) -> Tuple[Optional[Any], Any]:
    """Resolve (optional node, required definition) from node_path/type/definition."""
    node_path = params.get("node_path")
    type_name = params.get("type_name") or params.get("definition_name")

    if node_path:
        node = hou.node(node_path)
        if node is None:
            raise ValueError(f"Node not found: {node_path}")
        definition = node.type().definition()
        if definition is None:
            raise ValueError(f"Node is not an HDA instance: {node_path}")
        return node, definition

    if not type_name:
        raise ValueError("Provide either node_path or type_name/definition_name")

    node_type = find_node_type(type_name, hou)
    if node_type is None:
        raise ValueError(f"HDA type not found: {type_name}")

    definition = node_type.definition()
    if definition is None:
        raise ValueError(f"Node type has no HDA definition: {type_name}")

    return None, definition


def find_node_type(type_name: str, hou):
    """Find node type by bare name, category-qualified name, or case-insensitive match."""
    wanted = str(type_name)
    for category in hou.nodeTypeCategories().values():
        node_types = category.nodeTypes()
        direct = node_types.get(wanted)
        if direct is not None:
            return direct
        for candidate_name, candidate in node_types.items():
            if candidate_name.lower() == wanted.lower():
                return candidate
            try:
                if candidate.nameWithCategory() == wanted:
                    return candidate
            except Exception:
                pass
    return None


def parm_template_to_dict(template, hou) -> Dict[str, Any]:
    """Serialize a parm template tree for transport/debugging."""
    data = {
        "name": template.name(),
        "label": template.label(),
        "type": template.type().name(),
    }

    if hasattr(template, "numComponents"):
        try:
            data["num_components"] = template.numComponents()
        except Exception:
            pass

    if hasattr(template, "defaultValue"):
        try:
            default = template.defaultValue()
            if isinstance(default, tuple) and len(default) == 1:
                data["default_value"] = default[0]
            else:
                data["default_value"] = default
        except Exception:
            pass

    if template.type() == hou.parmTemplateType.Folder:
        children = []
        for child in template.parmTemplates():
            children.append(parm_template_to_dict(child, hou))
        data["children"] = children
        try:
            data["folder_type"] = template.folderType().name()
        except Exception:
            pass
        return data

    if hasattr(template, "menuItems"):
        try:
            data["menu_items"] = list(template.menuItems())
            data["menu_labels"] = list(template.menuLabels())
        except Exception:
            pass

    for key, fn_name in (
        ("min", "minValue"),
        ("max", "maxValue"),
        ("min_is_strict", "minIsStrict"),
        ("max_is_strict", "maxIsStrict"),
    ):
        fn = getattr(template, fn_name, None)
        if callable(fn):
            try:
                data[key] = fn()
            except Exception:
                pass

    return data


def create_parm_template_from_tree(spec: Dict[str, Any], hou):
    """Create hou.ParmTemplate from a dictionary tree."""
    if not isinstance(spec, dict):
        raise ValueError("Template spec must be a dictionary")

    kind = str(spec.get("type", "Float")).lower()
    name = spec.get("name")
    label = spec.get("label", name)
    if not name:
        raise ValueError("Template spec requires 'name'")

    def _components(default: Any, fallback: int = 1):
        comps = int(spec.get("num_components", fallback))
        if isinstance(default, (list, tuple)):
            vals = tuple(default)
            if len(vals) == comps:
                return comps, vals
            if len(vals) == 1:
                return comps, tuple(vals[0] for _ in range(comps))
            raise ValueError(
                f"default_value length mismatch for '{name}': expected {comps}, got {len(vals)}"
            )
        return comps, tuple(default for _ in range(comps))

    if kind == "folder":
        folder = hou.FolderParmTemplate(name, label)
        for child in spec.get("children", []) or spec.get("templates", []):
            folder.addParmTemplate(create_parm_template_from_tree(child, hou))
        return folder

    if kind in ("float", "floattuple"):
        comps, default = _components(spec.get("default_value", 0.0), 1)
        template = hou.FloatParmTemplate(name, label, comps, default_value=default)
    elif kind in ("int", "inttuple"):
        comps, default = _components(spec.get("default_value", 0), 1)
        template = hou.IntParmTemplate(name, label, comps, default_value=tuple(int(v) for v in default))
    elif kind in ("string", "stringtuple"):
        comps, default = _components(spec.get("default_value", ""), 1)
        template = hou.StringParmTemplate(name, label, comps, default_value=tuple(str(v) for v in default))
    elif kind == "toggle":
        template = hou.ToggleParmTemplate(name, label, bool(spec.get("default_value", False)))
    elif kind == "button":
        template = hou.ButtonParmTemplate(name, label)
    elif kind == "menu":
        items = [str(v) for v in spec.get("menu_items", spec.get("menu_tokens", []))]
        labels = [str(v) for v in spec.get("menu_labels", items)]
        default = int(spec.get("default_value", 0))
        template = hou.MenuParmTemplate(name, label, menu_items=items, menu_labels=labels, default_value=default)
    else:
        raise ValueError(f"Unsupported template type: {spec.get('type')}")

    if hasattr(template, "setMinValue") and "min" in spec:
        template.setMinValue(float(spec["min"]))
    if hasattr(template, "setMaxValue") and "max" in spec:
        template.setMaxValue(float(spec["max"]))
    if hasattr(template, "setMinIsStrict") and "min_is_strict" in spec:
        template.setMinIsStrict(bool(spec["min_is_strict"]))
    if hasattr(template, "setMaxIsStrict") and "max_is_strict" in spec:
        template.setMaxIsStrict(bool(spec["max_is_strict"]))

    return template


def geometry_stats(node, hou) -> Dict[str, Any]:
    """Return basic geometry stats from a node or its display/render SOP."""
    probe = node
    for candidate in (node, getattr(node, "displayNode", lambda: None)(), getattr(node, "renderNode", lambda: None)()):
        if candidate is None:
            continue
        geo_fn = getattr(candidate, "geometry", None)
        if not callable(geo_fn):
            continue
        try:
            geo = geo_fn()
            probe = candidate
            break
        except Exception:
            continue
    else:
        raise ValueError(f"Node has no cookable geometry: {node.path()}")

    geo = probe.geometry()
    point_attrs = [a.name() for a in geo.pointAttribs()]
    prim_attrs = [a.name() for a in geo.primAttribs()]
    detail_attrs = [a.name() for a in geo.globalAttribs()]
    return {
        "points": len(geo.points()),
        "prims": len(geo.prims()),
        "vertices": len(geo.vertices()),
        "point_attributes": point_attrs,
        "prim_attributes": prim_attrs,
        "detail_attributes": detail_attrs,
    }
