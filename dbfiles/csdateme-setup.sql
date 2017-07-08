DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(16) NOT NULL,
   password VARCHAR(256) NOT NULL,
   email VARCHAR(64) NOT NULL,
   token VARCHAR(256) DEFAULT NULL,
   tokenTime TIMESTAMP NULL,
   salt VARCHAR(256)
);


CREATE TABLE Questions (
   id INT AUTO_INCREMENT PRIMARY KEY,
   completed BOOLEAN,
   firstName VARCHAR(32),
   middleName VARCHAR(32) DEFAULT NULL,
   lastName VARCHAR(32),
   gender VARCHAR(1),
   state VARCHAR(32),
   city VARCHAR(32),
   birthday DATE,
   favoriteOS VARCHAR(16),
   phoneOS VARCHAR(16),
   relationship VARCHAR(32),
   gaming VARCHAR(32),
   favLang1 VARCHAR(32),
   favLang2 VARCHAR(32) DEFAULT NULL,
   favLang3 VARCHAR(32) DEFAULT NULL,
   favHobby1 VARCHAR(32),
   favHobby2 VARCHAR(32) DEFAULT NULL,
   favHobby3 VARCHAR(32) DEFAULT NULL,
   wpm INTEGER,
   pic VARCHAR(32),
   bio VARCHAR(256),
   interestedIn VARCHAR(1)
);
