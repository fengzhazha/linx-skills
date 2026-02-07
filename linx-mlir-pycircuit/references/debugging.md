# Debugging pyCircuit MLIR (reference)

Evidence anchor: use `PYC-*` IDs in `references/evidence.md` when justifying debug/trace requirements.

## Reduce first

- Reduce to a minimal `.pyc` file that still fails.
- Prefer isolating one pass or one emitter path at a time.

## Use the right tool

- `pyc-opt`: run passes over `.pyc` and inspect IR
- `pyc-compile`: end-to-end compile to Verilog/C++

## Common tactics

- Run one pass at a time and dump IR between passes.
- Keep `docs/IR_SPEC.md` as the contract; update it when behavior changes intentionally.

## Linx bring-up hooks (helpful knobs)

From the repo `README.md`:

- `PYC_TRACE=1` enables a commit/WB log
- `PYC_VCD=1` enables VCD dumping
- `PYC_TRACE_DIR=/path/to/out` overrides trace output directory

If PR #1 “Add pipeview, swimlane” is present, the Linx CPU C++ TB also supports:

- Konata pipeview: `-p1` or `--pipeview 1` (set output with `--pipfile`)
- Perfetto swimlane trace JSON: `--swimlane 1` (set output with `--swimfile`)
- Boot PC override: `--boot-pc <addr>` (also supports `PYC_BOOT_PC`)

(Evidence: PYC-04)
