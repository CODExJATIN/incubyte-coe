CREATE OR REPLACE TABLE newsletter_2024 AS
SELECT * FROM (VALUES
    ('asha@example.com'),
    ('ravi@example.com'),
    ('meera@example.com'),
    ('ravi@example.com')
) AS t(email);

CREATE OR REPLACE TABLE newsletter_2025 AS
SELECT * FROM (VALUES
    ('ravi@example.com'),
    ('karan@example.com'),
    ('nisha@example.com')
) AS t(email);

SELECT email FROM newsletter_2024
UNION
SELECT email FROM newsletter_2025
ORDER BY email;

SELECT email FROM newsletter_2024
UNION ALL
SELECT email FROM newsletter_2025
ORDER BY email;

SELECT email FROM newsletter_2024
INTERSECT
SELECT email FROM newsletter_2025;

SELECT email FROM newsletter_2024
EXCEPT
SELECT email FROM newsletter_2025
ORDER BY email;

SELECT email, 2024 AS year FROM newsletter_2024
UNION ALL
SELECT email, 2025 AS year FROM newsletter_2025
ORDER BY email, year;

SELECT 'asha@example.com' AS email, 'Pune' AS city
UNION ALL BY NAME
SELECT 'karan@example.com' AS email, DATE '2025-05-01' AS joined_on;
