# inventory — warehouse stock and order tracking

A stdlib-only application that tracks warehouse stock and orders. It is
built on the vendored mini-ORM in `oldorm/` (0.x API). Its successor
`neworm/` (2.x API, breaking changes) is vendored alongside it — see
`MIGRATION.md`.

## Layout

```
oldorm/       vendored legacy ORM 0.x (do not edit)
neworm/       vendored successor ORM 2.x (do not edit)
inventory/    the application (oldorm 0.x API)
├── models.py     Item / Order models (class Meta config)
├── warehouse.py  receive/issue stock, stock listings
├── orders.py     order lifecycle (create / fulfill / ledger)
├── reports.py    valuation + open-order aggregates
└── audit.py      save-hook callbacks (audit trail)
tests/         behavior suite (must stay green)
```

## Development

```
/usr/bin/python3 -m pytest tests/ -q
```

## Domain rules

- Items are identified by `sku`; `receive_stock` creates or accumulates,
  `issue_stock` refuses to go negative (`InsufficientStock`).
- Orders are opened against known skus with positive qty, then fulfilled
  exactly once (`AlreadyFulfilled` on repeat); fulfillment decrements stock.
- Every save fires an audit hook (`inventory/audit.py`) recording the
  change; `inventory.audit.entries()` exposes the trail.
- Item fields: `sku` (str, pk), `qty` (int), `price` (float).
  Order fields: `oid` (str, pk), `sku`, `qty` (int), `status` (str).
