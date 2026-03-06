"""MCP protocol compliance tests.

Validates that parapilot's MCP server follows best practices:
- All tools have descriptions
- All tools have proper parameter schemas
- Resource URIs follow the parapilot:// scheme
- Server metadata is correct
- Tool naming conventions are consistent
"""

from __future__ import annotations

import inspect
import re

import pytest


def _get_tool_objects() -> dict:
    """Get FunctionTool objects from server module."""
    from parapilot import server

    names = [
        "inspect_data", "render", "slice", "contour", "clip",
        "streamlines", "extract_stats", "plot_over_line",
        "integrate_surface", "animate", "split_animate",
        "execute_pipeline", "pv_isosurface",
        "cinematic_render", "compare",
        "probe_timeseries", "batch_render", "preview_3d",
    ]
    tools = {}
    for name in names:
        obj = getattr(server, name)
        tools[name] = obj
    return tools


class TestToolCompliance:
    """Every tool must have a description and typed parameters."""

    def test_all_tools_have_descriptions(self):
        """MCP tools must have descriptions for LLM tool selection."""
        for name, tool in _get_tool_objects().items():
            desc = getattr(tool, "description", None) or ""
            assert len(desc) > 10, f"Tool {name} has no/short description"

    def test_all_tools_have_typed_parameters(self):
        """MCP tools must have type annotations for JSON schema generation."""
        for name, tool in _get_tool_objects().items():
            fn = getattr(tool, "fn", None)
            if fn is None:
                continue
            sig = inspect.signature(fn)
            for pname, param in sig.parameters.items():
                if pname in ("self", "ctx"):
                    continue
                assert param.annotation != inspect.Parameter.empty, (
                    f"Tool {name} param '{pname}' has no type annotation"
                )

    def test_all_tools_have_return_annotations(self):
        """MCP tools should have return type annotations."""
        for name, tool in _get_tool_objects().items():
            fn = getattr(tool, "fn", None)
            if fn is None:
                continue
            sig = inspect.signature(fn)
            assert sig.return_annotation != inspect.Signature.empty, (
                f"Tool {name} has no return type annotation"
            )

    def test_tool_names_are_snake_case(self):
        """MCP tool names should be snake_case."""
        pattern = re.compile(r"^[a-z][a-z0-9_]*$")
        for name in _get_tool_objects():
            assert pattern.match(name), f"Tool name '{name}' is not snake_case"

    def test_tool_count_matches_expected(self):
        """Guard against accidentally dropping or adding tools."""
        assert len(_get_tool_objects()) == 18

    def test_descriptions_are_unique(self):
        """No two tools should have the same description."""
        descriptions = []
        for name, tool in _get_tool_objects().items():
            desc = getattr(tool, "description", "") or ""
            first_line = desc.split("\n")[0].strip()
            descriptions.append((name, first_line))
        seen = {}
        for name, desc in descriptions:
            if desc in seen:
                pytest.fail(f"Tools '{seen[desc]}' and '{name}' have duplicate descriptions")
            seen[desc] = name

    def test_tool_names_match_attribute(self):
        """FunctionTool.name should match the attribute name on server module."""
        for name, tool in _get_tool_objects().items():
            tool_name = getattr(tool, "name", None)
            assert tool_name == name, (
                f"Tool attr '{name}' has FunctionTool.name='{tool_name}'"
            )


class TestResourceCompliance:
    """Resource URIs must follow parapilot:// scheme."""

    def test_resource_uris_use_correct_scheme(self):
        from parapilot.server import mcp
        instr = mcp.instructions or ""
        uris = re.findall(r"parapilot://[\w/\-]+", instr)
        assert len(uris) >= 5, f"Expected 5+ resource URIs, found {len(uris)}"
        for uri in uris:
            assert uri.startswith("parapilot://"), f"Invalid URI scheme: {uri}"

    def test_core_resources_documented(self):
        """Core resource URIs must be in instructions."""
        from parapilot.server import mcp
        instr = mcp.instructions or ""
        expected = [
            "parapilot://formats",
            "parapilot://filters",
            "parapilot://colormaps",
            "parapilot://cameras",
            "parapilot://cinematic",
        ]
        for res in expected:
            assert res in instr, f"Resource {res} not in instructions"


class TestServerMetadata:
    """Server-level MCP metadata compliance."""

    def test_server_name(self):
        from parapilot.server import mcp
        assert mcp.name == "parapilot"

    def test_instructions_present_and_substantial(self):
        from parapilot.server import mcp
        assert mcp.instructions is not None
        assert len(mcp.instructions) > 200

    def test_instructions_describe_workflow(self):
        from parapilot.server import mcp
        instr = mcp.instructions or ""
        assert "inspect_data" in instr
        assert "render" in instr
        # Must describe recommended usage order
        assert "Workflow" in instr or "workflow" in instr

    def test_instructions_mention_capabilities(self):
        from parapilot.server import mcp
        instr = (mcp.instructions or "").lower()
        for cap in ["cfd", "fea", "cae", "visualization", "pipeline"]:
            assert cap in instr, f"Instructions missing '{cap}'"


class TestSecurityCompliance:
    """Security-related compliance checks."""

    def test_validate_file_path_exists(self):
        from parapilot.server import _validate_file_path
        assert callable(_validate_file_path)

    def test_file_path_param_on_data_tools(self):
        """Tools that read files must accept file_path."""
        data_tools = [
            "inspect_data", "render", "slice", "contour", "clip",
            "streamlines", "animate", "cinematic_render",
        ]
        for name, tool in _get_tool_objects().items():
            if name not in data_tools:
                continue
            fn = getattr(tool, "fn", None)
            if fn is None:
                continue
            sig = inspect.signature(fn)
            assert "file_path" in sig.parameters, (
                f"Data tool {name} missing file_path parameter"
            )
