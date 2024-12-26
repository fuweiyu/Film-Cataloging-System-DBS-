-- Step 1: Use the film_cataloging_db
USE film_cataloging_db;

-- Step 2: Create the PassHash table
CREATE TABLE PassHash (
    authId INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    passwordHash VARCHAR(255) NOT NULL,
    FOREIGN KEY (userName) REFERENCES Users(userName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

