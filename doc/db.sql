-- --------------------------------------------------------
-- Host:                         192.168.0.123
-- Server version:               10.3.22-MariaDB-0+deb10u1 - Raspbian 10
-- Server OS:                    debian-linux-gnueabihf
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for boodschappp
CREATE DATABASE IF NOT EXISTS `boodschappp` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `boodschappp`;

-- Dumping structure for table boodschappp.GroceryStore
CREATE TABLE IF NOT EXISTS `GroceryStore` (
  `Id` char(36) NOT NULL DEFAULT uuid(),
  `store_name` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table boodschappp.Product
CREATE TABLE IF NOT EXISTS `Product` (
  `Id` int(11) NOT NULL,
  `store_id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `last_updated` datetime NOT NULL DEFAULT current_timestamp(),
  `image` varchar(255) DEFAULT NULL,
  `price` int(11) NOT NULL DEFAULT 0,
  `bonus` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`Id`,`store_id`,`last_updated`) USING BTREE,
  KEY `FK__GrocerieStore` (`store_id`),
  CONSTRAINT `FK__GrocerieStore` FOREIGN KEY (`store_id`) REFERENCES `GroceryStore` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table boodschappp.ScrapeErrors
CREATE TABLE IF NOT EXISTS `ScrapeErrors` (
  `Id` char(36) NOT NULL DEFAULT uuid(),
  `scrape_id` char(36) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_ScrapeErrors_Product` (`product_id`),
  KEY `FK_ScrapeErrors_GrocerieStore` (`scrape_id`) USING BTREE,
  CONSTRAINT `FK_ScrapeErrors_Product` FOREIGN KEY (`product_id`) REFERENCES `Product` (`Id`),
  CONSTRAINT `FK_ScrapeErrors_ScrapeHistory` FOREIGN KEY (`scrape_id`) REFERENCES `ScrapeHistory` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table boodschappp.ScrapeHistory
CREATE TABLE IF NOT EXISTS `ScrapeHistory` (
  `Id` char(36) NOT NULL DEFAULT uuid(),
  `store_id` char(36) DEFAULT NULL,
  `start_date` datetime NOT NULL DEFAULT current_timestamp(),
  `end_date` datetime DEFAULT NULL,
  `error_count` int(11) NOT NULL DEFAULT 0,
  `scrape_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_ScrapeHistory_GrocerieStore` (`store_id`),
  CONSTRAINT `FK_ScrapeHistory_GrocerieStore` FOREIGN KEY (`store_id`) REFERENCES `GroceryStore` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table boodschappp.UserAgents
CREATE TABLE IF NOT EXISTS `UserAgents` (
  `Id` char(36) NOT NULL DEFAULT uuid(),
  `agent` varchar(255) NOT NULL,
  `os` varchar(255) DEFAULT NULL,
  `software` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
