-- sqlbolt practice yayyyyy!!!!

-- Exercise 1: --

-- Find the title of each film
SELECT 
    title
FROM movies; 

-- Find the director of each film
SELECT 
    director
FROM movies;

-- Find the title and director of each film 
SELECT 
    title, director
FROM movies;

-- Find the title and year of each film
SELECT
    title, year
FROM movies; 

-- Find all the information about each film 
SELECT 
    *
FROM movies;

-- Exercise 2: --

-- Find the movie with a row id of 6
SELECT 
    title
FROM movies
WHERE id = 6;

-- Find the movies released in the years between 2000 and 2010
SELECT
    title
FROM movies
WHERE year BETWEEN 2000 AND 2010;

-- Find the movies not released in the years between 2000 and 2010
SELECT
    title
FROM movies
WHERE year NOT BETWEEN 2000 AND 2010;

-- Excersize 3: --

-- Find all the Toy Story movies
SELECT 
    title
FROM movies
WHERE title LIKE "Toy Story%"; 

-- Find all the movies directed by John Lasseter
SELECT 
    title
FROM movies
WHERE director = "John Lasseter";

-- Find all the movies (and director) not directed by John Lasseter
SELECT 
    title, director
FROM movies
WHERE director NOT LIKE "John Lasseter";

-- Find all the WALL-* movies
SELECT 
    title
FROM movies
WHERE title LIKE "WALL-%";

-- Exercise 4: -- 

-- List all directors of Pixar movies (alphabetically), without duplicates
SELECT
    DISTINCT director
FROM movies
ORDER BY director ASC;

-- List the last four Pixar movies released (ordered from most recent to least)
SELECT 
    title
FROM movies
ORDER BY year DESC
LIMIT 4;

-- List the first five Pixar movies sorted alphabetically
SELECT 
    title
FROM movies
ORDER BY title
LIMIT 5;

-- List the next five Pixar movies sorted alphabetically
SELECT 
    title
FROM movies
ORDER BY title
LIMIT 5 OFFSET 5;

-- Exercise 5: --

-- List all the Canadian cities and their populations
SELECT 
    City, Population
FROM North_american_cities
WHERE Country = "Canada";

-- Order all the cities in the United States by their latitude from north to south
SELECT 
    City
FROM North_american_cities
WHERE Country = "United States"
ORDER BY latitude DESC; 

-- List all the cities west of Chicago, ordered from west to east
SELECT
    City
FROM North_american_cities
WHERE longitude < -87.629798
ORDER BY longitude;

-- List the two largest cities in Mexico (by population)
SELECT 
    City
FROM North_american_cities
WHERE Country IS "Mexico"
ORDER BY population DESC
LIMIT 2;

-- List the third and fourth largest cities by population in the United States 
SELECT 
    City
FROM North_american_cities
WHERE Country = "United States"
ORDER BY population DESC
LIMIT 2 OFFSET 2;

-- Exercise 6: --

-- Find the domestic and international sales for each movie
SELECT 
    Title, 
    Domestic_sales, 
    International_sales
FROM movies
JOIN boxoffice 
    ON movies.id = boxoffice.movie_id;

-- Show the sales numbers for each movie that did better internationally rather than domestically
SELECT 
    title, 
    domestic_sales, 
    international_sales
FROM boxoffice
JOIN movies 
    ON movies.id = boxoffice.movie_id
WHERE international_sales > domestic_sales;

-- List all the movies by their ratings in descending order
SELECT 
    title,
    rating
FROM movies 
JOIN boxoffice
    ON boxoffice.movie_id = movies.id 
ORDER BY rating DESC;

-- Exercise 7: -- 

-- Find the list of all buildings that have employees
SELECT 
    DISTINCT building 
FROM employees;

-- Find the list of all buildings and their capacity
SELECT 
    building_name,
    capacity
FROM buildings;

-- List all buildings and the distinct employee roles in each building (including empty buildings)  
SELECT 
    DISTINCT building_name, 
    role 
FROM buildings 
  LEFT JOIN employees
    ON building_name = building;

-- Exercise 8: --

-- Find the name and role of all employees who have not been assigned to a building
SELECT 
    name,
    role
FROM employees
WHERE building IS NULL;

-- Find the names of the buildings that hold no employees
SELECT 
    building_name
FROM buildings
LEFT JOIN employees
    ON building = building_name
WHERE building IS NULL;

-- Exercise 9: --

