-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: mussa
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ajustado_curso_modelos_I`
--

DROP TABLE IF EXISTS `ajustado_curso_modelos_I`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ajustado_curso_modelos_I` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `actualizado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alumno`
--

DROP TABLE IF EXISTS `alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `padron` varchar(12) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `alumno_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alumnos_carreras`
--

DROP TABLE IF EXISTS `alumnos_carreras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnos_carreras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) DEFAULT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `alumnos_carreras_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`) ON DELETE CASCADE,
  CONSTRAINT `alumnos_carreras_ibfk_2` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `aprobacion_finales_pref_plan`
--

DROP TABLE IF EXISTS `aprobacion_finales_pref_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aprobacion_finales_pref_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `preferencias_id` int(11) DEFAULT NULL,
  `num_cuatrimestre_aprobacion` int(11) NOT NULL DEFAULT '0',
  `carrera_id` int(11) NOT NULL DEFAULT '0',
  `materia_alumno_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `preferencias_id` (`preferencias_id`),
  CONSTRAINT `aprobacion_finales_pref_plan_ibfk_1` FOREIGN KEY (`preferencias_id`) REFERENCES `preferencias_generacion_plan_de_estudios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `carrera`
--

DROP TABLE IF EXISTS `carrera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carrera` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(4) NOT NULL DEFAULT '',
  `nombre` varchar(50) NOT NULL DEFAULT '',
  `plan` varchar(4) NOT NULL DEFAULT '',
  `duracion_estimada_en_cuatrimestres` int(11) NOT NULL,
  `requiere_prueba_suficiencia_de_idioma` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `carrera_por_curso`
--

DROP TABLE IF EXISTS `carrera_por_curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carrera_por_curso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `curso_id` int(11) DEFAULT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `curso_id` (`curso_id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `carrera_por_curso_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  CONSTRAINT `carrera_por_curso_ibfk_2` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=352 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `carreras_plan_de_estudios`
--

DROP TABLE IF EXISTS `carreras_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carreras_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_estudios_id` int(11) DEFAULT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `plan_estudios_id` (`plan_estudios_id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `carreras_plan_de_estudios_ibfk_1` FOREIGN KEY (`plan_estudios_id`) REFERENCES `plan_de_estudios` (`id`),
  CONSTRAINT `carreras_plan_de_estudios_ibfk_2` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `correlativas`
--

DROP TABLE IF EXISTS `correlativas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `correlativas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materia_id` int(11) DEFAULT NULL,
  `materia_correlativa_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_id` (`materia_id`),
  KEY `materia_correlativa_id` (`materia_correlativa_id`),
  CONSTRAINT `correlativas_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `correlativas_ibfk_2` FOREIGN KEY (`materia_correlativa_id`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=347 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `creditos`
--

DROP TABLE IF EXISTS `creditos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creditos_obligatorias` int(11) NOT NULL,
  `creditos_electivas_general` int(11) NOT NULL,
  `creditos_orientacion` int(11) NOT NULL,
  `creditos_electivas_con_tp` int(11) NOT NULL,
  `creditos_electivas_con_tesis` int(11) NOT NULL,
  `creditos_tesis` int(11) NOT NULL,
  `creditos_tp_profesional` int(11) NOT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `creditos_ibfk_1` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_materia` varchar(4) NOT NULL DEFAULT '',
  `codigo` varchar(15) NOT NULL DEFAULT '',
  `se_dicta_primer_cuatrimestre` tinyint(1) NOT NULL DEFAULT '0',
  `se_dicta_segundo_cuatrimestre` tinyint(1) NOT NULL DEFAULT '0',
  `cantidad_encuestas_completas` int(11) NOT NULL DEFAULT '0',
  `puntaje_total_encuestas` int(11) NOT NULL DEFAULT '0',
  `fecha_actualizacion` datetime DEFAULT NULL,
  `primer_cuatrimestre_actualizado` tinyint(1) NOT NULL DEFAULT '0',
  `segundo_cuatrimestre_actualizado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=235 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cursos_docente`
--

DROP TABLE IF EXISTS `cursos_docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cursos_docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docente_id` int(11) DEFAULT NULL,
  `curso_id` int(11) DEFAULT NULL,
  `eliminado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `docente_id` (`docente_id`),
  KEY `curso_id` (`curso_id`),
  CONSTRAINT `cursos_docente_ibfk_1` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`),
  CONSTRAINT `cursos_docente_ibfk_2` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=638 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `docente`
--

DROP TABLE IF EXISTS `docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(35) NOT NULL DEFAULT '',
  `nombre` varchar(40) DEFAULT '',
  `eliminado` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=624 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encuesta_alumno`
--

DROP TABLE IF EXISTS `encuesta_alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encuesta_alumno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) NOT NULL,
  `materia_alumno_id` int(11) NOT NULL,
  `cuatrimestre_aprobacion_cursada` varchar(1) NOT NULL DEFAULT '',
  `anio_aprobacion_cursada` varchar(4) NOT NULL DEFAULT '',
  `finalizada` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `materia_alumno_id` (`materia_alumno_id`),
  CONSTRAINT `encuesta_alumno_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`),
  CONSTRAINT `encuesta_alumno_ibfk_2` FOREIGN KEY (`materia_alumno_id`) REFERENCES `materias_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encuesta_generada`
--

DROP TABLE IF EXISTS `encuesta_generada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encuesta_generada` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `grupo_id` int(11) NOT NULL,
  `encuesta_id` int(11) NOT NULL,
  `excluir_si_id` int(11) NOT NULL,
  `orden` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `orden` (`orden`),
  KEY `grupo_id` (`grupo_id`),
  KEY `encuesta_id` (`encuesta_id`),
  KEY `excluir_si_id` (`excluir_si_id`),
  CONSTRAINT `encuesta_generada_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupo_encuesta` (`id`),
  CONSTRAINT `encuesta_generada_ibfk_2` FOREIGN KEY (`encuesta_id`) REFERENCES `pregunta_encuesta` (`id`),
  CONSTRAINT `encuesta_generada_ibfk_3` FOREIGN KEY (`excluir_si_id`) REFERENCES `excluir_encuesta_si` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_materia`
--

DROP TABLE IF EXISTS `estado_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(70) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_pasos_encuesta_alumno`
--

DROP TABLE IF EXISTS `estado_pasos_encuesta_alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_pasos_encuesta_alumno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encuesta_alumno_id` int(11) NOT NULL,
  `estadoPaso1` int(11) NOT NULL DEFAULT '0',
  `estadoPaso2` int(11) NOT NULL DEFAULT '0',
  `estadoPaso3` int(11) NOT NULL DEFAULT '0',
  `estadoPaso4` int(11) NOT NULL DEFAULT '0',
  `estadoPaso5` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `encuesta_alumno_id` (`encuesta_alumno_id`),
  CONSTRAINT `estado_pasos_encuesta_alumno_ibfk_1` FOREIGN KEY (`encuesta_alumno_id`) REFERENCES `encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_plan_de_estudios`
--

DROP TABLE IF EXISTS `estado_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` int(11) NOT NULL DEFAULT '0',
  `descripcion` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `excluir_encuesta_si`
--

DROP TABLE IF EXISTS `excluir_encuesta_si`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `excluir_encuesta_si` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(35) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forma_aprobacion_materia`
--

DROP TABLE IF EXISTS `forma_aprobacion_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forma_aprobacion_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forma` varchar(35) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grupo_encuesta`
--

DROP TABLE IF EXISTS `grupo_encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_encuesta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero_grupo` int(11) NOT NULL DEFAULT '0',
  `grupo` varchar(35) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `horario`
--

DROP TABLE IF EXISTS `horario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `horario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia` varchar(12) NOT NULL DEFAULT '',
  `hora_desde` varchar(4) NOT NULL DEFAULT '',
  `hora_hasta` varchar(4) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=443 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `horario_por_curso`
--

DROP TABLE IF EXISTS `horario_por_curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `horario_por_curso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `curso_id` int(11) DEFAULT NULL,
  `horario_id` int(11) DEFAULT NULL,
  `es_horario_activo` tinyint(1) NOT NULL DEFAULT '0',
  `fecha_actualizacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `curso_id` (`curso_id`),
  KEY `horario_id` (`horario_id`),
  CONSTRAINT `horario_por_curso_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  CONSTRAINT `horario_por_curso_ibfk_2` FOREIGN KEY (`horario_id`) REFERENCES `horario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=442 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `horario_preferencias_generacion_plan_de_estudios`
--

DROP TABLE IF EXISTS `horario_preferencias_generacion_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `horario_preferencias_generacion_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `preferencias_id` int(11) DEFAULT NULL,
  `horario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `preferencias_id` (`preferencias_id`),
  KEY `horario_id` (`horario_id`),
  CONSTRAINT `horario_preferencias_generacion_plan_de_estudios_ibfk_1` FOREIGN KEY (`preferencias_id`) REFERENCES `preferencias_generacion_plan_de_estudios` (`id`),
  CONSTRAINT `horario_preferencias_generacion_plan_de_estudios_ibfk_2` FOREIGN KEY (`horario_id`) REFERENCES `horario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `horarios_ya_cargados`
--

DROP TABLE IF EXISTS `horarios_ya_cargados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `horarios_ya_cargados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anio` varchar(4) NOT NULL DEFAULT '',
  `cuatrimestre` varchar(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materia`
--

DROP TABLE IF EXISTS `materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(4) NOT NULL DEFAULT '',
  `nombre` varchar(80) NOT NULL DEFAULT '',
  `objetivos` varchar(250) DEFAULT '',
  `creditos_minimos_para_cursarla` int(11) NOT NULL,
  `creditos` int(11) NOT NULL,
  `tipo_materia_id` int(11) DEFAULT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_materia_id` (`tipo_materia_id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `materia_ibfk_1` FOREIGN KEY (`tipo_materia_id`) REFERENCES `tipo_materia` (`id`),
  CONSTRAINT `materia_ibfk_2` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materia_plan_de_estudios`
--

DROP TABLE IF EXISTS `materia_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materia_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_estudios_id` int(11) DEFAULT NULL,
  `materia_id` int(11) DEFAULT NULL,
  `curso_id` int(11) DEFAULT NULL,
  `orden` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `plan_estudios_id` (`plan_estudios_id`),
  KEY `materia_id` (`materia_id`),
  KEY `curso_id` (`curso_id`),
  CONSTRAINT `materia_plan_de_estudios_ibfk_1` FOREIGN KEY (`plan_estudios_id`) REFERENCES `plan_de_estudios` (`id`),
  CONSTRAINT `materia_plan_de_estudios_ibfk_2` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `materia_plan_de_estudios_ibfk_3` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materia_plan_de_estudios_cache`
--

DROP TABLE IF EXISTS `materia_plan_de_estudios_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materia_plan_de_estudios_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_estudios_cache_id` int(11) DEFAULT NULL,
  `materia_id` int(11) DEFAULT NULL,
  `curso_id` int(11) DEFAULT NULL,
  `orden` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `plan_estudios_cache_id` (`plan_estudios_cache_id`),
  KEY `materia_id` (`materia_id`),
  KEY `curso_id` (`curso_id`),
  CONSTRAINT `materia_plan_de_estudios_cache_ibfk_1` FOREIGN KEY (`plan_estudios_cache_id`) REFERENCES `plan_de_estudios_cache` (`id`),
  CONSTRAINT `materia_plan_de_estudios_cache_ibfk_2` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `materia_plan_de_estudios_cache_ibfk_3` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materias_alumno`
--

DROP TABLE IF EXISTS `materias_alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materias_alumno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) DEFAULT NULL,
  `materia_id` int(11) DEFAULT NULL,
  `curso_id` int(11) DEFAULT NULL,
  `carrera_id` int(11) DEFAULT NULL,
  `estado_id` int(11) DEFAULT NULL,
  `calificacion` int(11) DEFAULT NULL,
  `fecha_aprobacion` datetime DEFAULT NULL,
  `cuatrimestre_aprobacion_cursada` varchar(1) DEFAULT '',
  `anio_aprobacion_cursada` varchar(4) DEFAULT '',
  `acta_o_resolucion` varchar(35) DEFAULT '',
  `forma_aprobacion_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `materia_id` (`materia_id`),
  KEY `curso_id` (`curso_id`),
  KEY `carrera_id` (`carrera_id`),
  KEY `estado_id` (`estado_id`),
  KEY `forma_aprobacion_id` (`forma_aprobacion_id`),
  CONSTRAINT `materias_alumno_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`),
  CONSTRAINT `materias_alumno_ibfk_2` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `materias_alumno_ibfk_3` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  CONSTRAINT `materias_alumno_ibfk_4` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`),
  CONSTRAINT `materias_alumno_ibfk_5` FOREIGN KEY (`estado_id`) REFERENCES `estado_materia` (`id`),
  CONSTRAINT `materias_alumno_ibfk_6` FOREIGN KEY (`forma_aprobacion_id`) REFERENCES `forma_aprobacion_materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materias_incompatibles`
--

DROP TABLE IF EXISTS `materias_incompatibles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materias_incompatibles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materia_id` int(11) DEFAULT NULL,
  `materia_incompatible_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_id` (`materia_id`),
  KEY `materia_incompatible_id` (`materia_incompatible_id`),
  CONSTRAINT `materias_incompatibles_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `materias_incompatibles_ibfk_2` FOREIGN KEY (`materia_incompatible_id`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orientacion`
--

DROP TABLE IF EXISTS `orientacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orientacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(125) NOT NULL DEFAULT '',
  `clave_reducida` varchar(50) NOT NULL DEFAULT '',
  `carrera_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `carrera_id` (`carrera_id`),
  CONSTRAINT `orientacion_ibfk_1` FOREIGN KEY (`carrera_id`) REFERENCES `carrera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `palabra_clave`
--

DROP TABLE IF EXISTS `palabra_clave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `palabra_clave` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `palabra` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `palabras_clave_para_materias`
--

DROP TABLE IF EXISTS `palabras_clave_para_materias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `palabras_clave_para_materias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materia_id` int(11) DEFAULT NULL,
  `palabra_clave_id` int(11) DEFAULT NULL,
  `cantidad_encuestas_asociadas` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `materia_id` (`materia_id`),
  KEY `palabra_clave_id` (`palabra_clave_id`),
  CONSTRAINT `palabras_clave_para_materias_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `palabras_clave_para_materias_ibfk_2` FOREIGN KEY (`palabra_clave_id`) REFERENCES `palabra_clave` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_de_estudios`
--

DROP TABLE IF EXISTS `plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) DEFAULT NULL,
  `fecha_generacion` datetime DEFAULT NULL,
  `fecha_ultima_actualizacion` datetime DEFAULT NULL,
  `estado_id` int(11) DEFAULT NULL,
  `cuatrimestre_inicio_plan` int(11) NOT NULL DEFAULT '0',
  `anio_inicio_plan` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `estado_id` (`estado_id`),
  CONSTRAINT `plan_de_estudios_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`),
  CONSTRAINT `plan_de_estudios_ibfk_2` FOREIGN KEY (`estado_id`) REFERENCES `estado_plan_de_estudios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_de_estudios_cache`
--

DROP TABLE IF EXISTS `plan_de_estudios_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan_de_estudios_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash_parametros` varchar(50) NOT NULL DEFAULT '',
  `estado_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estado_id` (`estado_id`),
  CONSTRAINT `plan_de_estudios_cache_ibfk_1` FOREIGN KEY (`estado_id`) REFERENCES `estado_plan_de_estudios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_de_estudios_finalizado_de_procesar`
--

DROP TABLE IF EXISTS `plan_de_estudios_finalizado_de_procesar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan_de_estudios_finalizado_de_procesar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) DEFAULT NULL,
  `plan_estudios_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `plan_estudios_id` (`plan_estudios_id`),
  CONSTRAINT `plan_de_estudios_finalizado_de_procesar_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`),
  CONSTRAINT `plan_de_estudios_finalizado_de_procesar_ibfk_2` FOREIGN KEY (`plan_estudios_id`) REFERENCES `plan_de_estudios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `preferencias_generacion_plan_de_estudios`
--

DROP TABLE IF EXISTS `preferencias_generacion_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preferencias_generacion_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alumno_id` int(11) DEFAULT NULL,
  `cant_cuatrimestres_max` int(11) NOT NULL DEFAULT '0',
  `hs_cursada_por_semana_max` int(11) NOT NULL DEFAULT '0',
  `hs_extras_por_semana_max` int(11) NOT NULL DEFAULT '0',
  `puntaje_minimo_cursos` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  CONSTRAINT `preferencias_generacion_plan_de_estudios_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_encuesta`
--

DROP TABLE IF EXISTS `pregunta_encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_encuesta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pregunta` varchar(250) NOT NULL DEFAULT '',
  `tipo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_id` (`tipo_id`),
  CONSTRAINT `pregunta_encuesta_ibfk_1` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_encuesta_numero`
--

DROP TABLE IF EXISTS `pregunta_encuesta_numero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_encuesta_numero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encuesta_id` int(11) NOT NULL,
  `numero_min` int(11) NOT NULL DEFAULT '0',
  `numero_max` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `encuesta_id` (`encuesta_id`),
  CONSTRAINT `pregunta_encuesta_numero_ibfk_1` FOREIGN KEY (`encuesta_id`) REFERENCES `pregunta_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_encuesta_puntaje`
--

DROP TABLE IF EXISTS `pregunta_encuesta_puntaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_encuesta_puntaje` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encuesta_id` int(11) NOT NULL,
  `texto_min` varchar(25) NOT NULL DEFAULT '',
  `texto_max` varchar(25) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `encuesta_id` (`encuesta_id`),
  CONSTRAINT `pregunta_encuesta_puntaje_ibfk_1` FOREIGN KEY (`encuesta_id`) REFERENCES `pregunta_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_encuesta_si_o_no`
--

DROP TABLE IF EXISTS `pregunta_encuesta_si_o_no`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_encuesta_si_o_no` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encuesta_id` int(11) NOT NULL,
  `encuesta_id_si` int(11) DEFAULT NULL,
  `encuesta_id_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `encuesta_id` (`encuesta_id`),
  KEY `encuesta_id_si` (`encuesta_id_si`),
  KEY `encuesta_id_no` (`encuesta_id_no`),
  CONSTRAINT `pregunta_encuesta_si_o_no_ibfk_1` FOREIGN KEY (`encuesta_id`) REFERENCES `pregunta_encuesta` (`id`),
  CONSTRAINT `pregunta_encuesta_si_o_no_ibfk_2` FOREIGN KEY (`encuesta_id_si`) REFERENCES `pregunta_encuesta` (`id`),
  CONSTRAINT `pregunta_encuesta_si_o_no_ibfk_3` FOREIGN KEY (`encuesta_id_no`) REFERENCES `pregunta_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_resultado_encuesta`
--

DROP TABLE IF EXISTS `pregunta_resultado_encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_resultado_encuesta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pregunta` varchar(250) NOT NULL DEFAULT '',
  `pregunta_encuesta_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pregunta_encuesta_id` (`pregunta_encuesta_id`),
  CONSTRAINT `pregunta_resultado_encuesta_ibfk_1` FOREIGN KEY (`pregunta_encuesta_id`) REFERENCES `pregunta_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pregunta_resultado_encuesta_puntaje`
--

DROP TABLE IF EXISTS `pregunta_resultado_encuesta_puntaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pregunta_resultado_encuesta_puntaje` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pregunta_resultado_id` int(11) NOT NULL,
  `texto_1` varchar(25) NOT NULL DEFAULT '',
  `texto_2` varchar(25) NOT NULL DEFAULT '',
  `texto_3` varchar(25) NOT NULL DEFAULT '',
  `texto_4` varchar(25) NOT NULL DEFAULT '',
  `texto_5` varchar(25) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `pregunta_resultado_id` (`pregunta_resultado_id`),
  CONSTRAINT `pregunta_resultado_encuesta_puntaje_ibfk_1` FOREIGN KEY (`pregunta_resultado_id`) REFERENCES `pregunta_resultado_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `respuesta_encuesta_alumno`
--

DROP TABLE IF EXISTS `respuesta_encuesta_alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `respuesta_encuesta_alumno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encuesta_alumno_id` int(11) NOT NULL,
  `pregunta_encuesta_id` int(11) NOT NULL,
  `tipo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `encuesta_alumno_id` (`encuesta_alumno_id`),
  KEY `pregunta_encuesta_id` (`pregunta_encuesta_id`),
  KEY `tipo_id` (`tipo_id`),
  CONSTRAINT `respuesta_encuesta_alumno_ibfk_1` FOREIGN KEY (`encuesta_alumno_id`) REFERENCES `encuesta_alumno` (`id`),
  CONSTRAINT `respuesta_encuesta_alumno_ibfk_2` FOREIGN KEY (`pregunta_encuesta_id`) REFERENCES `pregunta_encuesta` (`id`),
  CONSTRAINT `respuesta_encuesta_alumno_ibfk_3` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_encuesta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `label` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_correlativa`
--

DROP TABLE IF EXISTS `rta_encuesta_correlativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_correlativa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `materia_correlativa_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  KEY `materia_correlativa_id` (`materia_correlativa_id`),
  CONSTRAINT `rta_encuesta_correlativa_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`),
  CONSTRAINT `rta_encuesta_correlativa_ibfk_2` FOREIGN KEY (`materia_correlativa_id`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_docente`
--

DROP TABLE IF EXISTS `rta_encuesta_docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `docente_id` int(11) NOT NULL,
  `comentario` varchar(250) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  KEY `docente_id` (`docente_id`),
  CONSTRAINT `rta_encuesta_docente_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`),
  CONSTRAINT `rta_encuesta_docente_ibfk_2` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_estrellas`
--

DROP TABLE IF EXISTS `rta_encuesta_estrellas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_estrellas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `estrellas` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  CONSTRAINT `rta_encuesta_estrellas_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_horario`
--

