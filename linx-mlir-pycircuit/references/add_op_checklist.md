# Add/modify a PYC op or type (reference)

Evidence anchor: use `PYC-*` IDs in `references/evidence.md` when justifying interface stability.

## 1) Update TableGen

- Ops: `pyc/mlir/include/pyc/Dialect/PYC/PYCOps.td`
- Types: `pyc/mlir/include/pyc/Dialect/PYC/PYCTypes.td`

Keep op assembly formats stable unless you intend to update existing `.pyc` goldens.

## 1.5) Keep “external” IDs stable (if you have them)

If the Linx CPU bring-up uses stable op IDs across backends/tests (e.g., `examples/linx_cpu_pyc/isa.py`), treat them as ABI:

- Do not renumber IDs casually.
- When adding IDs, append at the end.
- Update both Verilog and C++ consumers in the same change.

(Evidence: PYC-06)

## 2) Rebuild generated headers

Run:

```bash
scripts/pyc build
```

If TableGen errors occur, fix them before touching C++ impl files (otherwise you chase stale build artifacts).

## 3) Implement C++ behavior

Common edit points:

- Dialect registration: `pyc/mlir/lib/Dialect/PYC/PYCDialect.cpp`
- Op/type implementations: `pyc/mlir/lib/Dialect/PYC/PYCOps.cpp`, `.../PYCTypes.cpp`

## 4) Update lowering and emitters

- Passes: `pyc/mlir/lib/Transforms/`
- Verilog: `pyc/mlir/lib/Emit/VerilogEmitter.cpp`
- C++: `pyc/mlir/lib/Emit/CppEmitter.cpp`

## 5) Update goldens / regressions

```bash
scripts/pyc regen
```

Then run the Linx regression helper if applicable:

```bash
bash tools/run_linx_cpu_pyc_cpp.sh
```
