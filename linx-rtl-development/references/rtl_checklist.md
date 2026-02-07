# Linx RTL bring-up checklist (reference)

Evidence anchor: use `RTL-*` IDs in `references/evidence.md` when justifying checks.

## Reset and initialization

- [ ] All architectural state has explicit reset values
- [ ] PC/reset vector is deterministic
- [ ] Any “X” sources are contained (uninitialized flops, don’t-care buses)

## Decode and legality

- [ ] Illegal encodings trap deterministically (reserved bits policy matches spec)
- [ ] Privilege checks are centralized and testable
- [ ] Block ISA legality is enforced:
  - [ ] branch/call/ret targets must land on a block start marker (safety rule) (Evidence: RTL-01)

## Execution

- [ ] Width/extension rules match the ISA spec exactly
- [ ] Shift-mask behavior matches the ISA spec exactly
- [ ] Side effects on trap are precise (either committed or not, per spec)
- [ ] Block boundaries match the spec model (`BSTOP` or implicit termination at next block start marker). (Evidence: RTL-01)

## Memory

- [ ] Endianness is consistent across RTL, emulator, and compiler
- [ ] Alignment rules are enforced (trap vs split)
- [ ] Byte enables are correct for sub-word stores

## Observability

- [ ] Commit log: PC + insn + writeback + trap metadata
- [ ] Include block-control fields when relevant (`brtype`, `carg`, `cond`, `tgt`) so “illegal instruction” bugs are actionable. (Evidence: RTL-03)
- [ ] Optional VCD dumping for failing tests

## Regression discipline

- [ ] Every fixed bug adds (or tightens) a regression test
- [ ] Tests are reproducible (fixed seeds, deterministic program images)
