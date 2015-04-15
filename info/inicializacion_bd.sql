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

CREATE TABLE "maquinas_salon" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(200) NOT NULL,
    "lugar" varchar(200) NOT NULL,
    "prioridad" integer NOT NULL
)
;
CREATE TABLE "maquinas_pc" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "salon_id" integer NOT NULL REFERENCES "maquinas_salon" ("id"),
    "nombre" varchar(200) NOT NULL,
    "mac" varchar(200) NOT NULL,
    "so" varchar(100) NOT NULL,
    "ram" integer NOT NULL,
    "cpu" decimal NOT NULL,
    "arq" varchar(50) NOT NULL,
    "cant_cores" integer NOT NULL,
    "estado" varchar(50) NOT NULL
)
;
CREATE TABLE "maquinas_registropc" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "pc_id" integer NOT NULL REFERENCES "maquinas_pc" ("id"),
    "fecha_alta" datetime NOT NULL
)
;
CREATE TABLE "maquinas_lecturatop" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "pc_id" integer NOT NULL REFERENCES "maquinas_pc" ("id"),
    "tiempo_lectura" datetime NOT NULL,
    "cant_usuarios" integer NOT NULL,
    "mem_perc" integer NOT NULL,
    "cpu_perc" integer NOT NULL
)
;

COMMIT;
