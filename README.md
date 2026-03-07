# parapilot

**English** | [한국어](README.ko.md)

> Headless CAE/CFD post-processing for AI terminals. No ParaView. No GUI.

[![CI](https://github.com/kimimgo/parapilot/actions/workflows/ci.yml/badge.svg)](https://github.com/kimimgo/parapilot/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/kimimgo/parapilot/branch/main/graph/badge.svg)](https://codecov.io/gh/kimimgo/parapilot)
[![PyPI](https://img.shields.io/pypi/v/mcp-server-parapilot)](https://pypi.org/project/mcp-server-parapilot/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-server-parapilot)](https://pypi.org/project/mcp-server-parapilot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/kimimgo/parapilot/blob/main/LICENSE)

![DrivAerML Automotive CFD](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/drivaerml_cp.webp)

## Quick Start

**Claude Code plugin:**

```bash
claude install kimimgo/parapilot
```

Then in a conversation:

> "Render the pressure field from cavity/cavity.foam with a jet colormap"

**pip:**

```bash
pip install mcp-server-parapilot
```

**Docker (GPU headless):**

```bash
docker compose up -d
```

Requires NVIDIA Container Toolkit. For CPU-only: `docker compose up parapilot-cpu -d`

**MCP config for Cursor / other clients:**

```json
{
  "mcpServers": {
    "parapilot": {
      "command": "mcp-server-parapilot"
    }
  }
}
```

## What You Get

- **Headless Rendering** — EGL/OSMesa off-screen rendering.
  No display, no GUI, no ParaView install needed.

- **18 MCP Tools** — inspect, render, slice, contour, clip, streamlines,
  cinematic render, compare, animate, extract stats, and more.

- **50+ Formats** — OpenFOAM, VTK, CGNS, STL, PLY, OBJ, Exodus, Ensight
  via VTK readers + meshio.

## See It In Action

All renders from single MCP tool calls — no post-processing.

| | | |
|---|---|---|
| ![Automotive CFD](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/drivaerml_cp.webp) | ![Medical CT](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/ct_head_contour.webp) | ![Blood Flow](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/streamlines.webp) |
| Automotive CFD | Medical CT | Blood flow |
| ![HVAC](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/office_flow.webp) | ![Structural FEA](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/arch_structural.webp) | ![Stanford Dragon](https://raw.githubusercontent.com/kimimgo/parapilot/main/www/public/showcase/dragon.webp) |
| HVAC airflow | Structural FEA | Stanford Dragon |

[Full Gallery →](https://kimimgo.github.io/parapilot)

## vs Alternatives

| Feature | parapilot | ParaView (pvpython) | PyVista | VTK Python |
|---------|-----------|---------------------|---------|------------|
| MCP Integration | Native 18 tools | — | — | — |
| Headless | EGL/OSMesa | pvpython | Yes | Manual |
| Docker | GPU + CPU | Complex | — | — |
| Natural Language | AI-first | — | — | — |
| File Formats | 50+ (meshio) | 70+ | 30+ | ~20 |
| Installation | pip install | System package | pip install | pip install |
| Tests | 1134 (99% cov) | N/A | Yes | N/A |

## Contributing

```bash
git clone https://github.com/kimimgo/parapilot
cd parapilot && pip install -e ".[dev]"
pytest  # 1134 tests, 99% coverage
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
