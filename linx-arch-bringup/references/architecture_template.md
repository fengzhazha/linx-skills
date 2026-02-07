# Architecture doc template (reference)

Use this template when writing a microarchitecture plan for a Linx core.

Evidence anchor: use `ARCH-*` IDs in `references/evidence.md` when pointing to block ISA constraints.

## 1. Scope

- ISA subset and extensions
- privilege model assumptions
- memory model assumptions
- Block ISA assumptions (block markers, safety rule, CARG, template macro blocks)

## 2. Pipeline overview

- stage diagram (fetch/decode/execute/mem/wb)
- where traps are detected and committed
- branch strategy (predict/not, resolve stage)
- where block boundaries are detected and where CARG is updated/committed

## 3. Hazard handling

- forwarding matrix
- stall conditions
- multi-cycle operations

## 4. Memory system

- alignment rules
- caches (if any) and refill behavior
- MMU/TLB (if any)

## 5. CSRs and privilege

- CSR address map
- RO/W1C semantics
- trap entry/return
- interrupt priority

## 6. Debug and observability

- commit trace fields
- debug hooks (single-step, breakpoints) if applicable

## 7. Verification plan

- feature → tests map
- difftest strategy
- formal targets (optional)
