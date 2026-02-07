# Linx architecture bring-up checklist (reference)

Evidence anchor: use `ARCH-*` IDs in `references/evidence.md` when justifying checklist items.

## Minimal “first light” milestone

- [ ] Reset sequence and initial privilege state are defined
- [ ] Fetch/decode/execute can run a tiny program from ROM/RAM
- [ ] A trap/exception path works (even for illegal instruction)
- [ ] A simple UART/printf-equivalent path exists (optional but high leverage)
- [ ] Block ISA basics work end-to-end:
  - [ ] block start/end markers are recognized
  - [ ] safety rule is enforced (branch to non-marker traps)
  - [ ] CARG resets at block start and commits at block boundaries (Evidence: ARCH-01)

## Feature-by-feature milestone map

Define each feature with:

- spec requirement
- expected architectural effects
- emulator reference behavior
- RTL check strategy
- tests (directed + negative)

High-value early features:

- branches/jumps (PC update and alignment)
- load/store (endianness and extension)
- CSR read/write and privilege checks
- interrupt entry/return (if applicable)

## Difftest readiness

- [ ] A commit trace schema exists and is shared by RTL + emulator
- [ ] The trace contains enough to localize:
  - PC/insn
  - reg writes
  - memory writes
  - traps (cause/tval)
  - block-control metadata (`brtype`, `carg`, `cond`, `tgt`) when applicable (Evidence: ARCH-05)

## Benchmark/report readiness

- [ ] For each benchmark, produce:
  - [ ] static instruction count (from disassembly)
  - [ ] dynamic instruction count + instruction histogram (from emulator tracing/instrumentation) (Evidence: ARCH-04)
