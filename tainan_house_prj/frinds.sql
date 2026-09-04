-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2026-09-03 04:45:04
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `frinds`
--
CREATE DATABASE IF NOT EXISTS `frinds` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `frinds`;

-- --------------------------------------------------------

--
-- 資料表結構 `friend_club`
--

CREATE TABLE `friend_club` (
  `no` smallint(5) UNSIGNED NOT NULL COMMENT '編號',
  `name` varchar(5) NOT NULL COMMENT '姓名',
  `sex` char(1) NOT NULL COMMENT '性別',
  `age` varchar(10) NOT NULL COMMENT '年齡',
  `star_signs` varchar(3) NOT NULL COMMENT '星座',
  `height` varchar(10) NOT NULL COMMENT '身高',
  `weight` varchar(10) NOT NULL COMMENT '體重',
  `career` varchar(10) NOT NULL COMMENT '職業'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `friend_club`
--

INSERT INTO `friend_club` (`no`, `name`, `sex`, `age`, `star_signs`, `height`, `weight`, `career`) VALUES
(2, '小燕子', '女', '20~25', '牡羊座', '155~160', '45~50', '上班族'),
(3, '雲翔', '男', '20~25', '天蠍座', '175~180', '65~70', 'SOHO族');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `friend_club`
--
ALTER TABLE `friend_club`
  ADD PRIMARY KEY (`no`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `friend_club`
--
ALTER TABLE `friend_club`
  MODIFY `no` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '編號', AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
