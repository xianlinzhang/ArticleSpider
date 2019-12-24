/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : article_spider

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-06-11 09:36:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
  `url_object_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `front_image_url` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `front_image_path` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
