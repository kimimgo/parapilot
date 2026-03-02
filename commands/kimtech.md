Use the kimtech plugin to post-process simulation results.

Usage:
  /kimtech render <file> <field>    — Render a field visualization
  /kimtech inspect <file>           — Inspect simulation data
  /kimtech mesh <file>              — Check mesh quality
  /kimtech report <case_dir>        — Generate post-processing report

Examples:
  /kimtech render cavity.foam pressure
  /kimtech inspect results/case.vtk
  /kimtech mesh part.stl
  /kimtech report ./openfoam_case/
