-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ispsecurity
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `permissoes_acesso`
--

DROP TABLE IF EXISTS `permissoes_acesso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissoes_acesso` (
  `id_permissao` int NOT NULL AUTO_INCREMENT,
  `id_veiculo` int NOT NULL,
  `validade` date DEFAULT NULL,
  `horario_acesso` varchar(20) DEFAULT NULL,
  `tipo_usuario` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_permissao`),
  KEY `id_veiculo` (`id_veiculo`),
  CONSTRAINT `permissoes_acesso_ibfk_1` FOREIGN KEY (`id_veiculo`) REFERENCES `veiculos_cadastrado` (`id_veiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissoes_acesso`
--

LOCK TABLES `permissoes_acesso` WRITE;
/*!40000 ALTER TABLE `permissoes_acesso` DISABLE KEYS */;
INSERT INTO `permissoes_acesso` VALUES (1,2,'2025-12-31','09:00 - 18:00','Estudante'),(2,3,'2025-12-31','09:00 - 18:00','Visitante'),(3,4,'2025-12-31','09:00 - 18:00','Outro'),(4,5,'2025-12-31','09:00 - 18:00','Docente'),(5,6,'2025-12-31','09:00 - 18:00','Estudante'),(6,7,'2025-12-31','09:00 - 18:00','Outro'),(7,8,'2025-12-31','09:00 - 18:00','Visitante');
/*!40000 ALTER TABLE `permissoes_acesso` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-03 20:29:40
