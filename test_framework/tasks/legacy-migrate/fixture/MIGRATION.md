# MIGRATION — oldorm 0.x → neworm 2.x

`inventory/` still uses the vendored `oldorm/` 0.x API. Migrate it to the
vendored `neworm/` 2.x API. `neworm/` is the same engine with breaking
API changes; the application's behavior must not change.

## API mapping

| oldorm 0.x                                | neworm 2.x                                      |
|-------------------------------------------|-------------------------------------------------|
| `from oldorm import Session, Model, ...`  | `from neworm import Session, Model, ...`        |
| `session.query(Item)`                     | `session.select(Item)`                          |
| `.filter(sku=sku)`                        | `.where(sku=sku)`                               |
| `.order_by("qty")` / `.order_by("-oid")`  | `.order_by(asc("qty"))` / `.order_by(desc("oid"))` |
| `Meta.ordering = ["sku"]`                 | `class Config:` with `def order_by(M): return [asc("sku")]` |
| `Meta.table` / `Meta.pk`                  | `Config.table` / `model_config["pk"]`           |
| `Meta.required` / `Meta.types`            | `model_config["required"]` / `model_config["types"]` |
| `Meta.hooks = {...}`                      | `model_config["hooks"] = {...}`                 |
| `Model.validate(data)`                    | `Model.model_validate(data)`                    |
| `model.dict()`                            | `model.model_dump()`                            |
| `session.save(instance)`                  | `session.persist(instance)`                     |
| `def cb(instance, old)` — `old` is the previous dict, or `None` on first save | `def cb(instance, previous_state)` — `previous_state` is a `neworm.Snapshot`, never `None`; empty on first save; `.as_dict()` gives the dict form |

`asc(field)` / `desc(field)` are exported from `neworm`. `Config.order_by`
is a **callable**: it receives the model class and returns a list of specs;
it is evaluated per query as the default ordering.

## Gotchas

1. **Ordering is no longer a list of strings.** `Meta.ordering = ["qty", "-oid"]`
   becomes a callable `Config.order_by(M)` returning
   `[asc("qty"), desc("oid")]`; explicit `.order_by("-oid")` becomes
   `.order_by(desc("oid"))`. String specs raise `TypeError` in 2.x.
2. **Hook callbacks changed signature AND state type.** 0.x called
   `cb(instance, old)` with a plain dict (or `None` on first save); 2.x calls
   `cb(instance, previous_state)` with a `Snapshot` that is never `None` —
   on first save it is empty, so use `if previous_state:` instead of
   `if old is None:`, and `previous_state["field"]` / `.as_dict()` for values.
   Hooks are registered in `model_config["hooks"]`, not `Meta.hooks`.
3. **`model_validate` rejects unknown keys.** `Model.validate` silently
   ignored keys not listed in `Meta.types`; `Model.model_validate` raises
   `ValidationError` for them. Data that only ever contains declared fields
   is unaffected.

## Rules

- Migrate `inventory/` only. Do **not** edit `oldorm/`, `neworm/`, or `tests/`.
- The application's observable behavior must not change; `pytest tests/ -q`
  is green before and must stay green after.
- After the migration `inventory/` must not import `oldorm` or touch any of
  its deprecated surface (`query`, `validate`, `dict`, `save`, `Meta`,
  `(instance, old)` callbacks).
