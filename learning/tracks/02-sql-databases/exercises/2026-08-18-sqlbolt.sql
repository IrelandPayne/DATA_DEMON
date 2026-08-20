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

-- 