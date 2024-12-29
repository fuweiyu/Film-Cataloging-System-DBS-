-- Populate the movies info table:
LOAD DATA INFILE '/var/lib/mysql-files/CleanData/movies_data.csv'
IGNORE
INTO TABLE Movies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@movieId, title, tagline, overview, language, @releaseDate, @runtime, @voteAverage, voteCount, budget)
SET
    movieId = CASE
        WHEN @movieId REGEXP '^[0-9]+$' THEN @movieId
        ELSE NULL -- Skip invalid movie IDs
    END,
    releaseDate = CASE
        WHEN @releaseDate = '' THEN NULL
        ELSE @releaseDate
    END,
    runtime = CASE
        WHEN @runtime = '' THEN NULL
        ELSE @runtime
    END,
    voteAverage = CASE
        WHEN @voteAverage = 'False' THEN 0
        ELSE @voteAverage
    END;

-- Populate Keywords table
LOAD DATA INFILE '/var/lib/mysql-files/CleanData/keywords/keywords.csv'
	INTO TABLE Keywords 
	FIELDS TERMINATED BY ',' 
	ENCLOSED BY '"' 
	LINES TERMINATED BY '\n' 
	IGNORE 1 ROWS (keywordId, name);

-- Populate MovieKeyword table (BRIDGE)
LOAD DATA INFILE '/var/lib/mysql-files/CleanData/keywords/movie_keywords.csv' 
	INTO TABLE MovieKeywords 
	FIELDS TERMINATED BY ',' 
	ENCLOSED BY '"' 
	LINES TERMINATED BY '\n' 
	IGNORE 1 ROWS (movieId, keywordId);

-- Populate ArtificialUserInformation
LOAD DATA INFILE '/var/lib/mysql-files/ArtificialUserInformation/Users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(userId, userName, emailAddress, @userRole)
SET userRole = CASE
	WHEN @userRole IN ('normal', 'admin') THEN @userRole
	ELSE 'normal'
END;

LOAD DATA INFILE '/var/lib/mysql-files/ArtificialUserInformation/UserPasswords.csv'
INTO TABLE UserPasswords
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(userId, passwordHash);


CREATE TEMPORARY TABLE TempRatings (
userId INT,
movieId INT,
rating DECIMAL(3, 2)
);

LOAD DATA INFILE '/var/lib/mysql-files/CleanData/ratings/ratings.csv'
INTO TABLE TempRatings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(userId, movieId, rating);

INSERT INTO Ratings (movieId, userId, rating)
	SELECT movieId, userId, rating
	FROM TempRatings
	WHERE movieId IN (SELECT movieId FROM Movies)
	AND userId IN (SELECT userId FROM Users);

