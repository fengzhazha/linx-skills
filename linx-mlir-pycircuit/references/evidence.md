# Evidence index (linx-mlir-pycircuit)

Use these IDs to justify PYC dialect/backends design decisions.

## PYC-01 — pyCircuit is a Python→MLIR frontend with multi-backend template libraries

Source: Codex session `019c22d5-634d-7203-a897-ee7ca363c286` user message in `/Users/zhoubot/.codex/sessions/2026/02/03/rollout-2026-02-03T17-28-55-019c22d5-634d-7203-a897-ee7ca363c286.jsonl` (requests: Python frontend emits `.pyc` MLIR; MLIR passes; common circuit components; C++ template backend + Verilog backend under `include/pyc/cpp` and `include/pyc/verilog`; design for extensibility).

## PYC-02 — Keep C++ and Verilog interfaces aligned; use template expressions for complex structures

Source: Same session as PYC-01; user message later in `/Users/zhoubot/.codex/sessions/2026/02/03/rollout-2026-02-03T17-28-55-019c22d5-634d-7203-a897-ee7ca363c286.jsonl` (requests: learn from `~/pto-isa`; define common data structures; make C++/Verilog interface the same; use C++ templates/template expressions).

## PYC-03 — Strict ready/valid semantics and multi-clock modeling are part of the IR contract

Source: Same session; tool output showing “PYC IR Spec (prototype)” in `/Users/zhoubot/.codex/sessions/2026/02/03/rollout-2026-02-03T17-28-55-019c22d5-634d-7203-a897-ee7ca363c286.jsonl` (mentions multi-clock modeling and strict ready/valid streaming semantics; FIFO push/pop rules).

## PYC-04 — Trace-first bring-up: Konata (O3PipeView) + Perfetto exports in pyCircuit PR #1

Source: GitHub PR #1 `zhoubot/pyCircuit` (“Add pipeview, swimlane.”), head `ea63425c3f631dfaa23483636673ec09295b60b4` (PR body lists `-p1/--pipeview/--pipfile/--swimlane/--swimfile/--boot-pc` flags).

Supporting sources in that PR head:
- `include/pyc/cpp/pyc_trace_export.hpp` (Konata/Perfetto trace writers)
- `examples/linx_cpu_pyc/tb_linx_cpu_pyc.cpp` (parses flags; emits “LinxISA Report”; writes traces)
- `tools/run_linx_cpu_pyc_cpp.sh` (forwards trace options to the TB)

## PYC-05 — `PYC_TRACE` as a bring-up debugging knob

Source: Same session as PYC-01; reasoning notes in `/Users/zhoubot/.codex/sessions/2026/02/03/rollout-2026-02-03T17-28-55-019c22d5-634d-7203-a897-ee7ca363c286.jsonl` about gating verbose C++ TB traces on the `PYC_TRACE` environment variable.

## PYC-06 — Stable “op ID” ABI across backends/tests for Linx bring-up CPU model

Source: GitHub PR #1 `zhoubot/pyCircuit` head `ea63425c3f...`, file `examples/linx_cpu_pyc/isa.py` (note: “Keep them stable across backends/tests (C++ + Verilog)”).

## PYC-07 — pyCircuit is expected to scale to a full Linx 5-stage CPU with dual backends + testbenches

Source: Same session as PYC-01; user message in `/Users/zhoubot/.codex/sessions/2026/02/03/rollout-2026-02-03T17-28-55-019c22d5-634d-7203-a897-ee7ca363c286.jsonl` requesting a “5-stage in order cpu based on LinxISA”, plus decoder/encoder, and both C++ and Verilog testbenches.

