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
  assembly_step,
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