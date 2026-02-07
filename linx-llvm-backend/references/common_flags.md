# Useful LLVM flags for backend bring-up (reference)

Evidence anchor: use `LLVM-*` IDs in `references/evidence.md` when justifying tool choices.

## llc

- `-mtriple=linx64-linx-none-elf` / `-mtriple=linx32-linx-none-elf`: select the target (current bring-up triples). (Evidence: LLVM-12)
- `-O0` vs `-O2`: separate legalization/isel bugs from optimization bugs
- `-verify-machineinstrs`: catch invalid MIR early
- `-print-after-all`: dump IR/MIR after each pass (noisy but effective)
- `-stop-after=<pass>`: bisect pass pipeline (when supported)

## opt

- `-passes='...'`: run a specific pass pipeline (new PM)
- `-S`: emit human-readable IR

## llvm-mc

- `-triple=linx`: select the target
- `-show-encoding`: print bytes for each instruction
- `-disassemble`: bytes → asm

## llvm-objdump / llvm-readobj

- `-d`: disassemble
- `-r`: relocations
- `-t`: symbols
- `--triple=<triple>`: force disassembly target when the object format is ambiguous

## General debug hygiene

- Reduce first: keep reproducers tiny.
- Prefer adding tests over leaving “known issues” notes.