DROP TABLE IF EXISTS `rta_encuesta_horario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_horario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `horario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  KEY `horario_id` (`horario_id`),
  CONSTRAINT `rta_encuesta_horario_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`),
  CONSTRAINT `rta_encuesta_horario_ibfk_2` FOREIGN KEY (`horario_id`) REFERENCES `horario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_numero`
--

DROP TABLE IF EXISTS `rta_encuesta_numero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_numero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  CONSTRAINT `rta_encuesta_numero_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_puntaje`
--

DROP TABLE IF EXISTS `rta_encuesta_puntaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_puntaje` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `puntaje` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  CONSTRAINT `rta_encuesta_puntaje_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_si_no`
--

DROP TABLE IF EXISTS `rta_encuesta_si_no`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_si_no` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `respuesta` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  CONSTRAINT `rta_encuesta_si_no_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_tags`
--

DROP TABLE IF EXISTS `rta_encuesta_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `palabra_clave_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  KEY `palabra_clave_id` (`palabra_clave_id`),
  CONSTRAINT `rta_encuesta_tags_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`),
  CONSTRAINT `rta_encuesta_tags_ibfk_2` FOREIGN KEY (`palabra_clave_id`) REFERENCES `palabra_clave` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_tematica`
--

DROP TABLE IF EXISTS `rta_encuesta_tematica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_tematica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `tematica_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  KEY `tematica_id` (`tematica_id`),
  CONSTRAINT `rta_encuesta_tematica_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`),
  CONSTRAINT `rta_encuesta_tematica_ibfk_2` FOREIGN KEY (`tematica_id`) REFERENCES `tematica_materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rta_encuesta_texto`
--

DROP TABLE IF EXISTS `rta_encuesta_texto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rta_encuesta_texto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rta_encuesta_alumno_id` int(11) NOT NULL,
  `texto` varchar(250) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `rta_encuesta_alumno_id` (`rta_encuesta_alumno_id`),
  CONSTRAINT `rta_encuesta_texto_ibfk_1` FOREIGN KEY (`rta_encuesta_alumno_id`) REFERENCES `respuesta_encuesta_alumno` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tematica_materia`
