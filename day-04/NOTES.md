# Day 4 Notes

## Semi-structured data

A normal table has fixed columns and every row has all of them. Semi-structured data like JSON doesn't: an order can have a nested `customer` object and an `items` array inside it, and two orders don't need to have the same fields. One order can have an email, the next one doesn't.

To get it into tables I flatten it:
- nested objects become dotted columns, `customer.name`, `customer.email`
- the `items` array becomes its own table, one row per line, linked back with `order_id`

So one order becomes one row in `orders` and N rows in `order_lines`.

## Schema drift

Schema drift is when the shape of the data changes without warning, a new field shows up or an old one stops coming. The pipeline should not crash on that and should not silently drop data either.

How mine handles it:
- **missing field** (Ravi has no email) -> column is filled with null
- **new field** (`channel` on the order, `gift_wrap` on a line) -> ignored, only the columns I listed are kept
- **empty items array** -> order is kept, it just has no lines
- **no items field at all or items is null** -> same as empty, order is kept with no lines. This one used to crash, fixed it today

Ignoring new fields is a choice, it keeps the pipeline running but the new data is lost. In a real pipeline I would at least log it so someone knows a new field started coming.

## What I missed

My first version had tests for a missing field, a new field and an empty items array, but I only thought about `items` being an empty list. When I tried more cases two of them crashed:

- order with **no `items` key** -> `KeyError: 'items'`, because the code did `order["items"]`
- order with **`"items": null`** -> `TypeError: 'NoneType' object is not iterable`

Both are normal in real JSON, some systems leave the field out and some send null instead of `[]`. And the crash would stop the whole load, not just skip that one order. Fixed both test-first with `order.get("items") or []`, so missing, null and empty all mean "no lines".

Then I tried more scenarios and found a few more:

- **empty file `[]`** -> crashed in DuckDB (`executemany` needs a non-empty list). Now it just creates empty tables, a day with no orders is normal
- **order with no `order_id`** -> `KeyError`, killed the whole load. Now that order is skipped, its lines can't be joined to anything anyway
- **`null` or junk inside the items list** -> `AttributeError`. Now only that line is skipped, the rest of the order still loads
- **duplicate `order_id`** -> didn't crash, but the join back doubled the lines (2 lines became 4). My reconcile check showed the counts didn't match, which is exactly why the counts matter. Now the first order wins, same rule as Day 3

Left for later: `qty: "two"` still crashes the load in DuckDB and `qty: 2.7` is silently stored as 3. That's type checking, which is more Day 9 data tests.

Same thing as Day 1 and Day 3, I tested wrong values but missed the shape of the data being different.

## XML basics

XML is the older format for the same kind of nested data. Data sits inside elements like `<customer><name>Asha</name></customer>`, and elements can also have attributes like `<order id="1001">`. JSON has no attributes, only keys and values, and has proper arrays, while in XML a list is just repeated elements. JSON is also shorter and maps straight to Python dicts and lists.

## Sample file

`orders.json` has 5 orders with the drift cases in it (missing email, new fields, empty items, no items). Loading it gives 5 orders and 4 lines and the join back loses nothing.

## Reflection

If we flatten without checking the row counts then rows can go missing or get doubled, the code raises no error since everything in the data seems fine but the numbers are wrong.
