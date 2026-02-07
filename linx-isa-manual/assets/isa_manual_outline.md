# Linx ISA Manual outline (template)

Use this as a starting table-of-contents. Keep chapter numbering stable to make cross-references durable.

## 1. Introduction

- Goals and non-goals
- Normative language (RFC 2119 terms)
- Notation (bit slices, endianness, integer widths)

## 2. Programmer-visible state

- General-purpose registers (GPRs)
- Special registers (PC, flags, etc.)
- Control/status registers (CSRs) and privilege state

## 3. Instruction encoding

- Instruction length(s)
- Bit numbering + diagrams
- Field definitions
- Reserved/illegal encoding rules

## 4. Assembly language

- Mnemonic spelling
- Operand syntax + grammar
- Pseudo-instructions (if any)

## 5. Block ISA (Block Split)

- Block boundaries (`BSTART.*`/`C.BSTART.*`, `BSTOP`/`C.BSTOP`)
- Safety rule: every control-flow target MUST point at a block start marker
- Commit arguments (CARG) and `SETC.*` / `SETRET` sequencing rules
- Template macro blocks (`FENTRY`/`FEXIT`/`FRET.*`) as standalone blocks

## 6. Base ISA

- Instruction-by-instruction reference (use a consistent per-instruction template)

## 7. Privileged architecture

- Privilege levels and transitions
- Exceptions and interrupts (cause codes, priority, nesting)
- Trap entry/return sequence

## 8. Memory model

- Address spaces and translation (if any)
- Alignment rules
- Ordering guarantees, fences, atomics

## 9. Debug (optional)

- Debug CSRs/state
- Breakpoints/watchpoints (if defined architecturally)

## 10. ABI (optional, if in scope)

- Calling convention summary
- Stack alignment and register usage

## 11. Compliance and testing

- Required behaviors
- Conformance test strategy
- Known limitations / errata process
