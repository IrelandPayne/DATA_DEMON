-- Given a table of candidates and their skills, youre 
-- tasked with finding the candidates best suited for an open Data Science job. 
-- You want to find candidates who are proficient in Python, Tableau, and PostgreSQL.

-- Write a query to list the candidates who possess all of the required skills for the job. Sort the output by candidate ID in ascending order.
SELECT candidate_id 
FROM candidates 
WHERE skill IN ('Python', 'Tableau', 'PostgreSQL') 
GROUP BY candidate_id 
HAVING COUNT(skill) = 3 
ORDER BY candidate_id ASC;

-- Assume you're given two tables containing data about Facebook Pages and their respective likes (as in "Like a Facebook Page").

-- Write a query to return the IDs of the Facebook pages that have zero likes. 
-- The output should be sorted in ascending order based on the page IDs.
SELECT pages.page_id
FROM pages
LEFT JOIN page_likes 
  USING (page_id)
WHERE page_likes.page_id IS NULL
ORDER BY pages.page_id; 

-- Tesla is investigating production bottlenecks and they need your help to extract the relevant data. Write a query to determine which parts have begun the assembly process but are not yet finished.

-- Assumptions:

-- parts_assembly table contains all parts currently in production, each at varying stages of the assembly process.
-- An unfinished part is one that lacks a finish_date.
-- This question is straightforward, so let's approach it with simplicity in both thinking and solution.
SELECT
  part,
  assembly_step
FROM parts_assembly
WHERE finish_date IS NULL;

-- Assume you're given the table on user viewership categorised by device type where the three types are laptop, tablet, and phone.

-- Write a query that calculates the total viewership for laptops and mobile devices 
-- where mobile is defined as the sum of tablet and phone viewership. Output the total 
-- viewership for laptops as laptop_reviews and the total viewership for mobile devices as mobile_views.
SELECT
  SUM(CASE WHEN device_type = 'laptop' THEN 1 ELSE 0 END) AS laptop_views,
  SUM(CASE WHEN device_type IN ('tablet', 'phone') THEN 1 ELSE 0 END) AS mobile_views
FROM viewership;

-- Given a table of Facebook posts, for each user who posted at least twice in 2021, write a query to find the number 
-- of days between each user’s first post of the year and last post of the year in the year 2021. 
-- Output the user and number of the days between each user's first and last post.
SELECT 
    user_id, 
    DATEDIFF(MAX(DATE(post_date)), MIN(DATE(post_date))) AS days_between
FROM posts
WHERE YEAR(post_date) = 2021
GROUP BY user_id
HAVING COUNT(post_id) > 1;

-- Write a query to identify the top 2 Power Users who sent the highest number of messages on Microsoft Teams in August 2022. 
-- Display the IDs of these 2 users along with the total number of messages they sent. Output the results in descending order based on the count 
-- of the messages.
SELECT 
  sender_id, 
  COUNT(message_id) AS count_messages
FROM messages
WHERE sent_date >= '2022-08-01' AND sent_date < '2022-09-01'
GROUP BY sender_id
ORDER BY count_messages DESC
LIMIT 2;

-- OR 
SELECT 
  sender_id, 
  COUNT(message_id) AS count_messages
FROM messages
WHERE EXTRACT(MONTH FROM sent_date) = '8'
  AND EXTRACT(YEAR FROM sent_date) = '2022'
GROUP BY sender_id
ORDER BY count_messages DESC
LIMIT 2;

-- Assume you're given a table containing job postings from various companies on the 
-- LinkedIn platform. Write a query to retrieve the count of companies that have posted 
-- duplicate job listings.

-- step 1: find which companies have dupes: 
SELECT 
  company_id, 
  title, 
  description, 
  COUNT(job_id) AS job_count
FROM job_listings
GROUP BY company_id, title, description;

-- then solve: 
WITH job_count_cte AS (
  SELECT 
    company_id, 
    title, 
    description, 
    COUNT(job_id) AS job_count
  FROM job_listings
  GROUP BY company_id, title, description
)

SELECT COUNT(DISTINCT company_id) AS duplicate_companies
FROM job_count_cte
WHERE job_count > 1;

-- OR: 
SELECT COUNT(DISTINCT company_id) AS duplicate_companies
FROM (
  SELECT 
    company_id, 
    title, 
    description, 
    COUNT(job_id) AS job_count
  FROM job_listings
  GROUP BY company_id, title, description
) AS job_count_cte
WHERE job_count > 1;

-- Assume you're given the tables containing completed trade orders and user details in a Robinhood trading system.
-- Write a query to retrieve the top three cities that have the highest number of completed trade orders listed in descending order. 
-- Output the city name and the corresponding number of completed trade orders.
SELECT 
  users.city, 
  COUNT(trades.order_id) AS total_orders 
FROM trades 
JOIN users 
  ON trades.user_id = users.user_id 
WHERE trades.status = 'Completed' 
GROUP BY users.city 
ORDER BY total_orders DESC
LIMIT 3;

-- Given the reviews table, write a query to retrieve the average star rating for each 
-- product, grouped by month. The output should display the month as a numerical value, 
-- product ID, and average star rating rounded to two decimal places. Sort the output first 
-- by month and then by product ID.
SELECT
  EXTRACT(MONTH FROM submit_date) AS mth,
  product_id AS product,
  ROUND(AVG(stars), 2) AS avg_stars
FROM reviews
GROUP BY 
    EXTRACT(MONTH FROM submit_date), 
    product
ORDER BY mth, product;
-- group by clause is executed before select, reasoning why we cannot group by mth and have to write out the whole function

