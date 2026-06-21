CREATE DATABASE IF NOT EXISTS ontozo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ontozo;

CREATE TABLE IF NOT EXISTS daily_moisture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_uid VARCHAR(64) NOT NULL,
    date DATE NOT NULL,
    avg_moisture FLOAT NOT NULL,
    received_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_device_date (device_uid, date)
);
