-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: tienda
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `ID_usuario` int NOT NULL,
  PRIMARY KEY (`ID_usuario`),
  CONSTRAINT `administrador_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuario` (`ID_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caja`
--

DROP TABLE IF EXISTS `caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caja` (
  `ID_caja` int NOT NULL AUTO_INCREMENT,
  `ID_usuario` int NOT NULL,
  `ID_pedido` int NOT NULL,
  `SaldoInicial` decimal(10,2) NOT NULL,
  `SaldoFinal` decimal(10,2) NOT NULL,
  `Estado` varchar(50) NOT NULL,
  PRIMARY KEY (`ID_caja`),
  KEY `ID_pedido` (`ID_pedido`),
  CONSTRAINT `caja_ibfk_1` FOREIGN KEY (`ID_pedido`) REFERENCES `pedido` (`ID_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caja`
--

LOCK TABLES `caja` WRITE;
/*!40000 ALTER TABLE `caja` DISABLE KEYS */;
/*!40000 ALTER TABLE `caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cajero`
--

DROP TABLE IF EXISTS `cajero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cajero` (
  `ID_usuario` int NOT NULL,
  PRIMARY KEY (`ID_usuario`),
  CONSTRAINT `cajero_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuario` (`ID_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cajero`
--

LOCK TABLES `cajero` WRITE;
/*!40000 ALTER TABLE `cajero` DISABLE KEYS */;
/*!40000 ALTER TABLE `cajero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `combos`
--

DROP TABLE IF EXISTS `combos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(100) NOT NULL,
  `Producto1_ID` int NOT NULL,
  `Producto2_ID` int NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Nombre` (`Nombre`),
  KEY `Producto1_ID` (`Producto1_ID`),
  KEY `Producto2_ID` (`Producto2_ID`),
  CONSTRAINT `combos_ibfk_1` FOREIGN KEY (`Producto1_ID`) REFERENCES `producto` (`ID_producto`),
  CONSTRAINT `combos_ibfk_2` FOREIGN KEY (`Producto2_ID`) REFERENCES `producto` (`ID_producto`),
  CONSTRAINT `combos_chk_1` CHECK ((`Producto1_ID` <> `Producto2_ID`)),
  CONSTRAINT `combos_chk_2` CHECK ((`Precio` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combos`
--

LOCK TABLES `combos` WRITE;
/*!40000 ALTER TABLE `combos` DISABLE KEYS */;
INSERT INTO `combos` VALUES (1,'Combo Mañanero',8,4,120.00),(2,'Combo grasoso :v @',4,6,9999.00),(5,'Combo Vladimir',10,5,150.00);
/*!40000 ALTER TABLE `combos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contadores`
--

DROP TABLE IF EXISTS `contadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contadores` (
  `tipo` varchar(10) NOT NULL,
  `ultimo_valor` int DEFAULT NULL,
  PRIMARY KEY (`tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contadores`
--

LOCK TABLES `contadores` WRITE;
/*!40000 ALTER TABLE `contadores` DISABLE KEYS */;
INSERT INTO `contadores` VALUES ('admin',5),('cajero',5);
/*!40000 ALTER TABLE `contadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `descuentos`
--

DROP TABLE IF EXISTS `descuentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `descuentos` (
  `ID_descuento` int NOT NULL AUTO_INCREMENT,
  `Porcentaje` decimal(10,2) NOT NULL,
  `Producto_ID` int NOT NULL,
  `Precio_final` float NOT NULL,
  PRIMARY KEY (`ID_descuento`),
  KEY `Producto_ID` (`Producto_ID`),
  CONSTRAINT `descuentos_ibfk_1` FOREIGN KEY (`Producto_ID`) REFERENCES `producto` (`ID_producto`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descuentos`
--

LOCK TABLES `descuentos` WRITE;
/*!40000 ALTER TABLE `descuentos` DISABLE KEYS */;
INSERT INTO `descuentos` VALUES (2,10.00,8,63);
/*!40000 ALTER TABLE `descuentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial`
--

DROP TABLE IF EXISTS `historial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial` (
  `ID_historial` int NOT NULL AUTO_INCREMENT,
  `Movimientos` varchar(255) NOT NULL,
  `Fecha_movimientos` date NOT NULL,
  `ID_pedido` int NOT NULL,
  PRIMARY KEY (`ID_historial`),
  KEY `ID_pedido` (`ID_pedido`),
  CONSTRAINT `historial_ibfk_1` FOREIGN KEY (`ID_pedido`) REFERENCES `pedido` (`ID_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial`
--

LOCK TABLES `historial` WRITE;
/*!40000 ALTER TABLE `historial` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inv_producto`
--

DROP TABLE IF EXISTS `inv_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inv_producto` (
  `ID_insumo` int NOT NULL,
  `ID_producto` int NOT NULL,
  `Cantidad_utilizada` int NOT NULL,
  PRIMARY KEY (`ID_insumo`,`ID_producto`),
  KEY `ID_producto` (`ID_producto`),
  CONSTRAINT `inv_producto_ibfk_1` FOREIGN KEY (`ID_insumo`) REFERENCES `inventario` (`ID_insumo`),
  CONSTRAINT `inv_producto_ibfk_2` FOREIGN KEY (`ID_producto`) REFERENCES `producto` (`ID_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inv_producto`
--

LOCK TABLES `inv_producto` WRITE;
/*!40000 ALTER TABLE `inv_producto` DISABLE KEYS */;
INSERT INTO `inv_producto` VALUES (1,1,2),(2,1,1);
/*!40000 ALTER TABLE `inv_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `ID_insumo` int NOT NULL,
  `Nombre_insumo` varchar(100) NOT NULL,
  `Cantidad_Producto` int NOT NULL,
  PRIMARY KEY (`ID_insumo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (1,'Harina',100),(2,'Azúcar',50);
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `ID_pago` int NOT NULL AUTO_INCREMENT,
  `TipoPago` varchar(50) NOT NULL,
  `Monto` decimal(10,2) NOT NULL,
  `Descuentos` decimal(10,2) DEFAULT NULL,
  `Promociones` varchar(100) DEFAULT NULL,
  `ID_pedido` int NOT NULL,
  PRIMARY KEY (`ID_pago`),
  KEY `ID_pedido` (`ID_pedido`),
  CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`ID_pedido`) REFERENCES `pedido` (`ID_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `ID_pedido` int NOT NULL,
  `Fecha` date NOT NULL,
  `Estado` varchar(50) NOT NULL,
  `Nombre_cajero` varchar(100) NOT NULL,
  PRIMARY KEY (`ID_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'2025-02-09','Entregado','Rolando'),(2,'2025-02-10','Pendiente','Carol');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `ID_producto` int NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `Categoria` varchar(50) NOT NULL,
  `Cantidad` int NOT NULL,
  PRIMARY KEY (`ID_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Comida',0.00,'Comida',0),(2,'Bebidas',0.00,'Bebidas',2),(4,'Pastel',40.00,'Comida',2),(5,'Capuccino',30.00,'Bebidas',2),(6,'Cafe Mocca',40.00,'Bebidas',10),(7,'Croissant',40.00,'Comida',10),(8,'Cafe Espresso',70.00,'Bebidas',4),(10,'Concha Rellena',20.00,'Comida',20);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_pedido`
--

DROP TABLE IF EXISTS `producto_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_pedido` (
  `ID_producto` int NOT NULL,
  `ID_pedido` int NOT NULL,
  PRIMARY KEY (`ID_producto`,`ID_pedido`),
  KEY `ID_pedido` (`ID_pedido`),
  CONSTRAINT `producto_pedido_ibfk_1` FOREIGN KEY (`ID_producto`) REFERENCES `producto` (`ID_producto`),
  CONSTRAINT `producto_pedido_ibfk_2` FOREIGN KEY (`ID_pedido`) REFERENCES `pedido` (`ID_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_pedido`
--

LOCK TABLES `producto_pedido` WRITE;
/*!40000 ALTER TABLE `producto_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto_pedido` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `actualizar_reporte` AFTER INSERT ON `producto_pedido` FOR EACH ROW BEGIN
    DECLARE v_precio DECIMAL(10,2);
    DECLARE v_categoria VARCHAR(50);
    DECLARE v_nombre_cajero VARCHAR(100);
    DECLARE v_fecha DATE;

    SELECT Fecha, Nombre_cajero INTO v_fecha, v_nombre_cajero
    FROM Pedido
    WHERE ID_pedido = NEW.ID_pedido;

    SELECT Precio, Categoria INTO v_precio, v_categoria
    FROM Producto
    WHERE ID_producto = NEW.ID_producto;

    INSERT INTO Reporte (ID_reporte, TipoReporte, Periodo, Datos)
    VALUES (
        NULL,
        'Venta',
        DATE_FORMAT(v_fecha, '%Y-%m'), 
        CONCAT('Fecha: ', v_fecha, 
               ', Producto: ', NEW.ID_producto, 
               ', Categoría: ', v_categoria,
               ', Precio: ', v_precio, 
               ', Cajero: ', v_nombre_cajero)
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `reporte`
--

DROP TABLE IF EXISTS `reporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reporte` (
  `ID_reporte` int NOT NULL AUTO_INCREMENT,
  `TipoReporte` varchar(50) NOT NULL,
  `Periodo` varchar(50) NOT NULL,
  `Datos` text NOT NULL,
  PRIMARY KEY (`ID_reporte`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reporte`
--

LOCK TABLES `reporte` WRITE;
/*!40000 ALTER TABLE `reporte` DISABLE KEYS */;
INSERT INTO `reporte` VALUES (1,'Venta','2025-04-01','El dia de hoy 2025-04-01 se vendieron 2 productos (Leche(x1), Pan(x1)) con un costo total de $25.00 usando los metodos de pago Efectivo'),(2,'Venta','2025-04-01','El dia de hoy 2025-04-01 se vendieron 8 productos (Leche(x1), Pan(x1), Capuccino(x1), Cafe Mocca(x1), Cafe Espresso(x1), Pastel(x1), Croissant(x1), Pan Tipo Concha(x1)) con un costo total de $275.00 usando los metodos de pago Efectivo'),(3,'Venta','2025-04-05','El dia de hoy 2025-04-05 se vendieron 18 productos (Capuccino(x1), Pastel(x1), Cafe Mocca(x1), Croissant(x1), Cafe Mocca(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1)) con un costo total de $650.00 usando los metodos de pago Efectivo'),(4,'Venta','2025-04-05','El dia de hoy 2025-04-05 se vendieron 18 productos (Capuccino(x1), Pastel(x1), Cafe Mocca(x1), Croissant(x1), Cafe Mocca(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1)) con un costo total de $650.00 usando los metodos de pago Efectivo'),(5,'Venta','2025-04-05','El dia de hoy 2025-04-05 se vendieron 18 productos (Capuccino(x1), Pastel(x1), Cafe Mocca(x1), Croissant(x1), Cafe Mocca(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1)) con un costo total de $650.00 usando los metodos de pago Efectivo'),(6,'Venta','2025-04-05','El dia de hoy 2025-04-05 se vendieron 18 productos (Capuccino(x1), Pastel(x1), Cafe Mocca(x1), Croissant(x1), Cafe Mocca(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Croissant(x1), Capuccino(x1), Pastel(x1), Capuccino(x1), Pastel(x1)) con un costo total de $650.00 usando los metodos de pago Efectivo');
/*!40000 ALTER TABLE `reporte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID_usuario` int NOT NULL,
  `Contrasenna` varchar(10) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `correo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Direccion` varchar(255) NOT NULL,
  `ID_puesto` int NOT NULL,
  PRIMARY KEY (`ID_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (250103,'895488','Miri','9229876543','Casa Fea 2',1),(250105,'1234','Rolando','9229988776','Casa SN Jaltipan',1),(250201,'123456','Oscar','9221234567','Insurgentes N',2),(250202,'1234567','Juanito','juanitoxddxddd@gmail.com','calle culera',2),(250203,'etesech','El Pepe','elpp@itesco.edu.mx','Juventino rosas 1023',2),(250205,'sexo1234','Joseph Horreb','josleftover@hotmail.com','Rios perales 614',2);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_generar_id_usuario` BEFORE INSERT ON `usuario` FOR EACH ROW BEGIN
    DECLARE nuevo_contador INT;
    
    
    IF NEW.ID_Puesto = 1 THEN
        UPDATE contadores SET ultimo_valor = ultimo_valor + 1 
        WHERE tipo = 'admin';
        SELECT ultimo_valor INTO nuevo_contador 
        FROM contadores WHERE tipo = 'admin';
        SET NEW.id_usuario = CONCAT('2501', LPAD(nuevo_contador, 2, '0'));
    
    
    ELSEIF NEW.ID_Puesto = 2 THEN
        UPDATE contadores SET ultimo_valor = ultimo_valor + 1 
        WHERE tipo = 'cajero';
        SELECT ultimo_valor INTO nuevo_contador 
        FROM contadores WHERE tipo = 'cajero';
        SET NEW.id_usuario = CONCAT('2502', LPAD(nuevo_contador, 2, '0'));
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `producto` varchar(100) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_total` decimal(10,2) DEFAULT NULL,
  `forma_pago` varchar(20) DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`ID_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (3,'Leche','2025-04-01',1,15.00,'Efectivo',250103),(4,'Pan','2025-04-01',1,10.00,'Efectivo',250103),(5,'Capuccino','2025-04-01',1,30.00,'Efectivo',250103),(6,'Cafe Mocca','2025-04-01',1,40.00,'Efectivo',250103),(7,'Cafe Espresso','2025-04-01',1,70.00,'Efectivo',250103),(8,'Pastel','2025-04-01',1,40.00,'Efectivo',250103),(9,'Croissant','2025-04-01',1,40.00,'Efectivo',250103),(10,'Pan Tipo Concha','2025-04-01',1,30.00,'Efectivo',250103),(11,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(12,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(13,'Cafe Mocca','2025-04-05',1,40.00,'Efectivo',250103),(14,'Croissant','2025-04-05',1,40.00,'Efectivo',250103),(15,'Cafe Mocca','2025-04-05',1,40.00,'Efectivo',250103),(16,'Croissant','2025-04-05',1,40.00,'Efectivo',250103),(17,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(18,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(19,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(20,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(21,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(22,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(23,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(24,'Croissant','2025-04-05',1,40.00,'Efectivo',250103),(25,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(26,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(27,'Capuccino','2025-04-05',1,30.00,'Efectivo',250103),(28,'Pastel','2025-04-05',1,40.00,'Efectivo',250103),(29,'Cafe Mocca','2025-04-07',99,3960.00,'Efectivo',250103),(30,'Combo grasoso :v @','2025-04-07',99,989901.00,'Efectivo',250103);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-07 23:56:39
