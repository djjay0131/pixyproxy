```sql
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

```