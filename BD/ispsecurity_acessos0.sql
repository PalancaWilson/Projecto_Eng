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
-- Table structure for table `acessos`
--

DROP TABLE IF EXISTS `acessos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acessos` (
  `id_acesso` int NOT NULL AUTO_INCREMENT,
  `id_carro` int NOT NULL,
  `tipo_frequentador` int NOT NULL,
  `estado` enum('Autorizado','Recusado') DEFAULT NULL,
  `data_acesso` date NOT NULL,
  `hora_acesso` time NOT NULL,
  `imagem` text,
  PRIMARY KEY (`id_acesso`),
  KEY `id_carro` (`id_carro`),
  KEY `tipo_frequentador` (`tipo_frequentador`),
  CONSTRAINT `acessos_ibfk_1` FOREIGN KEY (`id_carro`) REFERENCES `veiculos_cadastrado` (`id_veiculo`),
  CONSTRAINT `acessos_ibfk_2` FOREIGN KEY (`tipo_frequentador`) REFERENCES `frequentadores` (`id_frequentador`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acessos`
--

LOCK TABLES `acessos` WRITE;
/*!40000 ALTER TABLE `acessos` DISABLE KEYS */;
INSERT INTO `acessos` VALUES (1,1,1,'Autorizado','2025-06-25','07:30:00','entrada1.jpg'),(2,1,4,'Autorizado','2025-06-25','10:00:00','entrada2.jpg'),(3,1,4,'Recusado','2025-06-25','15:45:00','entrada3.jpg'),(4,2,2,'Autorizado','2025-06-26','08:00:00','entrada4.jpg'),(5,1,1,'Autorizado','2025-06-30','19:21:39','foto1.jpg'),(6,1,1,'Recusado','2025-06-30','08:30:00','foto2.jpg'),(7,1,1,'Autorizado','2025-06-30','09:45:00','foto3.jpg'),(8,4,4,'Autorizado','2025-06-25','07:30:00','entrada1.jpg'),(9,1,4,'Autorizado','2025-06-25','10:00:00','entrada2.jpg'),(12,2,2,'Autorizado','2025-07-01','06:30:00','entrada1.jpg'),(13,3,3,'Autorizado','2025-07-01','22:00:00','entrada2.jpg'),(14,2,3,'Autorizado','2025-07-01','15:00:00','entrada1.jpg'),(15,3,1,'Autorizado','2025-07-01','12:20:00','entrada2.jpg'),(16,1,4,'Autorizado','2025-07-01','08:00:00','entrada1.jpg'),(22,2,2,'Recusado','2025-07-01','07:30:00','entrada1.jpg'),(23,4,3,'Recusado','2025-07-01','23:00:00','entrada2.jpg'),(24,1,3,'Recusado','2025-07-01','11:00:00','entrada1.jpg'),(25,3,1,'Recusado','2025-07-01','09:20:00','entrada2.jpg'),(26,1,4,'Recusado','2025-07-01','20:30:00','entrada1.jpg'),(27,1,2,'Autorizado','2025-07-01','10:30:00','entrada1.jpg'),(28,4,3,'Autorizado','2025-07-01','06:00:00','entrada2.jpg'),(29,1,3,'Recusado','2025-07-01','17:00:00','entrada1.jpg'),(30,1,1,'Autorizado','2025-07-01','18:20:00','entrada2.jpg'),(31,2,4,'Recusado','2025-07-01','20:30:00','entrada1.jpg'),(32,1,2,'Autorizado','2025-07-01','12:40:00','entrada1.jpg'),(33,4,3,'Autorizado','2025-07-01','09:20:00','entrada2.jpg'),(34,1,3,'Recusado','2025-07-01','19:16:00','entrada1.jpg'),(35,1,1,'Autorizado','2025-07-01','13:26:16','entrada2.jpg'),(36,2,4,'Recusado','2025-07-01','05:33:00','entrada1.jpg'),(37,1,2,'Autorizado','2025-07-01','11:40:00','entrada1.jpg'),(38,4,3,'Autorizado','2025-07-01','19:20:00','entrada2.jpg'),(39,1,3,'Recusado','2025-07-01','12:16:00','entrada1.jpg'),(40,1,1,'Autorizado','2025-07-01','15:26:16','entrada2.jpg'),(41,2,4,'Recusado','2025-07-01','08:33:00','entrada1.jpg'),(42,1,2,'Autorizado','2025-07-02','11:40:00','entrada1.jpg'),(43,4,3,'Autorizado','2025-07-03','19:20:00','entrada2.jpg'),(44,1,3,'Recusado','2025-07-02','12:16:00','entrada1.jpg'),(45,1,1,'Autorizado','2025-07-02','15:26:16','entrada2.jpg'),(46,2,4,'Recusado','2025-07-02','08:33:00','entrada1.jpg'),(47,1,2,'Autorizado','2025-07-02','12:40:00','entrada1.jpg'),(48,4,3,'Autorizado','2025-07-03','18:20:00','entrada2.jpg'),(49,1,3,'Recusado','2025-07-02','14:16:00','entrada1.jpg'),(50,1,1,'Autorizado','2025-07-02','18:26:16','entrada2.jpg'),(51,2,4,'Recusado','2025-07-02','10:43:00','entrada1.jpg'),(52,1,2,'Autorizado','2025-07-02','12:40:00','entrada1.jpg'),(53,4,3,'Autorizado','2025-07-03','18:20:00','entrada2.jpg'),(54,1,3,'Recusado','2025-07-02','14:16:00','entrada1.jpg'),(55,1,1,'Autorizado','2025-07-02','18:26:16','entrada2.jpg'),(56,2,4,'Recusado','2025-07-02','10:43:00','entrada1.jpg'),(57,1,2,'Autorizado','2025-07-02','12:40:00','entrada1.jpg'),(58,4,3,'Recusado','2025-07-03','18:20:00','entrada2.jpg'),(59,1,3,'Recusado','2025-07-02','14:16:00','entrada1.jpg'),(60,1,1,'Autorizado','2025-07-02','18:26:16','entrada2.jpg'),(61,2,4,'Recusado','2025-07-02','10:43:00','entrada1.jpg'),(62,1,2,'Autorizado','2025-07-02','12:40:00','entrada1.jpg'),(63,4,3,'Recusado','2025-07-03','18:20:00','entrada2.jpg'),(64,1,3,'Recusado','2025-07-02','14:16:00','entrada1.jpg'),(65,1,1,'Autorizado','2025-07-02','18:26:16','entrada2.jpg'),(66,2,4,'Recusado','2025-07-02','10:43:00','entrada1.jpg'),(67,1,2,'Autorizado','2025-07-03','12:40:00','entrada1.jpg'),(68,4,3,'Recusado','2025-07-03','18:20:00','entrada2.jpg'),(69,1,3,'Recusado','2025-07-03','14:16:00','entrada1.jpg'),(70,1,1,'Autorizado','2025-07-03','18:26:16','entrada2.jpg'),(71,2,4,'Recusado','2025-07-03','10:43:00','entrada1.jpg'),(72,1,2,'Autorizado','2025-07-03','12:40:00','entrada1.jpg'),(73,4,3,'Recusado','2025-07-03','18:20:00','entrada2.jpg'),(74,1,3,'Recusado','2025-07-03','14:16:00','entrada1.jpg'),(75,1,1,'Autorizado','2025-07-03','18:26:16','entrada2.jpg'),(76,2,4,'Recusado','2025-07-03','10:43:00','entrada1.jpg'),(77,1,2,'Autorizado','2025-07-03','12:40:00','entrada1.jpg'),(78,1,2,'Autorizado','2025-07-03','22:40:00','entrada1.jpg'),(79,1,2,'Autorizado','2025-07-03','22:55:00','entrada1.jpg'),(80,1,2,'Autorizado','2025-07-03','23:45:00','entrada1.jpg'),(81,4,3,'Recusado','2025-07-03','15:10:00','entrada2.jpg'),(82,1,3,'Recusado','2025-07-03','12:46:00','entrada1.jpg'),(83,1,1,'Autorizado','2025-07-03','00:46:16','entrada2.jpg'),(84,2,4,'Recusado','2025-07-03','17:43:30','entrada1.jpg'),(85,2,4,'Autorizado','2025-07-03','23:59:00','entrada1.jpg'),(86,1,2,'Autorizado','2025-07-03','15:40:00','entrada2.jpg'),(87,3,1,'Autorizado','2025-07-03','12:26:00','entrada1.jpg'),(88,4,4,'Autorizado','2025-07-03','00:57:16','entrada2.jpg'),(89,1,1,'Autorizado','2025-07-03','17:13:30','entrada1.jpg');
/*!40000 ALTER TABLE `acessos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-03 20:29:39
