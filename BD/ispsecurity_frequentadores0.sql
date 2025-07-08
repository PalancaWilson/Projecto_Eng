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
-- Table structure for table `frequentadores`
--

DROP TABLE IF EXISTS `frequentadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frequentadores` (
  `id_frequentador` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `tipo` enum('Estudante','Visitante','Encarregado','Professor','Direção') NOT NULL,
  `numero_documento` varchar(20) DEFAULT NULL,
  `contacto` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `criado_em` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_frequentador`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frequentadores`
--

LOCK TABLES `frequentadores` WRITE;
/*!40000 ALTER TABLE `frequentadores` DISABLE KEYS */;
INSERT INTO `frequentadores` VALUES (1,'Mario Ricardo','Estudante','12345678LA045','923456789','mario@alunos.isptec.co.ao','2025-06-30 18:40:58'),(2,'Amaro Costantino','Visitante','87654321LA012','924567890','amaro@gmail.com','2025-06-30 18:40:58'),(3,'Fanilton Samuel','Encarregado','10987654LA030','922334455','samuel@gmail.com','2025-06-30 18:40:58'),(4,'Skenk Velas','Professor','19283746LA019','933445566','velas@isptec.co.ao','2025-06-30 18:40:58'),(5,'Palanca Wilson','Direção','56473829LA056','928884422','wilson@isptec.co.ao','2025-06-30 18:40:58'),(6,'Jandira Pena','Estudante','15445678LA045','924466789','jandira@alunos.isptec.co.ao','2025-07-03 00:34:02'),(7,'Benicio Scout','Visitante','64654321LA012','923567890','benicio@gmail.com','2025-07-03 00:34:02'),(8,'Fabricio Mavacala','Encarregado','16487654LA030','927634455','fabry@gmail.com','2025-07-03 00:34:02'),(9,'Miguel Amaral','Professor','16483746LA019','912445566','miguel@isptec.co.ao','2025-07-03 00:34:02'),(10,'Deltonio Costa','Direção','56343829LA056','928234422','costa@isptec.co.ao','2025-07-03 00:34:02');
/*!40000 ALTER TABLE `frequentadores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-03 20:29:38
