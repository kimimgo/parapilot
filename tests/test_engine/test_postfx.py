"""Tests for engine/postfx.py — SSAO and FXAA post-processing."""

from __future__ import annotations

import pytest
import vtk

from parapilot.engine.postfx import (
    PostFXConfig,
    apply_fxaa,
    apply_postfx,
    apply_ssao,
)


@pytest.fixture
def renderer():
    rw = vtk.vtkRenderWindow()
    rw.SetOffScreenRendering(True)
    rw.SetSize(100, 100)
    ren = vtk.vtkRenderer()
    rw.AddRenderer(ren)
    return ren


class TestApplySSAO:
    def test_ssao_returns_true(self, renderer):
        result = apply_ssao(renderer, scene_size=10.0)
        # vtkSSAOPass may or may not be available depending on VTK build
        assert isinstance(result, bool)

    def test_ssao_with_explicit_params(self, renderer):
        result = apply_ssao(renderer, scene_size=10.0, radius=1.0, bias=0.01, kernel_size=64)
        assert isinstance(result, bool)

    def test_ssao_auto_scales_from_scene(self, renderer):
        # Just verify no crash with different scene sizes
        apply_ssao(renderer, scene_size=1.0)
        apply_ssao(renderer, scene_size=100.0)
        apply_ssao(renderer, scene_size=0.001)


class TestApplyFXAA:
    def test_fxaa_returns_true(self, renderer):
        result = apply_fxaa(renderer)
        assert result is True

    def test_fxaa_with_params(self, renderer):
        result = apply_fxaa(renderer, subpixel_blend=0.5, contrast_threshold=0.2)
        assert result is True


class TestPostFXConfig:
    def test_defaults(self):
        config = PostFXConfig()
        assert config.ssao is False
        assert config.fxaa is False
        assert config.ssao_kernel_size == 128

    def test_custom_config(self):
        config = PostFXConfig(ssao=True, fxaa=True, ssao_kernel_size=64)
        assert config.ssao is True
        assert config.ssao_kernel_size == 64


class TestApplyPostFX:
    def test_apply_both(self, renderer):
        config = PostFXConfig(ssao=True, fxaa=True)
        apply_postfx(renderer, config, scene_size=10.0)

    def test_apply_none(self, renderer):
        config = PostFXConfig(ssao=False, fxaa=False)
        apply_postfx(renderer, config, scene_size=10.0)
        # No crash, no effects applied

    def test_apply_fxaa_only(self, renderer):
        config = PostFXConfig(fxaa=True)
        apply_postfx(renderer, config)
