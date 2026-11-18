CREATE OR REPLACE TABLE customers AS
SELECT * FROM (VALUES
    (1, 'Asha',  'Pune'),
    (2, 'Ravi',  'Mumbai'),
    (3, 'Meera', 'Ahmedabad'),
    (4, 'Karan', 'Pune'),
    (5, 'Nisha', 'Bengaluru')
) AS t(customer_id, name, city);

CREATE OR REPLACE TABLE orders AS
SELECT * FROM (VALUES
    (101, 1, DATE '2025-03-01', 1200.50, 'delivered'),
    (102, 1, DATE '2025-04-10',  450.00, 'delivered'),
    (103, 2, DATE '2025-04-12', 3200.00, 'cancelled'),
    (104, 3, DATE '2025-05-05',  780.25, 'delivered'),
    (105, 4, DATE '2025-05-18',   99.99, 'pending'),
    (106, 2, DATE '2025-06-02', 1500.00, 'delivered'),
    (107, 9, DATE '2025-06-15', 2100.00, 'delivered'),
    (108, 1, DATE '2025-07-01',  640.00, 'pending')
) AS t(order_id, customer_id, order_date, amount, status);

SELECT c.name, o.order_id, o.amount
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
ORDER BY o.order_id;

SELECT c.name, o.order_id, o.amount
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;

SELECT c.name, o.order_id, o.customer_id AS order_customer_id
FROM customers c
FULL OUTER JOIN orders o ON o.customer_id = c.customer_id
ORDER BY o.order_id NULLS LAST;

SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;

SELECT name FROM customers ANTI JOIN orders USING (customer_id);

SELECT name FROM customers SEMI JOIN orders USING (customer_id);

SELECT c.city, count(*) AS orders, sum(o.amount) AS revenue
FROM orders o
JOIN customers c USING (customer_id)
WHERE o.status = 'delivered'
GROUP BY ALL
ORDER BY revenue DESC;

SELECT c.name, c.city,
count(o.order_id) FILTER (WHERE o.status = 'delivered') AS delivered_orders,
sum(o.amount) FILTER (WHERE o.status = 'delivered') AS delivered_total,
max(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY ALL;