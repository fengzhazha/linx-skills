---
name: linx-rtl-development
description: RTL and verification workflows for Linx CPU cores. Use when writing/modifying SystemVerilog/Verilog RTL, designing microarchitectural blocks (pipeline, CSR, cache, MMU), building testbenches, running open-source simulation (Icarus/Verilator), adding assertions/formal checks, or aligning RTL behavior with the Linx ISA spec and emulator.
---

# Linx RTL Development

## Overview

Develop Linx CPU RTL with a bring-up-first workflow: quick simulation, strong observability, and continuous alignment with the ISA spec and emulator.

When you need the concrete “why”, open `references/evidence.md` and cite the matching evidence ID in your change notes.

## Bring-up invariants (Block ISA)

- Implement and test the **safety rule**: architectural control-flow targets must land on a block start marker; otherwise trap/illegal. (Evidence: RTL-01)
- Model **block boundaries** correctly: blocks end at `BSTOP`/`C.BSTOP` or the next block start marker; block-local state (e.g., CARG) resets at block start and is evaluated/committed at boundaries. (Evidence: RTL-01)
- Treat `FENTRY`/`FEXIT`/`FRET.*` as standalone blocks when generating/consuming traces and when defining “function boundary” behavior. (Evidence: RTL-02)

## Bring-up workflow (recommended loop)

1. Pick one feature (one instruction, one exception, one CSR).
2. Update the spec (if needed) and ensure emulator + compiler expectations are clear.
3. Implement RTL with explicit reset/invalid behavior.
4. Add a self-checking test:
   - Directed program (assembly / mem image)
   - Checker that validates architectural effects (regs/mem/traps)
5. Run simulation (fast path first), then expand coverage.
6. If RTL != emulator: reduce to first-diff trace and fix root cause.

## Observability checklist

- PC + current instruction word at commit
- Register writeback (rd, value, write-enable)
- Memory ops (addr, data, size, byte-enables)
- Trap/exception cause + tval + next PC
- Reset sequencing + privilege state
- Block-control metadata (when available): `brtype`, `carg`, `cond`, `tgt` (match what QEMU logs on failures). (Evidence: RTL-03)

## Practical verification structure

- Smoke tests: 5–20 tiny programs that each isolate a feature
- Random/regression tests: seeded, reproducible
- Assertions: invariants that should never fail (e.g., alignment, CSR RO bits)
- Formal (optional): local proofs for tricky blocks (CSR file, decoders, FIFOs)

## In this repo (pyCircuit example)

- SV testbench: `examples/linx_cpu/tb_linx_cpu_pyc.sv`
- Program images: `examples/linx_cpu/programs/*.memh`
- Verilog flow doc: `docs/VERILOG_FLOW.md`

## References

- `references/rtl_checklist.md`
- `references/verification_plan_template.md`
- `references/sim_commands.md`
- `references/evidence.md`
