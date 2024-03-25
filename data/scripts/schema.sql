-- MySQL Script
-- File: /data/scripts/schema.sql
"""
This script is used to create the `images` table in the `pixyproxy` database for the PixyProxy system.

The `images` table has the following columns:
- `id`: an auto-incrementing integer that serves as the primary key.
- `guid`: a unique identifier for each image.
- `filename`: the name of the file where the image is stored.
- `prompt`: the text prompt used to generate the image.
- `created_at`: the timestamp when the image record was created.
- `updated_at`: the timestamp when the image record was last updated.

The script also creates several indexes on the `images` table to improve query performance:
- A unique index on the `guid` column to ensure that each image has a unique GUID and to speed up lookups by GUID.
- Non-unique indexes on the `filename`, `created_at`, and `updated_at` columns to speed up queries that filter or sort by these columns.

Author: djjay
Date: 2024-03-20
"""

USE `pixyproxy`;

CREATE TABLE `images` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `guid` VARCHAR(36) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `prompt` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Images_U1` (`guid`),
  KEY `Images_I1` (`filename`),
  KEY `Images_I2` (`created_at`),
  KEY `Images_I3` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;