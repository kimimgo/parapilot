"""Tests for resources/catalog.py — MCP resource registration."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from parapilot.resources.catalog import register_resources


def _capture_resources():
    """Register resources with a mock and return name→function mapping."""
    mcp = MagicMock()
    captured = {}

    def resource_decorator(uri):
        def wrapper(fn):
            captured[uri] = fn
            return fn
        return wrapper

    mcp.resource = resource_decorator
    register_resources(mcp)
    return captured


class TestResourceRegistration:
    def test_all_resources_registered(self):
        resources = _capture_resources()
        expected = {
            "parapilot://formats",
            "parapilot://filters",
            "parapilot://colormaps",
            "parapilot://representations",
            "parapilot://case-presets",
            "parapilot://cameras",
            "parapilot://cinematic",
            "parapilot://pipelines/cfd",
            "parapilot://pipelines/fea",
            "parapilot://pipelines/split-animate",
            "parapilot://physics-defaults",
        }
        assert expected.issubset(set(resources.keys()))


class TestFormatsResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        result = resources["parapilot://formats"]()
        data = json.loads(result)
        assert isinstance(data, dict)
        assert ".vtk" in data or ".vtu" in data

    def test_entries_have_reader(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://formats"]())
        for ext, info in data.items():
            assert "reader" in info


class TestFiltersResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        result = resources["parapilot://filters"]()
        data = json.loads(result)
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_entries_have_vtk_class(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://filters"]())
        for name, info in data.items():
            assert "vtk_class" in info


class TestCasePresetsResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://case-presets"]())
        assert isinstance(data, dict)
        assert len(data) > 0


class TestCamerasResource:
    def test_has_presets_and_auto_camera(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://cameras"]())
        assert "presets" in data
        assert "auto_camera" in data
        assert "custom" in data


class TestCinematicResource:
    def test_has_all_sections(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://cinematic"]())
        assert "lighting_presets" in data
        assert "material_presets" in data
        assert "background_presets" in data
        assert "quality_presets" in data


class TestPipelineResources:
    def test_cfd_pipelines(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://pipelines/cfd"]())
        assert "pressure_distribution" in data
        assert "velocity_slice" in data
        assert "streamlines" in data

    def test_fea_pipelines(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://pipelines/fea"]())
        assert "deformation" in data
        assert "stress_threshold" in data

    def test_split_animate_pipelines(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://pipelines/split-animate"]())
        assert "dual_field_comparison" in data


class TestPhysicsDefaultsResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://physics-defaults"]())
        assert isinstance(data, dict)
        assert "_usage" in data

    def test_has_known_physics(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://physics-defaults"]())
        keys = set(data.keys())
        # Should detect at least pressure, velocity, temperature
        assert "pressure" in keys or "Pressure" in keys


class TestColormapsResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://colormaps"]())
        assert isinstance(data, dict)
        assert "colormaps" in data
        assert "field_recommendations" in data
        assert len(data["colormaps"]) >= 16

    def test_field_recommendations_reference_valid_colormaps(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://colormaps"]())
        guide_names = {k.lower() for k in data["colormaps"]}
        for field, cmap in data["field_recommendations"].items():
            if field.startswith("_"):
                continue
            assert cmap.lower() in guide_names, f"{field} → {cmap} not in guide"


class TestRepresentationsResource:
    def test_returns_valid_json(self):
        resources = _capture_resources()
        data = json.loads(resources["parapilot://representations"]())
        assert isinstance(data, dict)
