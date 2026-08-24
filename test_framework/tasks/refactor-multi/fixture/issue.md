# Refactor: extract calculation engine + typed models

## Context

`invcalc/core.py` has grown into a monolith. The tax and discount percentage
math is copy-pasted in several places, and the data model is raw dicts
everywhere, which makes call sites hard to read and the math impossible to
audit in one place.

## Requirements

Complete ALL of the following. The acceptance criteria are machine-checked.

1. **Extract the engine.** Create `invcalc/engine.py` containing the pure
   calculation logic (line net totals, tax, discounts). `core.py` must import
   and delegate to it — no calculation formulas may remain duplicated.

2. **One percentage helper.** All percentage math (discounts AND tax) must go
   through a single shared helper in `engine.py`. Concretely: the expression
   pattern `round(x * y / 100, 2)` may appear **at most once** across all
   modules in the `invcalc` package after the refactor.

3. **Typed models with dict compatibility.** Rework `invcalc/models.py` to use
   `@dataclass` (or `NamedTuple`) for lines and invoices, each with a
   `to_dict()` method. Public functions must keep accepting the plain dicts
   they accept today (duck-type both dict and model inputs), and
   `new_line`/`new_invoice` keep returning objects that expose the same fields.

4. **Public API unchanged.** Every function in the README contract keeps its
   exact name and parameter list (names, order, defaults). Existing tests in
   `tests/` must pass unmodified.

## Out of scope

- New features, new validation rules, CLI behavior changes, storage format
  changes.

## Acceptance

- `/usr/bin/python3 -m pytest tests/ -q` exits 0 on your refactored tree.
- The hidden acceptance suite checks items 1-4 structurally and behaviorally.
