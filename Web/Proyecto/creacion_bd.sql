CREATE TABLE `maquinas_salon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `lugar` varchar(200) NOT NULL,
  `prioridad` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `maquinas_registropc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_alta` datetime NOT NULL,
  `pc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Maquinas_registropc_01ced8be` (`pc_id`),
  CONSTRAINT `Maquinas_registropc_pc_id_2a6ffe70_fk_Maquinas_pc_id` FOREIGN KEY (`pc_id`) REFERENCES `maquinas_pc` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

CREATE TABLE `maquinas_pc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `mac` varchar(200) NOT NULL,
  `so` varchar(200) NOT NULL,
  `ram` varchar(200) NOT NULL,
  `cpu` varchar(200) NOT NULL,
  `estado` varchar(200) NOT NULL,
  `cant_usuarios` int(11) NOT NULL,
  `salon_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Maquinas_pc_72ee9dc3` (`salon_id`),
  CONSTRAINT `Maquinas_pc_salon_id_45951068_fk_Maquinas_salon_id` FOREIGN KEY (`salon_id`) REFERENCES `maquinas_salon` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
