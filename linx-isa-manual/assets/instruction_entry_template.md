# Instruction entry template

Copy this file when documenting a new instruction.

## {MNEMONIC} — {Short title}

### Summary

One sentence: what it does and its key architectural effects.

### Assembly syntax

```
{MNEMONIC} rd, rs1, rs2
```

Define operand types, width rules, and any syntactic constraints.

### Encoding

- Instruction length: {N} bits
- Fields:
  - `{field}`: bits `[hi:lo]`
- Reserved/illegal encodings:
  - `{rule}`: MUST trap as `IllegalInstruction` (or defined alternative)

If you maintain a bit diagram, include it here.

### Block ISA interaction (Linx-specific, if applicable)

- Is this a **block marker** (`BSTART.*`/`C.BSTART.*`/`BSTOP`/`C.BSTOP`)?
- Is this instruction only valid **inside a block** (after a block start marker)?
- If this instruction has a control-flow target:
  - State the **safety rule**: targets MUST point at a block start marker (including template macro blocks).
- If this is a call/return-related instruction:
  - State the `BSTART CALL` + `SETRET` adjacency rule (no instruction in between).

### Semantics (pseudocode)

Use explicit width casts and extension rules; avoid implicit truncation.

```text
tmp = ...
if ...:
  TRAP(cause, tval)
GPR[rd] = ...
PC = PC + {insn_length}
```

### Exceptions and traps

List every possible trap, including:

- Illegal instruction (bad encoding)
- Privilege fault
- Misaligned access
- Page fault (if applicable)

Define which architectural state is committed on a trap (precise state rules).

### Side effects

- Flags/condition codes
- CSRs
- Memory ordering effects (fences/atomics)

### Notes

- Undefined / implementation-defined behavior (minimize)
- Performance notes (non-normative)

### Test requirements

- Directed tests: {list}
- Negative tests: {list}
- Difftest/traces: {list}
