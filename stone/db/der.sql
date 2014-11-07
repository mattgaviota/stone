-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'calendarios'
-- 
-- ---

DROP TABLE IF EXISTS `calendarios`;
		
CREATE TABLE `calendarios` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `desde` DATETIME NOT NULL DEFAULT 'NULL',
  `hasta` DATETIME NOT NULL DEFAULT 'NULL',
  `descripcion` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'dias'
-- 
-- ---

DROP TABLE IF EXISTS `dias`;
		
CREATE TABLE `dias` (
  `fecha` DATETIME NOT NULL DEFAULT 'NULL',
  `tickets_disponibles` INTEGER NOT NULL DEFAULT NULL,
  `tickets_vendidos` INTEGER NOT NULL DEFAULT NULL,
  `evento` VARCHAR(200) NULL DEFAULT NULL,
  `estado` INTEGER NULL DEFAULT NULL,
  `id_calendario` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`fecha`)
);

-- ---
-- Table 'facultades'
-- 
-- ---

DROP TABLE IF EXISTS `facultades`;
		
CREATE TABLE `facultades` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(80) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'feriados'
-- 
-- ---

DROP TABLE IF EXISTS `feriados`;
		
CREATE TABLE `feriados` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `descripcion` VARCHAR(150) NOT NULL DEFAULT 'NULL',
  `fecha` DATETIME NOT NULL DEFAULT 'NULL',
  `tipo` INTEGER NULL DEFAULT NULL,
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'menu'
-- 
-- ---

DROP TABLE IF EXISTS `menu`;
		
CREATE TABLE `menu` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(100) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  `orden` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'log_operaciones'
-- 
-- ---

DROP TABLE IF EXISTS `log_operaciones`;
		
CREATE TABLE `log_operaciones` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `fecha` DATETIME NOT NULL DEFAULT 'NULL',
  `dni` INTEGER NULL DEFAULT NULL,
  `id_tipos_operacion` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'perfiles'
-- 
-- ---

DROP TABLE IF EXISTS `perfiles`;
		
CREATE TABLE `perfiles` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(30) NULL DEFAULT NULL,
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'perfiles_tipos_operaciones'
-- 
-- ---

DROP TABLE IF EXISTS `perfiles_tipos_operaciones`;
		
