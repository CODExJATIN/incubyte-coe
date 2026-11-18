CREATE OR REPLACE TABLE sales AS
SELECT * FROM (VALUES
    ('Pune',      DATE '2025-01-01', 1200),
    ('Pune',      DATE '2025-02-01',  900),
    ('Pune',      DATE '2025-03-01',  900),
    ('Pune',      DATE '2025-04-01', 1500),
    ('Mumbai',    DATE '2025-01-01', 3000),
    ('Mumbai',    DATE '2025-02-01', 2500),
    ('Mumbai',    DATE '2025-03-01', 3500),
    ('Mumbai',    DATE '2025-04-01', 3100),
    ('Bengaluru', DATE '2025-01-01',  800),
    ('Bengaluru', DATE '2025-02-01', 1100),
    ('Bengaluru', DATE '2025-03-01', 1300),
    ('Bengaluru', DATE '2025-04-01', 1250)
) AS t(city, month, revenue);

SELECT city, sum(revenue) AS city_total FROM sales GROUP BY city ORDER BY city;

SELECT city, month, revenue,
       sum(revenue) OVER (PARTITION BY city) AS city_total,
       round(100.0 * revenue / sum(revenue) OVER (PARTITION BY city), 1) AS pct_of_city
FROM sales
ORDER BY city, month;

SELECT city, month, revenue,
       row_number() OVER w AS row_number,
       rank()       OVER w AS rank,
       dense_rank() OVER w AS dense_rank
FROM sales
WHERE city = 'Pune'
WINDOW w AS (PARTITION BY city ORDER BY revenue DESC)
ORDER BY revenue DESC;

SELECT city, month, revenue,
       sum(revenue) OVER (PARTITION BY city ORDER BY month) AS running_total
FROM sales
ORDER BY city, month;

SELECT city, month, revenue,
       lag(revenue) OVER (PARTITION BY city ORDER BY month) AS prev_month,
       revenue - lag(revenue) OVER (PARTITION BY city ORDER BY month) AS change
FROM sales
ORDER BY city, month;

SELECT city, month, revenue,
       round(avg(revenue) OVER (
           PARTITION BY city ORDER BY month
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 1) AS moving_avg_3m
FROM sales
ORDER BY city, month;

SELECT city, month, revenue
FROM sales
QUALIFY row_number() OVER (PARTITION BY city ORDER BY revenue DESC) = 1
ORDER BY city;
