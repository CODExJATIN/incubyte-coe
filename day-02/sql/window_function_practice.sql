-- SQL Window Functions Practice
-- Compatible with PostgreSQL and DuckDB

-- =========================================================
-- 1. Create the sample employees table
-- =========================================================

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary INTEGER
);

INSERT INTO employees (emp_id, name, department, salary) VALUES
    (1, 'Rahul',  'IT',    60000),
    (2, 'Priya',  'IT',    80000),
    (3, 'Amit',   'IT',    70000),
    (4, 'Neha',   'HR',    50000),
    (5, 'Raj',    'HR',    65000),
    (6, 'Sneha',  'HR',    75000),
    (7, 'Karan',  'Sales', 45000),
    (8, 'Meera',  'Sales', 55000);

-- View the sample data
SELECT *
FROM employees
ORDER BY department, salary;


-- =========================================================
-- 2. ROW_NUMBER(): Number employees within each department
--    Highest salary gets row number 1.
-- =========================================================

SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS row_num
FROM employees
ORDER BY department, salary DESC;


-- =========================================================
-- 3. Find the second-highest-paid employee in each department
--    ROW_NUMBER() returns exactly one row per department.
--    If salaries are tied, add a tie-breaker such as emp_id.
-- =========================================================

WITH ranked_employees AS (
    SELECT
        name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC, emp_id
        ) AS rn
    FROM employees
)
SELECT
    name,
    department,
    salary
FROM ranked_employees
WHERE rn = 2
ORDER BY department;


-- =========================================================
-- 4. RANK(): Rank employees across the whole company
--    (No PARTITION BY, so all employees are in one ranking.)
-- =========================================================

SELECT
    name,
    department,
    salary,
    RANK() OVER (
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees
ORDER BY salary DESC;


-- =========================================================
-- 5. RANK(): Rank employees separately within each department
-- =========================================================

SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS dept_rank
FROM employees
ORDER BY department, salary DESC;


-- =========================================================
-- 6. DENSE_RANK(): Top 2 distinct salary levels per department
--    Includes all employees tied at either of the top 2 levels.
-- =========================================================

WITH ranked_employees AS (
    SELECT
        name,
        department,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS rnk
    FROM employees
)
SELECT
    name,
    salary,
    department
FROM ranked_employees
WHERE rnk <= 2
ORDER BY department, salary DESC;


-- =========================================================
-- 7. AVG() OVER(): Show each employee with their department average
-- =========================================================

SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (
        PARTITION BY department
    ) AS dept_avg
FROM employees
ORDER BY department, salary;


-- =========================================================
-- 8. Employees earning more than their department average
--    A CTE lets us filter the calculated window value.
-- =========================================================

WITH emp_with_dept_avg AS (
    SELECT
        name,
        department,
        salary,
        AVG(salary) OVER (
            PARTITION BY department
        ) AS dept_avg
    FROM employees
)
SELECT
    name,
    department,
    salary,
    dept_avg
FROM emp_with_dept_avg
WHERE salary > dept_avg
ORDER BY department, salary DESC;


-- =========================================================
-- 9. LAG(): Show the previous salary within each department
--    Employees are ordered from lowest salary to highest.
-- =========================================================

SELECT
    name,
    department,
    salary,
    LAG(salary) OVER (
        PARTITION BY department
        ORDER BY salary ASC
    ) AS prev_salary
FROM employees
ORDER BY department, salary ASC;


-- =========================================================
-- 10. LEAD(): Show the next salary within each department
--     Employees are ordered from lowest salary to highest.
-- =========================================================

SELECT
    name,
    department,
    salary,
    LEAD(salary) OVER (
        PARTITION BY department
        ORDER BY salary ASC
    ) AS next_salary
FROM employees
ORDER BY department, salary ASC;


-- =========================================================
-- 11. SUM() OVER(): Running salary total per department
-- =========================================================

SELECT
    name,
    department,
    salary,
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY salary ASC
    ) AS running_total
FROM employees
ORDER BY department, salary ASC;


-- =========================================================
-- 12. Running total with an explicit window frame
--     From the first row in the department through the current row.
-- =========================================================

SELECT
    name,
    department,
    salary,
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY salary ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM employees
ORDER BY department, salary ASC;


-- =========================================================
-- 13. CHALLENGE: Employees earning more than the previous
--     employee's salary in their department.
--     LAG() returns NULL for the first employee in each department.
-- =========================================================

WITH employee_salary_comparison AS (
    SELECT
        name,
        department,
        salary,
        LAG(salary) OVER (
            PARTITION BY department
            ORDER BY salary ASC
        ) AS prev_salary
    FROM employees
)
SELECT
    name,
    department,
    salary,
    prev_salary
FROM employee_salary_comparison
WHERE salary > prev_salary
ORDER BY department, salary ASC;


-- =========================================================
-- Quick reference
-- =========================================================
-- ROW_NUMBER()  : Unique sequential number for each row in a window.
-- RANK()        : Ties share a rank; later ranks may have gaps.
-- DENSE_RANK()  : Ties share a rank; no gaps in later ranks.
-- LAG(column)   : Value from a preceding row.
-- LEAD(column)  : Value from a following row.
-- SUM() OVER()  : Aggregate while keeping individual rows.
-- AVG() OVER()  : Average while keeping individual rows.
-- PARTITION BY  : Splits rows into independent windows.
-- ORDER BY      : Defines row order inside the window.
-- WHERE         : Filters rows; use an outer query/CTE to filter
--                 results of window functions.