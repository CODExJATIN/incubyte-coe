-- DuckDB can query CSV files directly – no loading step needed.
SELECT * FROM 'data/customers.csv' LIMIT 5;

-- Revenue per city (delivered orders only)
SELECT c.city,
       count(*)              AS orders,
       round(sum(o.amount), 2) AS revenue
FROM 'data/orders.csv'    o
JOIN 'data/customers.csv' c USING (customer_id)
WHERE o.status = 'delivered'
GROUP BY c.city
ORDER BY revenue DESC;

-- Window function: running total per customer
SELECT customer_id, order_date, amount,
       sum(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM 'data/orders.csv'
ORDER BY customer_id, order_date;
