DROP DATABASE IF EXISTS Music;
CREATE DATABASE Music;
USE Music;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(50),
    PRIMARY KEY(username)
) ENGINE INNODB;

DROP TABLE IF EXISTS Genres;
CREATE TABLE Genres (
    genre VARCHAR(50) NOT NULL,
    PRIMARY KEY (genre)
) ENGINE INNODB;

INSERT INTO Genres(genre) VALUES ("Hip-Hop/Rap");

DROP TABLE IF EXISTS Artists;
CREATE TABLE Artists (
	artist VARCHAR(300) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    FOREIGN KEY (genre) REFERENCES Genres(genre) ON DELETE CASCADE,
    PRIMARY KEY (artist)
) ENGINE INNODB;

DROP TABLE IF EXISTS Songs;
CREATE TABLE Songs (
    songID INT NOT NULL AUTO_INCREMENT,
    artist VARCHAR(300) NOT NULL,
    song_name VARCHAR(300) NOT NULL,
    features VARCHAR(300) NOT NULL,
    genre VARCHAR(300) NOT NULL,
    link VARCHAR(300) NOT NULL,
    release_date DATE NOT NULL,
    FOREIGN KEY (artist) REFERENCES Artists(artist) ON DELETE  CASCADE,
    FOREIGN KEY (genre) REFERENCES Genres(genre) ON DELETE CASCADE,
    PRIMARY KEY (songID, link)
) ENGINE INNODB;

DROP TABLE IF EXISTS Collaborations;
CREATE TABLE Collaborations (
    main_artist VARCHAR(300) NOT NULL,
    feature VARCHAR(300) NOT NULL,
    songID INT,
    FOREIGN KEY (main_artist) REFERENCES Artists(artist) ON DELETE CASCADE,
    FOREIGN KEY (feature) REFERENCES Artists(artist) ON DELETE CASCADE,
    PRIMARY KEY (main_artist, feature, songID)
) ENGINE INNODB;

DROP TABLE IF EXISTS Likes;
CREATE TABLE Likes (
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    artist VARCHAR(50) NOT NULL,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE,
    FOREIGN KEY (artist) REFERENCES Artists(artist) ON DELETE CASCADE,
    FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE,
    PRIMARY KEY (username, artist)
) ENGINE INNODB;

DROP TABLE IF EXISTS Dislikes;
CREATE TABLE Dislikes (
    username VARCHAR(50) NOT NULL,
    artist VARCHAR(50) NOT NULL,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE,
    FOREIGN KEY (artist) REFERENCES Artists(artist) ON DELETE CASCADE,
    PRIMARY KEY (username, artist)
) ENGINE INNODB;