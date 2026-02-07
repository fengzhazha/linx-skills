# Linx LLVM backend checklist (reference)

Use this as a “done means…” rubric for bring-up.

Evidence anchor: use `LLVM-*` IDs in `references/evidence.md` when justifying sequencing or constraints.

## 0. Preconditions (spec + conventions)

- ISA spec is stable enough to encode/decode deterministically.
- Register set, calling convention direction, and endianness are decided.
- There is at least one assembly test corpus (even tiny).
  - For Linx: decide the Block ISA contract (block start markers, safety rule, CARG lifetime) before deep optimizations. (Evidence: LLVM-01, LLVM-02)

## 1. MC layer first (encoding correctness)

Goal: deterministic bytes ↔ asm.

- [ ] Target registration and triple (in-tree or out-of-tree)
- [ ] Instruction encodings and operand printers
- [ ] Asm parser accepts canonical syntax
- [ ] Disassembler shows canonical syntax
- [ ] Block ISA printing is stable:
  - [ ] `BSTART`/`C.BSTART` forms, `BSTOP`/`C.BSTOP`, and call-header sugar (if used) are unambiguous. (Evidence: LLVM-04, LLVM-10)
- [ ] `llvm-mc` round-trip tests exist for:
  - [ ] fixed encodings
  - [ ] immediate edge cases
  - [ ] illegal encodings (must be rejected or printed as `.word`)

## 2. Basic codegen (correctness before performance)

Goal: `llc` emits correct assembly for a constrained subset.

- [ ] Register info and register classes
- [ ] Instruction selection for:
  - [ ] integer add/sub/logic
  - [ ] shifts (with correct mask/width behavior)
  - [ ] branches/jumps (PC-relative rules)
- [ ] Prologue/epilogue correctness:
  - [ ] stack grows direction chosen and documented
  - [ ] stack alignment enforced
  - [ ] callee-saved preserved
  - [ ] Frame macro blocks (`FENTRY`/`FEXIT`/`FRET.*`) are treated as standalone blocks (no extra `BSTART`/`BSTOP`). (Evidence: LLVM-03)
  - [ ] `BSTART CALL` + `SETRET` adjacency is preserved. (Evidence: LLVM-04)

## 3. Memory + ABI details

- [ ] Loads/stores with:
  - [ ] correct endianness
  - [ ] correct sign/zero extension
  - [ ] correct alignment behavior (trap/unaligned rules)
- [ ] Calls/returns:
  - [ ] argument passing registers + spill rules
  - [ ] return value registers
  - [ ] varargs (if supported)

## 4. Object emission + linking

- [ ] Object writer + relocations for:
  - [ ] branches/jumps
  - [ ] absolute/PC-relative data references
- [ ] Can link and run a minimal program in the emulator
- [ ] Relocation coverage matches the bring-up test harness:
  - [ ] ET_REL loader path works (QEMU loads relocatable objects and applies relocations). (Evidence: LLVM-11)
  - [ ] PLT/shared-lib relocation types are produced and observable in tooling:
    - [ ] `R_LINX_B17_PLT` in PIC objects
    - [ ] `.plt` section exists in shared objects
    - [ ] `R_LINX_JUMP_SLOT` relocations exist for external calls
    - [ ] `.plt` disassembly contains `BSTART IND` entries (per current convention) (Evidence: LLVM-09)

## 5. Testing discipline

- [ ] Every new instruction has:
  - [ ] MC encoding test
  - [ ] CodeGen test (IR → asm)
- [ ] A “conformance” test suite exists that can run in the emulator/RTL.
