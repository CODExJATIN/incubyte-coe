# Day 2 Notes

## UNION vs UNION ALL

In `set_operators.sql` I have two newsletter lists. 2024 has 4 emails (ravi is in there twice) and 2025 has 3 (ravi again).

- `UNION` gives **5** rows, it removes duplicates so ravi shows only once
- `UNION ALL` gives **7** rows, it just stacks both lists so ravi shows 3 times

So if you are adding up totals, UNION can silently drop real rows that just look the same (like two orders with the same amount on the same day) and UNION ALL can double count if the same data comes from both sides. Need to know which one the question actually needs.

## NULL things I tested (customer_questions.sql)

- `count(*)` counts every row but `count(amount)` skips NULLs, 10 vs 9 for orders
- `WHERE city = NULL` returns nothing, need `IS NULL`
- `NOT IN` returns nothing at all if the subquery has a NULL in it. `NOT EXISTS` gives the right answer (Dev and Nisha)
- in a join NULL never matches anything, so order 109 with no customer just falls off an inner join

## Checking Claude's queries against mine

I asked Claude Code to write the ten questions and checked two of them against queries I had already written in `joins.sql`:

- **Delivered revenue per city (Q3)**: same result as mine, Pune 1650.50, Mumbai 1500, Ahmedabad 780.25
- **Latest order per customer (Q9)**: the dates match my `max(order_date)` query. But ROW_NUMBER gives the whole row, not just the date, so you also get the order id and amount. It also showed that Meera's latest order has a NULL amount, which my query didn't show.

One thing I changed in Q10: Claude's first version included the order from customer 9 (who doesn't exist) in the overall average, so I joined with customers first.

## Reflection

Window functions were new for me compared to what I did in Postgres, needed some extra practice for that (`window_function_practice.sql`). Also learnt ANTI JOIN and SEMI JOIN.