-- List all movies and their combined sales in millions of dollars
SELECT 
    title,
    (domestic_sales + international_sales) / 1000000 AS combined_sales
FROM boxoffice
    JOIN movies
        ON movies.id = boxoffice.movie_id;

-- List all movies and their ratings in percent
SELECT 
    title,
    (rating * 10) "%" AS rating
FROM movies
JOIN boxoffice
    ON boxoffice.movie_id = movies.id;

-- List all movies that were released on even number years
SELECT
    title
FROM movies
WHERE year % 2 = 0;

-- Exercise 10: -- 

-- Find the longest time that an employee has been at the studio
SELECT 
    name, 
    MAX (years_employed)
FROM employees;

-- For each role, find the average number of years employed by employees in that role
SELECT 
    role,
    AVG(years_employed) AS AVG_years_employed
FROM employees
GROUP BY role;

-- Find the total number of employee years worked in each building
SELECT 
    building,
    SUM (years_employed) AS total_years_employed
FROM employees
GROUP BY building;

-- Exercise 11: --

-- Find the number of Artists in the studio (without a HAVING clause)
SELECT
    role,
    COUNT (role) AS Number_of_artists
FROM employees
WHERE role = "Artist";

-- Find the number of Employees of each role in the studio
SELECT 
    role, 
    COUNT (name)
FROM employees
GROUP BY role;

-- Find the total number of years employed by all Engineers
SELECT 
    role, 
    SUM (years_employed)
FROM employees
GROUP BY role
HAVING role = "Engineer";

-- Exercise 12: -- 

-- Find the number of movies each director has directed
SELECT 
    DISTINCT COUNT(Title) AS "Number of Movies",
    Director
FROM Movies
GROUP BY Director;

-- Find the total domestic and international sales that can be attributed to each director
SELECT 
    SUM(Domestic_sales + International_sales) AS Total_sales,
    Director
FROM boxoffice
    JOIN Movies 
        ON movies.id = boxoffice.movie_id
GROUP BY director;

-- Exercise 13: -- 

-- Add the studio's new production, Toy Story 4 to the list of movies (you can use any director)
INSERT INTO Movies 
VALUES (4, "Toy Story 4", "John Lasseter", NULL, NULL); 

-- Toy Story 4 has been released to critical acclaim! It had a rating of 8.7, and made 340 million domestically and 270 million internationally. Add the record to the BoxOffice table.
INSERT INTO boxoffice
VALUES (4, 8.7, 340000000, 270000000);

-- Exercise 14: --

-- The director for A Bug's Life is incorrect, it was actually directed by John Lasseter
UPDATE movies 
SET Director = "John Lasseter"
WHERE id = 2;

-- The year that Toy Story 2 was released is incorrect, it was actually released in 1999
UPDATE movies
SET Year = 1999
WHERE id = 3;

-- Both the title and director for Toy Story 8 is incorrect! The title should be "Toy Story 3" and it was directed by Lee Unkrich
UPDATE movies
SET Title = "Toy Story 3",
    Director = "Lee Unkrich"
WHERE id = 11;

-- Exercise 15: --

-- This database is getting too big, lets remove all movies that were released before 2005.
DELETE FROM Movies
WHERE Year < 2005;

-- Andrew Stanton has also left the studio, so please remove all movies directed by him.
DELETE FROM Movies
WHERE Director = "Andrew Stanton";

-- Exercise 16: --

-- Create a new table named Database with the following columns:
-- Name A string (text) describing the name of the database
-- Version A number (floating point) of the latest version of this database
-- Download_count An integer count of the number of times this database was downloaded

CREATE TABLE Database (
    id INTEGER PRIMARY KEY,
    Name TEXT,
    Version TEXT,
    Download_count INTEGER
);

-- Exercise 17: --

-- Add a column named Aspect_ratio with a FLOAT data type to store the aspect-ratio each movie was released in.
ALTER TABLE Movies
ADD Aspect_ratio FLOAT;

-- Add another column named Language with a TEXT data type to store the language that the movie was released in. Ensure that the default for this language is English.
ALTER TABLE Movies 
ADD Language TEXT
    DEFAULT "English";

-- Exercise 18: --

-- We've sadly reached the end of our lessons, lets clean up by removing the Movies table
DROP TABLE IF EXISTS Movies;

-- And drop the BoxOffice table as well
DROP TABLE IF EXISTS BoxOffice;

-- DONE. 
-- 