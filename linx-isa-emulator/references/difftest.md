# Difftest strategy (reference)

Evidence anchor: use `EMU-*` IDs in `references/evidence.md` when justifying trace fields.

## Why commit traces

Raw RTL waveforms are too low-level for fast bug localization. Commit traces compare the architectural intent:

- which instruction retired (PC + instruction word)
- what architectural state changed (register writes, memory writes)
- whether a trap occurred (cause + metadata)

## Suggested record schema

Keep one record per retired instruction:

```text
pc=<hex> insn=<hex> trap=<0|1> cause=<hex?> tval=<hex?>
gpr: x1=<hex> x5=<hex> ...
memw: addr=<hex> size=<1|2|4|8> data=<hex>
```

For Block ISA bring-up, add block-control metadata when it exists in your model:

```text
brtype=<n> carg=<hex> cond=<0|1> tgt=<hex>
```

(Evidence: EMU-07)

## Comparison rules

- Compare the first divergence, not the whole log.
- Normalize:
  - ignore timestamps/cycle counters
  - canonicalize hex case and leading zeros
- If a trap happens:
  - compare PC/insn at trap
  - compare cause/tval and next PC (epc/trap vector behavior)

## Tooling

Use `scripts/trace_diff.py` as a first-pass mismatch locator, then tighten the trace schema if too much noise remains.