CREATE TABLE `perfiles_tipos_operaciones` (
  `id_tipos_operacion` INTEGER NULL DEFAULT NULL,
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_perfil` INTEGER NULL DEFAULT NULL,
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'provincias'
-- 
-- ---

DROP TABLE IF EXISTS `provincias`;
		
CREATE TABLE `provincias` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(40) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'tickets'
-- 
-- ---

DROP TABLE IF EXISTS `tickets`;
		
CREATE TABLE `tickets` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `fecha` DATETIME NOT NULL DEFAULT 'NULL',
  `unidad` INTEGER NOT NULL DEFAULT NULL,
  `importe` INTEGER NOT NULL DEFAULT NULL,
  `estado` VARCHAR(50) NOT NULL DEFAULT 'NULL',
  `id_log_usuario` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'tipos_operaciones'
-- 
-- ---

DROP TABLE IF EXISTS `tipos_operaciones`;
		
CREATE TABLE `tipos_operaciones` (
  `id_menu` INTEGER NULL DEFAULT NULL,
  `nombre` VARCHAR(30) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  `controlador` VARCHAR(50) NOT NULL DEFAULT 'NULL',
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `accion` VARCHAR(50) NOT NULL DEFAULT 'NULL',
  `orden` INTEGER NOT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'usuarios'
-- 
-- ---

DROP TABLE IF EXISTS `usuarios`;
		
CREATE TABLE `usuarios` (
  `dni` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(70) NOT NULL DEFAULT 'NULL',
  `password` VARCHAR(32) NOT NULL DEFAULT 'NULL',
  `lu` VARCHAR(10) NOT NULL DEFAULT 'NULL',
  `estado` VARCHAR(email) NOT NULL DEFAULT 'NULL',
  `saldo` DOUBLE NULL DEFAULT 0,
  `id_provincia` INTEGER NULL DEFAULT NULL,
  `id_facultad` INTEGER NULL DEFAULT NULL,
  `id_categoria` INTEGER NULL DEFAULT NULL,
  `id_perfil` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`dni`)
);

-- ---
-- Table 'categorias'
-- 
-- ---

DROP TABLE IF EXISTS `categorias`;
		
CREATE TABLE `categorias` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(20) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'acciones'
-- 
-- ---

DROP TABLE IF EXISTS `acciones`;
		
CREATE TABLE `acciones` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `nombre` VARCHAR(50) NOT NULL DEFAULT 'NULL',
  `created` DATETIME NULL DEFAULT NULL,
  `updated` DATETIME NULL DEFAULT NULL,
  `nombre_canonico` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'log_usuarios'
-- 
-- ---

DROP TABLE IF EXISTS `log_usuarios`;
		
CREATE TABLE `log_usuarios` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_accion` INTEGER NULL DEFAULT NULL,
  `fecha` DATETIME NULL DEFAULT NULL,
  `lugar` INTEGER NULL DEFAULT NULL,
  `dni` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'configuraciones'
-- 
-- ---

DROP TABLE IF EXISTS `configuraciones`;
		
CREATE TABLE `configuraciones` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `puerto` SMALLINT NULL DEFAULT NULL,
  `email` VARCHAR(50) NULL DEFAULT NULL,
  `asunto` VARCHAR(100) NULL DEFAULT NULL,
  `mensaje_email` VARCHAR(300) NULL DEFAULT NULL,
  `password` VARCHAR(50) NULL DEFAULT NULL,
  `charset` VARCHAR(20) NULL DEFAULT NULL,
  `email_type` VARCHAR(10) NULL DEFAULT NULL,
  `smtp` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `dias` ADD FOREIGN KEY (id_calendario) REFERENCES `calendarios` (`id`);
ALTER TABLE `log_operaciones` ADD FOREIGN KEY (dni) REFERENCES `usuarios` (`dni`);
ALTER TABLE `log_operaciones` ADD FOREIGN KEY (id_tipos_operacion) REFERENCES `tipos_operaciones` (`id`);
ALTER TABLE `perfiles_tipos_operaciones` ADD FOREIGN KEY (id_tipos_operacion) REFERENCES `tipos_operaciones` (`id`);
ALTER TABLE `perfiles_tipos_operaciones` ADD FOREIGN KEY (id_perfil) REFERENCES `perfiles` (`id`);
ALTER TABLE `tickets` ADD FOREIGN KEY (fecha) REFERENCES `dias` (`fecha`);
ALTER TABLE `tickets` ADD FOREIGN KEY (id_log_usuario) REFERENCES `log_usuarios` (`id`);
ALTER TABLE `tipos_operaciones` ADD FOREIGN KEY (id_menu) REFERENCES `menu` (`id`);
ALTER TABLE `usuarios` ADD FOREIGN KEY (id_provincia) REFERENCES `provincias` (`id`);
ALTER TABLE `usuarios` ADD FOREIGN KEY (id_facultad) REFERENCES `facultades` (`id`);
ALTER TABLE `usuarios` ADD FOREIGN KEY (id_categoria) REFERENCES `categorias` (`id`);
ALTER TABLE `usuarios` ADD FOREIGN KEY (id_perfil) REFERENCES `perfiles` (`id`);
ALTER TABLE `log_usuarios` ADD FOREIGN KEY (id_accion) REFERENCES `acciones` (`id`);
ALTER TABLE `log_usuarios` ADD FOREIGN KEY (dni) REFERENCES `usuarios` (`dni`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `calendarios` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `dias` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `facultades` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `feriados` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `menu` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `log_operaciones` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `perfiles` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `perfiles_tipos_operaciones` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `provincias` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tickets` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tipos_operaciones` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `usuarios` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `categorias` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `acciones` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `log_usuarios` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `configuraciones` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `calendarios` (`id`,`desde`,`hasta`,`descripcion`) VALUES
-- ('','','','');
-- INSERT INTO `dias` (`fecha`,`tickets_disponibles`,`tickets_vendidos`,`evento`,`estado`,`id_calendario`) VALUES
-- ('','','','','','');
-- INSERT INTO `facultades` (`id`,`nombre`,`created`,`updated`) VALUES
-- ('','','','');
-- INSERT INTO `feriados` (`id`,`descripcion`,`fecha`,`tipo`,`created`,`updated`) VALUES
-- ('','','','','','');
-- INSERT INTO `menu` (`id`,`nombre`,`created`,`updated`,`orden`) VALUES
-- ('','','','','');
-- INSERT INTO `log_operaciones` (`id`,`fecha`,`dni`,`id_tipos_operacion`) VALUES
-- ('','','','');
-- INSERT INTO `perfiles` (`id`,`nombre`,`created`,`updated`) VALUES
-- ('','','','');
-- INSERT INTO `perfiles_tipos_operaciones` (`id_tipos_operacion`,`id`,`id_perfil`,`created`,`updated`) VALUES
-- ('','','','','');
-- INSERT INTO `provincias` (`id`,`nombre`,`created`,`updated`) VALUES
-- ('','','','');
-- INSERT INTO `tickets` (`id`,`fecha`,`unidad`,`importe`,`estado`,`id_log_usuario`) VALUES
-- ('','','','','','');
-- INSERT INTO `tipos_operaciones` (`id_menu`,`nombre`,`created`,`updated`,`controlador`,`id`,`accion`,`orden`) VALUES
-- ('','','','','','','','');
-- INSERT INTO `usuarios` (`dni`,`nombre`,`password`,`lu`,`estado`,`saldo`,`id_provincia`,`id_facultad`,`id_categoria`,`id_perfil`) VALUES
-- ('','','','','','','','','','');
-- INSERT INTO `categorias` (`id`,`nombre`,`created`,`updated`) VALUES
-- ('','','','');
-- INSERT INTO `acciones` (`id`,`nombre`,`created`,`updated`,`nombre_canonico`) VALUES
-- ('','','','','');
-- INSERT INTO `log_usuarios` (`id`,`id_accion`,`fecha`,`lugar`,`dni`) VALUES
-- ('','','','','');
-- INSERT INTO `configuraciones` (`id`,`puerto`,`email`,`asunto`,`mensaje_email`,`password`,`charset`,`email_type`,`smtp`) VALUES
-- ('','','','','','','','','');
