CREATE TABLE `fing`.`datos` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pc` VARCHAR(45) NULL,
  `timestamp` TIMESTAMP NULL,
  `state` VARCHAR(45) NULL,
  `on_time` INT NULL,
  `users` INT NULL,
  `process` INT NULL,
  `process_active` INT NULL,
  `process_sleep` INT NULL,
  `process_per_user` VARCHAR(500) NULL,
  `cpu_use` DECIMAL(10,2) NULL,
  `memory_use` DECIMAL(10,2) NULL,
  PRIMARY KEY (`id`))
COMMENT = 'Tabla que almacena los datos recibidos de las pc';
