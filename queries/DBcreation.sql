-- Create Database
CREATE DATABASE FilmCatalog;

USE FilmCatalog;

-- Create the Movies table
CREATE TABLE Movies (
    movieId INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    tagline VARCHAR(255),
    overview TEXT,
    language VARCHAR(10),
    releaseDate DATE,
    runtime INTEGER,
    voteAverage FLOAT,
    voteCount INTEGER,
    budget INTEGER
);

-- Create the Genres table
CREATE TABLE Genres (
    genreId INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create link between genres and movies
CREATE TABLE MovieGenres (
    movieId INTEGER NOT NULL,
    genreId INTEGER NOT NULL,
    PRIMARY KEY (movieId, genreId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (genreId) REFERENCES Genres(genreId) ON DELETE CASCADE
);

-- Create the Countries table
CREATE TABLE Countries (
    countryId INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create link between countries and movies
CREATE TABLE MovieCountries (
    movieId INTEGER NOT NULL,
    countryId INTEGER NOT NULL,
    PRIMARY KEY (movieId, countryId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (countryId) REFERENCES Countries(countryId) ON DELETE CASCADE
);

-- Create the Production Companies table
CREATE TABLE Companies (
    companyId INTEGER PRIMARY KEY,
    name VARCHAR(255)
);

-- Create link between companies and movies
CREATE TABLE MovieCompanies (
    movieId INTEGER NOT NULL,
    companyId INTEGER NOT NULL,
    PRIMARY KEY (movieId, companyId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (companyId) REFERENCES Companies(companyId) ON DELETE CASCADE
);

-- Create the Keywords table
CREATE TABLE Keywords (
    keywordId INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

-- Create link between keywords and movies
CREATE TABLE MovieKeywords (
    movieId INTEGER NOT NULL,
    keywordId INTEGER NOT NULL,
    PRIMARY KEY (movieId, keywordId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (keywordId) REFERENCES Keywords(keywordId) ON DELETE CASCADE
);

-- Create the Users table
CREATE TABLE Users (
    userId INTEGER AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    emailAddress VARCHAR(255) NOT NULL UNIQUE,
    createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    userRole ENUM('normal', 'moderator', 'admin') DEFAULT 'normal'
);

-- Isolate the passwords
CREATE TABLE UserPasswords (
    authId INTEGER AUTO_INCREMENT PRIMARY KEY,
    userId INTEGER NOT NULL UNIQUE,
    passwordHash TEXT NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- Create the Comments table
CREATE TABLE Comments (
    commentId INTEGER AUTO_INCREMENT PRIMARY KEY,
    movieId INTEGER NOT NULL,
    userId INTEGER NOT NULL,
    commentText TEXT,
    timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    isFlagged BOOLEAN DEFAULT false,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- Create the Ratings table
CREATE TABLE Ratings (
    movieId INTEGER NOT NULL,
    userId INTEGER NOT NULL,
    rating FLOAT,
    PRIMARY KEY (movieId, userId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);
