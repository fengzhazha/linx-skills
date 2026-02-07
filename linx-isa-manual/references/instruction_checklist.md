# Instruction entry checklist (reference)

Use this checklist before declaring an instruction “done”.

Evidence anchor: use `MAN-*` IDs in `references/evidence.md` when justifying decisions.

## Required fields

- [ ] Mnemonic spelling and expansion rules (if pseudo-ops exist)
- [ ] Operand syntax and constraints (register classes, immediates, alignment)
- [ ] Encoding with:
  - [ ] full bit field map
  - [ ] reserved/illegal encoding behavior
- [ ] Semantics pseudocode with:
  - [ ] explicit width/extension rules
  - [ ] explicit PC update
- [ ] Exceptions/traps list (including negative cases)
- [ ] Side effects (flags, CSRs, memory ordering)
- [ ] Reset/initial state dependencies (if any)

## Block ISA invariants (Linx-specific)

- [ ] If the instruction is a **block marker** (`BSTART.*`, `C.BSTART.*`, `BSTOP`, `C.BSTOP`) clearly state:
  - [ ] whether it **ends the current block**, **begins the next**, or both (tooling may treat “next block start” as an implicit end). (Evidence: MAN-01)
- [ ] If the instruction is only valid **inside a block** (e.g., `SETC.*` / `SETRET`-style operations), state that it MUST execute after a block start marker. (Evidence: MAN-01)
- [ ] If the instruction creates/consumes a control-flow target, state the **safety rule**: targets MUST be a block start marker (including template macro blocks). (Evidence: MAN-02, MAN-03)
- [ ] If documenting calls/returns, include the **call header adjacency** rule: `BSTART CALL, <target>` + `SETRET` MUST be adjacent (no instruction between). (Evidence: MAN-07)
- [ ] If documenting `FENTRY`/`FEXIT`/`FRET.*`, state they are **standalone blocks** (do not require surrounding `BSTART`/`BSTOP`). (Evidence: MAN-04, MAN-05)

## Cross-artifact consistency

- [ ] Emulator implements the exact same trap rules and width rules
- [ ] LLVM backend encodes/decodes identically and uses the same operand constraints
- [ ] RTL decoder treats reserved bits the same way (trap vs ignore)
  - [ ] Specifically: toolchain/emulator/RTL agree on which encodings count as **block start markers** (e.g., template macro blocks). (Evidence: MAN-03, MAN-05)

## Testability

- [ ] Directed tests cover:
  - [ ] corner operands (0, -1, max, min)
  - [ ] boundary immediates / shift amounts
  - [ ] branch target edge cases (alignment, sign extension)
- [ ] Negative tests cover:
  - [ ] illegal encodings
  - [ ] privilege faults
  - [ ] misaligned accesses (if applicable)
- [ ] Difftest trace schema contains enough fields to localize a mismatch
