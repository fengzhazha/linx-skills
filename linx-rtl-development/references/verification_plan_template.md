# Verification plan template (reference)

Use this format to keep bring-up scoped and measurable.

Evidence anchor: use `RTL-*` IDs in `references/evidence.md` when pointing to why a requirement exists.

## Feature: {name}

### Spec contract

- Relevant spec sections:
- Normative requirements:
  - Block ISA interactions (if any): safety rule, block boundaries, CARG/reset rules.

### Implementation notes

- RTL blocks impacted:
- Emulator/compiler impacts:

### Tests

- Directed tests:
  - `{test}`: expected behavior
- Negative tests:
  - `{test}`: expected trap/cause
- Random/regression:
  - seed strategy, coverage notes

### Done means

- Tests passing in:
  - emulator
  - RTL sim (fast)
  - RTL sim (full)
- Difftest traces match (if applicable)
