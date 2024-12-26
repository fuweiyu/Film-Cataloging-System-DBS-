-- Step 1: Use the film_cataloging_db
USE film_cataloging_db;

-- Step 2: Create the Users table
CREATE TABLE Users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    emailAddress VARCHAR(100) NOT NULL UNIQUE,
    createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    userRole ENUM('normal', 'moderator', 'admin') DEFAULT 'normal'
);

