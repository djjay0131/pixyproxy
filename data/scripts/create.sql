-- MySQL Script
-- File: /data/scripts/create.sql
"""
This script is used to set up the initial database for the PixyProxy system.

It first sets the character set and collation for the connection to UTF-8, which supports a wide range of characters and is suitable for international applications.

Then, it drops the `pixyproxy` database if it already exists, and creates a new `pixyproxy` database with the UTF-8 character set and collation.

Next, it creates a new MySQL user named 'pixyproxy' if it doesn't already exist, and sets its password to 'pixyproxy'.

Finally, it grants all privileges on the `pixyproxy` database to the 'pixyproxy' user and flushes the privileges to ensure they take effect immediately.

Author: djjay
Date: 2024-03-20
"""

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

DROP DATABASE IF EXISTS `pixyproxy`;

CREATE DATABASE `pixyproxy`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'pixyproxy'@'localhost' IDENTIFIED BY 'pixyproxy';

GRANT ALL PRIVILEGES ON `pixyproxy`.* TO 'pixyproxy'@'localhost';

FLUSH PRIVILEGES;