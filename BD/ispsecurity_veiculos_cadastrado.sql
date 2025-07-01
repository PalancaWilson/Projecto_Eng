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
-- Table structure for table `veiculos_cadastrado`
--

DROP TABLE IF EXISTS `veiculos_cadastrado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veiculos_cadastrado` (
  `id_veiculo` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(20) NOT NULL,
  `proprietario` varchar(100) NOT NULL,
  `tipo_usuario` int NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `estado` enum('Ativo','Inativo') DEFAULT 'Ativo',
  `imagem` varchar(255) DEFAULT NULL,
  `cadastrado_por` int DEFAULT NULL,
  `cadastrado_em` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_veiculo`),
  UNIQUE KEY `matricula` (`matricula`),
  KEY `cadastrado_por` (`cadastrado_por`),
  CONSTRAINT `veiculos_cadastrado_ibfk_1` FOREIGN KEY (`cadastrado_por`) REFERENCES `funcionarios` (`id_funcionario`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veiculos_cadastrado`
--

LOCK TABLES `veiculos_cadastrado` WRITE;
/*!40000 ALTER TABLE `veiculos_cadastrado` DISABLE KEYS */;
INSERT INTO `veiculos_cadastrado` VALUES (1,'LD-51-15-HZ','Ana Silva',1,'Toyota','Yaris','Ativo','ana-yaris.jpg',2,'2025-06-30 18:43:06'),(2,'LD-91-22-KP','Carlos Gomes',2,'Honda','Civic','Ativo','carlos-civic.jpg',2,'2025-06-30 18:43:06'),(3,'LD-31-11-MN','Maria João',3,'Hyundai','Tucson','Inativo','maria-tucson.jpg',1,'2025-06-30 18:43:06'),(4,'LD-71-99-FG','José Manuel',4,'Kia','Sportage','Ativo','jose-sportage.jpg',2,'2025-06-30 18:43:06'),(5,'LD-51-18-gj','Pedro Silva',1,'V8','toyota','Ativo','ana-yaris.jpg',1,'2025-06-30 19:30:20'),(6,'LD-41-22-dP','Miguel Gomes',2,'Camaro','cd','Ativo','carlos-civic.jpg',1,'2025-06-30 19:30:20'),(7,'LD-31-20-aa','Pedro Amaral',4,'V8','toyota','Ativo','ana-yaris.jpg',1,'2025-06-30 23:09:38'),(8,'LD-11-85-st','Miguel Gomes',3,'uno','uno','Inativo','carlos-civic.jpg',1,'2025-06-30 23:09:38'),(9,'LD-41-10-BA','Miguel Baptista',2,'Lexus','toyota','Ativo','ana-yaris.jpg',1,'2025-07-01 10:44:55'),(10,'LD-15-45-PP','João Ferreira Gomes',1,'Yace','toyota','Ativo','carlos-civic.jpg',1,'2025-07-01 10:44:55');
/*!40000 ALTER TABLE `veiculos_cadastrado` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-01 14:04:11
