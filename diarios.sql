-- MySQL dump 10.13  Distrib 5.7.32, for Linux (x86_64)
--
-- Host: localhost    Database: catering
-- ------------------------------------------------------
-- Server version	5.7.32-0ubuntu0.16.04.1

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
-- Table structure for table `diarios`
--

DROP TABLE IF EXISTS `diarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diarios` (
  `nome` varchar(50) DEFAULT NULL,
  `dia` int(1) DEFAULT NULL,
  `tipo` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diarios`
--

LOCK TABLES `diarios` WRITE;
/*!40000 ALTER TABLE `diarios` DISABLE KEYS */;
INSERT INTO `diarios` VALUES ('Caldo Verde',1,'sopa'),('Sopa de Grão',2,'sopa'),('Creme de Cenoura',3,'sopa'),('Sopa de Couve Lombarda',4,'sopa'),('Creme de Broculos',5,'sopa'),('Sopa de Cebola',6,'sopa'),('Canja de Galinha',7,'sopa'),('Feijoada à Transmontana',1,'carne'),('Favas à Portuguesa',2,'carne'),('Arroz de Cabidela',3,'carne'),('Alheira Frita com Batata Cozida e Grelos',4,'carne'),('Arroz de Pato',5,'carne'),('Moelas com Arroz e Batata Frita',6,'carne'),('Carne de Porco à Portuguesa',7,'carne'),('Arroz de Feijão com Pataniscas de Bacalhau',1,'peixe'),('Arroz de Marisco',2,'peixe'),('Bacalhau Assado com Batata Cozida',3,'peixe'),('Arroz de Lulas',4,'peixe'),('Bacalhau com Natas',5,'peixe'),('Caldeirada de Peixe e Marisco',6,'peixe'),('Filetes de Pescada com arroz de ervilhas',7,'peixe'),('Pastel de Nata',1,'sobremesa'),('Pudim Flan',2,'sobremesa'),('Rabanadas',3,'sobremesa'),('Aletria',4,'sobremesa'),('Pêras Bêbedas',5,'sobremesa'),('Molotof',6,'sobremesa'),('Arroz Doce',7,'sobremesa');
/*!40000 ALTER TABLE `diarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-29 18:36:51
