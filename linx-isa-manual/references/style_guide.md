# Linx ISA spec style guide (reference)

Evidence anchor: use `MAN-*` IDs in `references/evidence.md` when justifying wording choices.

## Normative language

Use RFC 2119 terms consistently:

- **MUST** / **MUST NOT**: hard architectural requirements
- **SHOULD** / **SHOULD NOT**: strong recommendation, but exceptions may exist (explain them)
- **MAY**: optional behavior

Avoid lowercase “should/must/may” in normative statements; prefer uppercase so requirements are grep-able and unambiguous.

## Notation conventions

- Spell out bit slicing and concatenation rules (e.g., `[hi:lo]` inclusive).
- State bit numbering (LSB=0) and endianness (byte order in memory).
- Use explicit types in pseudocode:
  - `uN` for N-bit unsigned
  - `sN` for N-bit signed (two’s complement)
- Use `sext(x, N)` / `zext(x, N)` helpers (or equivalents) to make extension explicit.

## Pseudocode rules

- Make all truncation explicit.
- Specify PC update for every instruction.
- Specify trap behavior precisely:
  - trap cause code
  - trap value (`tval`) and how it is computed
  - whether architectural state is committed (precise vs imprecise)
- Keep pseudocode deterministic (no “implementation-defined” unless unavoidable).

## Encoding rules

- State behavior for every encoding bit:
  - fixed (opcode/funct bits)
  - field (operand/immediate bits)
  - reserved (define whether it traps or must be zero)
- Prefer “reserved bits MUST be zero and otherwise MUST trap” over “ignored” unless there is a compatibility reason.

## Document structure rules

- Keep instruction entries structurally identical.
- Put non-normative notes in a clearly labeled **Notes** section.
- Add “Compatibility” notes when behavior changes across revisions.

## Block ISA language (Linx-specific)

- Use the term **block start marker** consistently for the encodings that may be used as control-flow targets. (Evidence: MAN-02, MAN-03)
- State the **safety rule** in normative language where control-flow is introduced: targets MUST point at a block start marker; branching into the interior of a block MUST raise an exception. (Evidence: MAN-02, MAN-03)
- When describing call/return, include the adjacency constraint for the call header (`BSTART CALL` + `SETRET`). (Evidence: MAN-07)
- When describing frame macro blocks (`FENTRY`/`FEXIT`/`FRET.*`), describe them as **standalone blocks** (they conceptually include their own block boundary behavior). (Evidence: MAN-04, MAN-05)