-- Companies often perform salary analyses to ensure fair compensation practices. 
-- One useful analysis is to check if there are any employees earning more than their direct managers.
-- As a HR Analyst, you're asked to identify all employees who earn more than their direct managers. The result should include the employee's ID and name.
SELECT 
  emp.employee_id AS employee_id,
  emp.name AS employee_name
FROM employee AS mgr
INNER JOIN employee AS emp
  ON mgr.employee_id = emp.manager_id
WHERE emp.salary > mgr.salary;

-- Assume you have an events table on Facebook app analytics. Write a query to calculate 
-- the click-through rate (CTR) for the app in 2022 and round the results to 2 decimal places.
SELECT 
  app_id, 
  ROUND(100.0 * SUM(CASE 
    WHEN event_type = 'click' THEN 1 ELSE 0 END)
  /
  SUM(CASE 
    WHEN event_type = 'impression' THEN 1 ELSE 0 END), 2) AS ctr
FROM events 
WHERE EXTRACT(YEAR FROM timestamp) = '2022'
GROUP BY app_id; 

-- OR 
SELECT 
  app_id, 
  ROUND(100.0 * 
  COUNT(CASE WHEN event_type = 'click' THEN 1 ELSE NULL END) /
  COUNT(CASE WHEN event_type = 'impression' THEN 1 ELSE NULL END), 2) AS ctr
FROM events 
WHERE EXTRACT(YEAR FROM timestamp) = '2022'
GROUP BY app_id; 

-- or for extracting the date you could just use: 
-- WHERE timestamp >= '2022-01-01' AND timestamp < '2023-01-01'

-- Assume you're given tables with information about TikTok user sign-ups and confirmations through 
-- email and text. New users on TikTok sign up using their email addresses, and upon sign-up, each user 
-- receives a text message confirmation to activate their account.

-- Write a query to display the user IDs of those who did not confirm their sign-up on the 
-- first day, but confirmed on the second day.
SELECT 
  emails.user_id
FROM emails 
JOIN texts 
  USING (email_id)
WHERE texts.signup_action = 'confirmed'
  AND texts.action_date = DATE_ADD(emails.signup_date, INTERVAL 1 DAY)

-- Display the number of unique queries as histogram categories, along with the count of employees who executed 
-- that number of unique queries.
WITH employee_queries AS (
  SELECT 
    e.employee_id,
    COALESCE(COUNT(DISTINCT q.query_id), 0) AS unique_queries
  FROM employees AS e
  LEFT JOIN queries AS q
    ON e.employee_id = q.employee_id
      AND q.query_starttime >= '2023-07-01T00:00:00Z'
      AND q.query_starttime < '2023-10-01T00:00:00Z'
  GROUP BY e.employee_id
)

SELECT
  unique_queries,
  COUNT(employee_id) AS employee_count
FROM employee_queries
GROUP BY unique_queries
ORDER BY unique_queries;

--- Where clauses 
SELECT * FROM customers
WHERE age BETWEEN 18 AND 22
AND state IN ('Victoria', 'Tasmania', 'Queensland')
AND gender != 'n/a'
AND (customer_name LIKE 'A%' OR customer_name LIKE 'B%');

-- group by 
SELECT 
  ticker,
  MIN(open) AS min
FROM stock_prices
GROUP BY ticker
ORDER BY min DESC;

-- another group by praccy 
SELECT 
  skill, 
  COUNT(skill) AS count
FROM candidates
GROUP BY skill
ORDER BY count DESC;

-- having review 
SELECT 
  ticker,
  MIN(open) AS min
FROM stock_prices
GROUP BY ticker
HAVING MIN(open) > 100;

-- comment: having is executed before select (so is group by), 
-- so have to write out what we are filtering; cannot use aliases

SELECT 
  candidate_id
FROM candidates 
GROUP BY candidate_id
HAVING COUNT(skill) > 2;

-- even tho we are only selecting by non-aggregates, we are still filtering by them, 
-- reasoning why we still have a group by. The group by creates one column which is not affected by the having clause

--- complete by tonight: 
-- 1. WHERE vs HAVING
-- 2. INNER JOIN vs LEFT JOIN
-- 3️. GROUP BY + Aggregate Functions
-- 4️. Find the 2nd/3rd highest salary
-- 5️ RANK() vs DENSE_RANK() vs ROW_NUMBER()
-- 6️ CTE vs Subquery
-- 7️ Find duplicate records
-- 8️ Find employees earning more than their manager
-- 9️ CASE WHEN
-- 10 Running Total using Window Functions
-- 11 COUNT(*) vs COUNT(column) vs COUNT(DISTINCT column)
-- 12 Handling NULL values
-- 13 Top N employees from each department
-- 14 DELETE vs TRUNCATE vs DROP
-- 15 SQL Query Execution Order

🐍 Python - Focus on these

1️⃣ List vs Tuple vs Set vs Dictionary
2️⃣ Mutable vs Immutable
3️⃣ Functions & Lambda Functions
4️⃣ for loop vs while loop
5️⃣ List Comprehension
6️⃣ Exception Handling
7️⃣ Handling Missing Values with Pandas
8️⃣ Filtering DataFrames
9️⃣ GroupBy in Pandas
🔟 Merge vs Join
1️⃣1️⃣ Removing Duplicates
1️⃣2️⃣ loc vs iloc
1️⃣3️⃣ Reading CSV/Excel files
1️⃣4️⃣ Data Cleaning using Pandas
1️⃣5️⃣ Basic EDA using Python
