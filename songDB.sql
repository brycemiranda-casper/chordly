CREATE DATABASE chordify_audio;
USE chordify_audio;
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    fingerprint LONGTEXT NOT NULL
);
DESCRIBE songs;

