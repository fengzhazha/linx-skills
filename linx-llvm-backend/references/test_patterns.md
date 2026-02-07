# LLVM test patterns for Linx (reference)

Evidence anchor: use `LLVM-*` IDs in `references/evidence.md` when justifying what to test.

## MC tests (asm ↔ bytes)

Prefer `llvm-mc` with `-show-encoding` or `llvm-objdump` round-trips.

Example skeleton:

```asm
# RUN: llvm-mc -triple=linx -show-encoding < %s | FileCheck %s

  add x1, x2, x3
# CHECK: add x1, x2, x3  # encoding: [0x..,0x..,0x..,0x..]
```

## CodeGen tests (IR → asm)

Keep IR minimal; check only the lines that matter.

```llvm
; RUN: llc -mtriple=linx -O2 < %s | FileCheck %s

define i32 @add_i32(i32 %a, i32 %b) {
; CHECK-LABEL: add_i32:
; CHECK: add
  %r = add i32 %a, %b
  ret i32 %r
}
```

## Tips

- Use `CHECK-LABEL` for function entry and then tight `CHECK:` lines.
- Avoid checking register numbers unless required; prefer patterns.
- If an instruction has multiple encodings, test all legal forms and one illegal form.

## Linx-specific test cases to add early

- **Frame macro blocks are standalone**: prologue/epilogue should emit `FENTRY`/`FRET.*` without surrounding `BSTART`/`BSTOP`. (Evidence: LLVM-03)
- **Call header adjacency**: if the backend prints or relies on `BSTART CALL` + `SETRET`, add a test that ensures no instruction can appear between them. (Evidence: LLVM-04)
- **PLT/shared-lib relocations**: add a smoke test that checks for `R_LINX_B17_PLT`, `.plt`, and `R_LINX_JUMP_SLOT` in shared objects. (Evidence: LLVM-09)
