# Linx emulator workflow (reference)

Evidence anchor: use `EMU-*` IDs in `references/evidence.md` when justifying implementation choices.

## Core design goals

- Deterministic decode and trap behavior (reserved bits, privilege checks)
- Precise architectural state updates (easy difftest)
- Strong observability (trace logs that localize bugs)

## Linx Block ISA requirements

- Model **blocks** explicitly:
  - begin at a block start marker (`BSTART.*` / `C.BSTART.*`) or a standalone template macro block (e.g., `FENTRY`/`FRET.*`)
  - end at `BSTOP`/`C.BSTOP` or at the next block start marker (implicit termination) (Evidence: EMU-01, EMU-03)
- Implement/enforce the **safety rule**: architectural control-flow targets must land on a block start marker; otherwise raise an exception/illegal instruction. (Evidence: EMU-02)
- Treat **CARG** as architectural state that is initialized at block start and committed at block boundaries. (Evidence: EMU-01)

## Suggested structure

### CPU state

Keep CPU state intentionally minimal and explicitly typed:

- GPR array + special regs (PC, flags)
- Privilege state + CSRs (if defined)
- Pending interrupts + mask state

### Decode

Prefer a table-driven decoder:

- A single decode table that drives:
  - execute dispatch
  - disassembler printing
  - “legal encoding” checks

Rules of thumb:

- “Reserved” bits are dangerous; decide early whether they trap or are ignored.
- Illegal encodings should trap before any state changes.
- Remember the `C.BSTOP` / all-zeros convention when debugging decode failures around `0x0000`. (Evidence: EMU-06)

### Execute

Keep helpers for the tricky classes:

- sign/zero extension
- shift masks and width truncation
- alignment checks
- memory access helpers (endianness and translation)

### Exceptions and interrupts

Define in one place:

- priority ordering
- whether traps are precise
- what gets written (cause, tval, epc)
- trap entry and return rules

## Minimal smoke suite

Start with tiny programs that each isolate one behavior:

- ALU ops (edge operands)
- branch/jump (PC-relative sign extension + alignment)
- load/store (endianness + alignment)
- illegal encoding (reserved bits)
- privilege fault (CSR access, if applicable)
- block markers + safety rule (branch to non-marker must trap) (Evidence: EMU-02)

## Practical tracing (QEMU-like)

- Enable trace events for bring-up:
  - `--trace "linx_insn_exec,linx_insn_decode_fail"` (Evidence: EMU-07)
- If you need counts/histograms, parse trace output with `scripts/qemu_trace_hist.py`. (Evidence: EMU-08)
