# pyCircuit repo map for Linx bring-up (reference)

Evidence anchor: use `PYC-*` IDs in `references/evidence.md` when justifying repo structure decisions.

## Top-level entry points

- `python/pycircuit/`: Python DSL + frontend (`emit_mlir()`, CLI)
- `pyc/mlir/`: MLIR dialect, passes, emitters, tools (`pyc-opt`, `pyc-compile`)
- `include/pyc/`: backend template libraries (C++ + Verilog primitives)
- `examples/`: designs and checked-in generated outputs
- `docs/`: dialect contract and flows

## Linx example layout (in this repo)

- `examples/linx_cpu_pyc/`: pyCircuit design for the Linx CPU
- `examples/linx_cpu/`: SV testbench and program images (`*.memh`)
- `examples/generated/linx_cpu_pyc/`: checked-in golden Verilog/C++ and logs

## Bring-up observability (where traces live)

- Base commit/VCD traces are controlled via env vars (`PYC_TRACE`, `PYC_VCD`, `PYC_TRACE_DIR`). (Evidence: PYC-05)
- If PR #1 “Add pipeview, swimlane” is present, Konata/Perfetto exporters live in:
  - `include/pyc/cpp/pyc_trace_export.hpp`
  - used by `examples/linx_cpu_pyc/tb_linx_cpu_pyc.cpp`
  - forwarded by `tools/run_linx_cpu_pyc_cpp.sh` (Evidence: PYC-04)

## Build/regenerate loop

```bash
scripts/pyc build     # build pyc-opt/pyc-compile
scripts/pyc regen     # refresh checked-in golden outputs under examples/generated/
scripts/pyc test      # run repo tests
```
