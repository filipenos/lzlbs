-- Adminer 4.7.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP DATABASE IF EXISTS `mglu`;
CREATE DATABASE `mglu` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mglu`;

DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `favorite_list`;
CREATE TABLE `favorite_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `favorite_list_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `favorite_list_id` int(11) NOT NULL,
  `product_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `favorite_list_id` (`favorite_list_id`),
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`favorite_list_id`) REFERENCES `favorite_list` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- 2019-09-18 15:32:48
