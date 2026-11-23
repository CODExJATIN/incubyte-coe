CREATE OR REPLACE TABLE customers AS
SELECT * FROM (VALUES
    (1, 'Asha',  'Pune'),
    (2, 'Ravi',  'Mumbai'),
    (3, 'Meera', 'Ahmedabad'),
    (4, 'Karan', 'Pune'),
    (5, 'Nisha', 'Bengaluru'),
    (6, 'Dev',   NULL)
) AS t(customer_id, name, city);

CREATE OR REPLACE TABLE orders AS
SELECT * FROM (VALUES
    (101, 1,    DATE '2025-03-01', 1200.50, 'delivered'),
    (102, 1,    DATE '2025-04-10',  450.00, 'delivered'),
    (103, 2,    DATE '2025-04-12', 3200.00, 'cancelled'),
    (104, 3,    DATE '2025-05-05',  780.25, 'delivered'),
    (105, 4,    DATE '2025-05-18',   99.99, 'pending'),
    (106, 2,    DATE '2025-06-02', 1500.00, 'delivered'),
    (107, 9,    DATE '2025-06-15', 2100.00, 'delivered'),
    (108, 1,    DATE '2025-07-01',  640.00, 'pending'),
    (109, NULL, DATE '2025-07-05',  300.00, 'pending'),
    (110, 3,    DATE '2025-07-10',    NULL, 'pending')
) AS t(order_id, customer_id, order_date, amount, status);

-- Q1. How many orders has each customer placed, including customers with none?
SELECT c.name, count(o.order_id) AS orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.name
ORDER BY orders DESC, c.name;

-- Q2. Which orders do not belong to any known customer?
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
ORDER BY o.order_id;

-- Q3. What is the delivered revenue per city?
SELECT c.city, sum(o.amount) AS delivered_revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'delivered'
GROUP BY c.city
ORDER BY delivered_revenue DESC;

-- Q4. Which customers have placed more than one order?
SELECT c.name, count(*) AS orders
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.name
HAVING count(*) > 1
ORDER BY orders DESC, c.name;

-- Q5. Which customers have spent more than 1500 on delivered orders?
SELECT c.name, sum(o.amount) AS delivered_spend
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'delivered'
GROUP BY c.name
HAVING sum(o.amount) > 1500
ORDER BY delivered_spend DESC;

-- Q6. How does NULL change count?
SELECT count(*)           AS all_orders,
       count(amount)      AS orders_with_amount,
       count(customer_id) AS orders_with_customer
FROM orders;

-- Q7. Which customers have no city? (= NULL finds nothing, IS NULL works)
SELECT 'city = NULL' AS filter, count(*) AS customers FROM customers WHERE city = NULL
UNION ALL
SELECT 'city IS NULL', count(*) FROM customers WHERE city IS NULL;

-- Q8. Which customers have never ordered? (NOT IN breaks when the list has a NULL)
SELECT 'NOT IN' AS method, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
UNION ALL
SELECT 'NOT EXISTS', name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY method, name;

-- Q9. What is the latest order of each customer?
WITH ranked_orders AS (
    SELECT o.*,
           ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS order_rank
    FROM orders o
)
SELECT c.name, r.order_id, r.order_date, r.amount
FROM ranked_orders r
JOIN customers c ON c.customer_id = r.customer_id
WHERE r.order_rank = 1
ORDER BY c.name;

-- Q10. Which customers spend more per order than the average customer?
WITH customer_spend AS (
    SELECT o.customer_id, avg(o.amount) AS avg_order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY o.customer_id
),
overall AS (
    SELECT avg(avg_order_value) AS avg_customer_value FROM customer_spend
)
SELECT c.name, round(s.avg_order_value, 2) AS avg_order_value, round(o.avg_customer_value, 2) AS avg_customer_value
FROM customer_spend s
JOIN customers c ON c.customer_id = s.customer_id
CROSS JOIN overall o
WHERE s.avg_order_value > o.avg_customer_value
ORDER BY avg_order_value DESC;
