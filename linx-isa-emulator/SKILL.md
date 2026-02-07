---
name: linx-isa-emulator
description: Instruction-accurate emulator development for the Linx ISA (QEMU-like). Use when building decode/execute, handling exceptions/interrupts, implementing memory/MMU/devices, adding GDB-style debugging, or building differential/conformance tests against the Linx spec or RTL.
---

# Linx ISA Emulator

## Overview

Build an instruction-accurate Linx emulator that is easy to debug and good for differential testing during RTL bring-up.

When you need the concrete “why”, open `references/evidence.md` and cite the matching evidence ID in your change notes.

## Bring-up invariants (Linx Block ISA)

- Enforce the **safety rule**: every architectural control-flow target MUST point at a block start marker; otherwise raise an exception/illegal instruction. (Evidence: EMU-01, EMU-02)
- Treat a **block** as the architectural sequencing unit (commit at `BSTOP` or implicit termination at the next block start marker). (Evidence: EMU-01)
- Treat frame macro instructions (`FENTRY`/`FEXIT`/`FRET.*`) as **standalone blocks** for bring-up tooling and translation. (Evidence: EMU-03)

## Workflow (implement or change an instruction)

1. Confirm spec intent: encoding validity, operand decoding, side effects, traps.
2. Decode:
   - Reject illegal encodings deterministically (reserved bits, bad funct, etc.).
   - Keep decode tables single-source when possible.
3. Execute:
   - Implement semantics with explicit width/extension rules.
   - Update architectural state atomically from the perspective of exceptions.
4. Exceptions + interrupts:
   - Define priority and precise state (PC, cause, tval, etc.).
   - Ensure side effects are either committed or not committed (match spec).
5. Observability:
   - Add disassembly + per-instruction trace (PC, insn, regs touched, mem ops).
6. Tests:
   - Add a directed test and at least one negative test per new behavior.
   - If RTL exists, add a difftest trace comparison.

## QEMU-style performance model (Block ISA → TBs)

- Translate **one Linx block into one QEMU TB** (from a block start marker up to `BSTOP` or the next block start marker). (Evidence: EMU-04)
- Use `goto_tb` chaining when the next target is fixed and no `SETC.TGT` override occurs inside the block; fall back to indirect dispatch otherwise. (Evidence: EMU-04, EMU-05)

## Differential testing tips

- Prefer comparing commit traces (architectural state changes) over raw signal dumps.
- Normalize both sides into a common record: `{pc, insn, gpr writes, mem writes, trap}`.
- Use `scripts/trace_diff.py` to spot the first divergence quickly.

Example:

```bash
python3 "$CODEX_HOME/skills/linx-isa-emulator/scripts/trace_diff.py" rtl.log emu.log
```

## Debugging playbook (first 30 minutes)

- If branch/jump bugs: verify PC update + alignment + sign extension.
- If load/store bugs: check endianness, alignment rules, and address translation.
- If “random” failures: check reserved/illegal encodings and reset state.

### If you see `linx_insn_decode_fail ... insn=0x00000000 len=2`

Treat this as a *loader vs decode* problem first:

- `0x0000` in the 16-bit space is conventionally `C.BSTOP` (all-zeros); ensure it is decoded/handled intentionally. (Evidence: EMU-06)
- If the PC points into a region that should contain code, verify the loader’s section mapping and relocation application (common failure: reading file offset instead of loaded VA). (Evidence: EMU-06, EMU-07)

### If you see `qemu: fatal: Linx: Illegal instruction` in benchmark runs

Triage as “unsupported instruction vs bad bytes”:

1. Capture the reported `pc=...` and dump bytes/disasm around that address.
2. If bytes decode to a valid instruction per the JSON spec but QEMU dies, implement the missing translation/exec path.
3. If bytes do not match any valid encoding, investigate relocations/loader and the safety rule (jumped into non-marker). (Evidence: EMU-02, EMU-07)

For histogram/dynamic counts from trace logs, use `scripts/qemu_trace_hist.py` (added in this skill). (Evidence: EMU-08)

## References

- `references/emulator_workflow.md`
- `references/difftest.md`
- `references/evidence.md`
