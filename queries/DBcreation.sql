-- Create Database
CREATE DATABASE FilmCatalog;

USE FilmCatalog;

-- Create the Movies table
CREATE TABLE Movies (
    movieId INTEGER PRIMARY KEY AUTO_INCREMENT,
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
    userRole ENUM('normal', 'admin') DEFAULT 'normal'
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
    FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- Create the Ratings table
CREATE TABLE Ratings (
        movieId INT NOT NULL,
        userId INT NOT NULL,
        rating DECIMAL(3, 2) NOT NULL,
        PRIMARY KEY (movieId, userId),
        FOREIGN KEY (movieId) REFERENCES Movies(movieId) ON DELETE CASCADE,
        FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);
