# Simulation commands (reference)

Evidence anchor: use `RTL-*` IDs in `references/evidence.md` when justifying observability requirements.

This repo includes a documented open-source flow:

- `docs/VERILOG_FLOW.md` (Icarus/Verilator/GTKWave)

## Typical loop

1. Generate or update the design (if using pyCircuit).
2. Run a small targeted test (one program image).
3. Enable tracing (commit log, then VCD) only when needed.

## Practical tips

- Keep smoke tests tiny and isolated (one feature per test).
- Prefer self-checking testbenches over manual waveform inspection.
- When debugging, align trace schemas between RTL and emulator (PC/insn/reg/mem/trap).
  - Include Block ISA fields (`brtype`, `carg`, `cond`, `tgt`) if they exist in your microarchitecture; QEMU fatal logs already report them. (Evidence: RTL-03)