--

DROP TABLE IF EXISTS `tematica_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tematica_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tematica` varchar(40) NOT NULL DEFAULT '',
  `verificada` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tematica_por_materia`
--

DROP TABLE IF EXISTS `tematica_por_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tematica_por_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materia_id` int(11) DEFAULT NULL,
  `tematica_id` int(11) DEFAULT NULL,
  `cantidad_encuestas_asociadas` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `materia_id` (`materia_id`),
  KEY `tematica_id` (`tematica_id`),
  CONSTRAINT `tematica_por_materia_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  CONSTRAINT `tematica_por_materia_ibfk_2` FOREIGN KEY (`tematica_id`) REFERENCES `tematica_materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tematica_preferencias_generacion_plan_de_estudios`
--

DROP TABLE IF EXISTS `tematica_preferencias_generacion_plan_de_estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tematica_preferencias_generacion_plan_de_estudios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `preferencias_id` int(11) DEFAULT NULL,
  `tematica_id` int(11) DEFAULT NULL,
  `porcentaje` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `preferencias_id` (`preferencias_id`),
  KEY `tematica_id` (`tematica_id`),
  CONSTRAINT `tematica_preferencias_generacion_plan_de_estudios_ibfk_1` FOREIGN KEY (`preferencias_id`) REFERENCES `preferencias_generacion_plan_de_estudios` (`id`),
  CONSTRAINT `tematica_preferencias_generacion_plan_de_estudios_ibfk_2` FOREIGN KEY (`tematica_id`) REFERENCES `tematica_materia` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_encuesta`
--

DROP TABLE IF EXISTS `tipo_encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_encuesta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` int(11) NOT NULL DEFAULT '0',
  `descripcion` varchar(25) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_materia`
--

DROP TABLE IF EXISTS `tipo_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL DEFAULT '',
  `confirmed_at` datetime DEFAULT NULL,
  `password` varchar(255) NOT NULL DEFAULT '',
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `first_name` varchar(50) NOT NULL DEFAULT '',
  `last_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_roles`
--

DROP TABLE IF EXISTS `users_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `users_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-13 19:53:30
