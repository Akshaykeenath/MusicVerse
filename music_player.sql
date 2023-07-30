-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jul 30, 2023 at 11:44 AM
-- Server version: 5.7.9
-- PHP Version: 5.6.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `music_player`
--

-- --------------------------------------------------------

--
-- Table structure for table `album`
--

DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `album_name` varchar(100) NOT NULL,
  `image_loc` varchar(255) NOT NULL,
  `cover_pic` varchar(255) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  PRIMARY KEY (`album_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `album`
--

INSERT INTO `album` (`album_id`, `album_name`, `image_loc`, `cover_pic`, `user_id`) VALUES
(1, 'Athiran', 'uploads/album/Athiranpropic.jpg', 'uploads/album/Athirancoverpic.jpg', '1'),
(2, 'Hridhyam', 'uploads/album/Hridhyampropic.jpg', 'uploads/album/Hridhyamcoverpic.jpg', '1'),
(3, 'Sita Ramam', 'uploads/album/Sita Ramampropic.jpg', 'uploads/album/Sita Ramamcoverpic.jpg', '2'),
(4, 'Urumi', 'uploads/album/Urumipropic.jpg', 'uploads/album/Urumicoverpic.jpg', '2');

-- --------------------------------------------------------

--
-- Table structure for table `artist`
--

DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `artist_name` varchar(100) NOT NULL,
  `image_loc` varchar(255) NOT NULL,
  `cover_pic` varchar(255) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  PRIMARY KEY (`artist_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `artist`
--

INSERT INTO `artist` (`artist_id`, `artist_name`, `image_loc`, `cover_pic`, `user_id`) VALUES
(1, 'K S Harishankar', 'uploads/artist/K S Harishankarpropic.png', 'uploads/artist/K S Harishankarcoverpic.jpg', '1'),
(2, 'Vineeth Sreenivasan', 'uploads/artist/Vineeth Sreenivasanpropic.jpg', 'uploads/artist/Vineeth Sreenivasancoverpic.jpg', '1'),
(3, 'Swetha Mohan', 'uploads/artist/Swetha Mohanpropic.jpg', 'uploads/artist/Swetha Mohancoverpic.jpg', '2'),
(4, 'Shreya Ghoshal', 'uploads/artist/Shreya Ghoshalpropic.jpeg', 'uploads/artist/Shreya Ghoshalcoverpic.jpg', '1');

-- --------------------------------------------------------

--
-- Table structure for table `clicks`
--

DROP TABLE IF EXISTS `clicks`;
CREATE TABLE IF NOT EXISTS `clicks` (
  `click_id` int(11) NOT NULL AUTO_INCREMENT,
  `content_id` varchar(25) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  `content_type` varchar(25) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`click_id`)
) ENGINE=MyISAM AUTO_INCREMENT=446 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clicks`
--

INSERT INTO `clicks` (`click_id`, `content_id`, `user_id`, `content_type`, `timestamp`) VALUES
(1, '1', '1', 'album', '2023-06-26 07:02:09'),
(2, '1', '1', 'album', '2023-06-26 07:38:25'),
(3, '1', '1', 'album', '2023-06-26 07:41:25'),
(4, '1', '1', 'album', '2023-06-26 07:42:50'),
(5, '1', '1', 'album', '2023-06-26 07:43:14'),
(6, '1', '1', 'album', '2023-06-26 07:49:40'),
(7, '1', '1', 'album', '2023-06-26 07:52:15'),
(8, '1', '1', 'album', '2023-06-26 07:55:00'),
(9, '1', '1', 'song', '2023-06-26 07:55:12'),
(10, '2', '1', 'album', '2023-06-26 07:55:31'),
(11, '2', '1', 'song', '2023-06-26 07:55:34'),
(12, '4', '1', 'song', '2023-06-26 07:55:39'),
(13, '2', '1', 'artist', '2023-06-26 07:56:25'),
(14, '4', '1', 'song', '2023-06-26 07:57:44'),
(15, '1', '2', 'album', '2023-06-26 07:58:35'),
(16, '1', '2', 'song', '2023-06-26 07:58:45'),
(17, '1', '1', 'song', '2023-06-26 08:06:24'),
(18, '3', '1', 'song', '2023-06-26 08:06:26'),
(19, '2', '1', 'song', '2023-06-26 08:06:29'),
(20, '4', '1', 'song', '2023-06-26 08:06:31'),
(21, '1', '1', 'song', '2023-06-26 08:08:41'),
(22, '1', '1', 'song', '2023-06-26 09:16:49'),
(23, '1', '1', 'song', '2023-06-26 09:18:41'),
(24, '1', '1', 'song', '2023-06-26 09:20:13'),
(25, '1', '1', 'album', '2023-06-26 09:21:28'),
(26, '1', '1', 'album', '2023-06-26 09:28:34'),
(27, '1', '1', 'song', '2023-06-26 09:29:06'),
(28, '1', '1', 'song', '2023-06-26 09:30:06'),
(29, '1', '1', 'song', '2023-06-26 09:33:52'),
(30, '1', '2', 'album', '2023-06-26 11:56:06'),
(31, '1', '2', 'song', '2023-06-26 11:56:11'),
(32, '1', '2', 'album', '2023-06-26 12:44:04'),
(33, '1', '2', 'song', '2023-06-26 12:44:06'),
(34, '2', '2', 'album', '2023-06-26 12:45:52'),
(35, '2', '2', 'song', '2023-06-26 12:45:56'),
(36, '4', '2', 'song', '2023-06-26 12:46:29'),
(37, '2', '2', 'album', '2023-06-26 12:47:41'),
(38, '2', '2', 'album', '2023-06-26 12:48:29'),
(39, '1', '2', 'song', '2023-06-26 12:59:43'),
(40, '3', '2', 'album', '2023-06-26 13:08:00'),
(41, '3', '2', 'song', '2023-06-26 13:08:03'),
(42, '3', '2', 'album', '2023-06-26 13:08:14'),
(43, '2', '2', 'album', '2023-06-26 13:08:20'),
(44, '1', '2', 'artist', '2023-06-26 13:08:39'),
(45, '1', '2', 'artist', '2023-06-26 13:18:18'),
(46, '2', '2', 'album', '2023-06-26 13:57:28'),
(47, '2', '2', 'song', '2023-06-26 13:57:33'),
(48, '2', '2', 'artist', '2023-06-26 14:24:02'),
(49, '4', '2', 'song', '2023-06-26 14:24:04'),
(50, '2', '2', 'album', '2023-06-26 14:24:11'),
(51, '2', '2', 'album', '2023-06-26 14:24:21'),
(52, '2', '2', 'artist', '2023-06-26 14:24:27'),
(53, '2', '2', 'song', '2023-06-27 12:24:38'),
(54, '1', '2', 'album', '2023-06-27 12:43:31'),
(55, '1', '2', 'song', '2023-06-27 12:43:33'),
(56, '1', '2', 'song', '2023-06-27 12:43:39'),
(57, '1', '2', 'song', '2023-06-27 12:43:40'),
(58, '1', '2', 'song', '2023-06-27 12:43:41'),
(59, '1', '2', 'song', '2023-06-27 12:43:42'),
(60, '1', '2', 'song', '2023-06-27 12:43:43'),
(61, '1', '2', 'song', '2023-06-27 12:43:43'),
(62, '1', '2', 'song', '2023-06-27 12:43:43'),
(63, '1', '2', 'song', '2023-06-27 12:43:43'),
(64, '1', '2', 'song', '2023-06-27 12:43:43'),
(65, '1', '2', 'song', '2023-06-27 12:43:43'),
(66, '1', '2', 'song', '2023-06-27 12:43:44'),
(67, '1', '2', 'song', '2023-06-27 12:43:44'),
(68, '1', '2', 'song', '2023-06-27 12:43:44'),
(69, '2', '1', 'album', '2023-06-27 16:54:15'),
(70, '4', '1', 'song', '2023-06-27 16:54:19'),
(71, '4', '1', 'song', '2023-06-27 16:54:20'),
(72, '4', '1', 'song', '2023-06-27 16:54:21'),
(73, '4', '1', 'song', '2023-06-27 16:54:21'),
(74, '4', '1', 'song', '2023-06-27 16:54:22'),
(75, '4', '1', 'song', '2023-06-27 16:54:22'),
(76, '4', '1', 'song', '2023-06-27 16:54:23'),
(77, '4', '1', 'song', '2023-06-27 16:54:23'),
(78, '4', '1', 'song', '2023-06-27 16:54:23'),
(79, '4', '1', 'song', '2023-06-27 16:54:23'),
(80, '4', '1', 'song', '2023-06-27 16:54:23'),
(81, '4', '1', 'song', '2023-06-27 16:54:23'),
(82, '4', '1', 'song', '2023-06-27 16:54:24'),
(83, '4', '1', 'song', '2023-06-27 16:54:24'),
(84, '3', '1', 'album', '2023-06-27 16:54:35'),
(85, '3', '1', 'song', '2023-06-27 16:54:36'),
(86, '3', '1', 'song', '2023-06-27 16:54:37'),
(87, '3', '1', 'song', '2023-06-27 16:54:37'),
(88, '3', '1', 'song', '2023-06-27 16:54:37'),
(89, '3', '1', 'song', '2023-06-27 16:54:38'),
(90, '1', '1', 'song', '2023-06-27 17:31:17'),
(91, '3', '1', 'song', '2023-06-27 17:32:28'),
(92, '2', '1', 'song', '2023-06-27 17:32:40'),
(93, '4', '1', 'song', '2023-06-27 17:32:50'),
(94, '1', '1', 'album', '2023-06-27 17:33:16'),
(95, '1', '1', 'artist', '2023-06-27 17:33:29'),
(96, '2', '2', 'album', '2023-06-27 17:59:19'),
(97, '2', '2', 'song', '2023-06-27 17:59:22'),
(98, '2', '2', 'song', '2023-06-27 17:59:50'),
(99, '2', '2', 'song', '2023-06-27 18:01:08'),
(100, '2', '1', 'album', '2023-06-27 19:02:09'),
(101, '4', '1', 'song', '2023-06-27 19:02:12'),
(102, '4', '1', 'song', '2023-06-27 19:02:17'),
(103, '4', '1', 'song', '2023-06-27 19:02:19'),
(104, '4', '1', 'song', '2023-06-27 19:04:52'),
(105, '4', '1', 'song', '2023-06-27 19:04:53'),
(106, '4', '1', 'song', '2023-06-27 19:04:53'),
(107, '4', '1', 'song', '2023-06-27 19:04:54'),
(108, '4', '1', 'song', '2023-06-27 19:04:54'),
(109, '4', '1', 'song', '2023-06-27 19:04:55'),
(110, '4', '1', 'song', '2023-06-27 19:04:55'),
(111, '4', '1', 'song', '2023-06-27 19:04:55'),
(112, '4', '1', 'song', '2023-06-27 19:04:56'),
(113, '4', '1', 'song', '2023-06-27 19:04:56'),
(114, '4', '1', 'song', '2023-06-27 19:04:56'),
(115, '3', '2', 'album', '2023-06-29 07:44:30'),
(116, '3', '2', 'song', '2023-06-29 07:44:34'),
(117, '1', '2', 'album', '2023-06-29 07:45:37'),
(118, '1', '2', 'album', '2023-06-29 07:45:41'),
(119, '1', '2', 'album', '2023-06-29 07:45:44'),
(120, '2', '2', 'artist', '2023-06-29 12:20:46'),
(121, '1', '2', 'album', '2023-06-29 19:02:04'),
(122, '1', '2', 'song', '2023-06-29 19:02:09'),
(123, '2', '2', 'song', '2023-06-29 19:02:17'),
(124, '1', '2', 'song', '2023-06-29 19:02:20'),
(125, '1', '1', 'song', '2023-06-30 06:18:31'),
(126, '4', '1', 'song', '2023-06-30 06:19:07'),
(127, '2', '1', 'song', '2023-06-30 06:19:11'),
(128, '3', '1', 'song', '2023-06-30 06:19:15'),
(129, '1', '1', 'song', '2023-06-30 06:19:25'),
(130, '4', '1', 'song', '2023-06-30 06:19:28'),
(131, '4', '1', 'song', '2023-06-30 06:20:54'),
(132, '1', '1', 'artist', '2023-06-30 06:21:05'),
(133, '1', '1', 'song', '2023-06-30 06:21:07'),
(134, '2', '1', 'artist', '2023-06-30 06:21:12'),
(135, '4', '1', 'song', '2023-06-30 06:21:15'),
(136, '2', '1', 'song', '2023-06-30 06:21:18'),
(137, '3', '1', 'album', '2023-06-30 06:21:21'),
(138, '3', '2', 'album', '2023-06-30 21:06:41'),
(139, '3', '2', 'song', '2023-06-30 21:06:45'),
(140, '3', '1', 'album', '2023-07-01 10:24:40'),
(141, '3', '1', 'album', '2023-07-01 10:24:44'),
(142, '3', '1', 'album', '2023-07-01 10:24:48'),
(143, '3', '1', 'album', '2023-07-01 10:24:51'),
(144, '3', '1', 'album', '2023-07-01 10:24:56'),
(145, '3', '1', 'album', '2023-07-01 10:24:59'),
(146, '3', '1', 'album', '2023-07-01 10:25:03'),
(147, '3', '1', 'album', '2023-07-01 10:25:06'),
(148, '3', '1', 'album', '2023-07-01 10:25:09'),
(149, '3', '1', 'album', '2023-07-01 10:25:14'),
(150, '3', '1', 'album', '2023-07-01 10:25:17'),
(151, '3', '2', 'album', '2023-07-01 10:27:02'),
(152, '3', '1', 'album', '2023-07-01 10:28:25'),
(153, '2', '1', 'album', '2023-07-01 10:30:54'),
(154, '4', '1', 'album', '2023-07-01 11:53:53'),
(155, '3', '1', 'album', '2023-07-01 11:54:59'),
(156, '3', '2', 'album', '2023-07-01 12:53:47'),
(157, '2', '2', 'artist', '2023-07-01 13:37:49'),
(158, '3', '2', 'album', '2023-07-01 14:14:52'),
(159, '2', '2', 'artist', '2023-07-01 14:15:14'),
(160, '1', '2', 'album', '2023-07-01 14:15:19'),
(161, '2', '2', 'album', '2023-07-01 14:15:23'),
(162, '1', '2', 'artist', '2023-07-01 14:15:32'),
(163, '2', '2', 'artist', '2023-07-01 14:15:39'),
(164, '4', '2', 'song', '2023-07-01 17:46:19'),
(165, '1', '2', 'song', '2023-07-01 17:47:55'),
(166, '1', '2', 'song', '2023-07-01 17:47:57'),
(167, '1', '2', 'song', '2023-07-01 17:47:59'),
(168, '1', '2', 'song', '2023-07-01 17:48:00'),
(169, '1', '2', 'song', '2023-07-01 17:48:01'),
(170, '3', '2', 'album', '2023-07-01 17:51:14'),
(171, '1', '2', 'artist', '2023-07-01 19:13:13'),
(172, '2', '2', 'artist', '2023-07-01 19:13:39'),
(173, '1', '1', 'song', '2023-07-02 07:32:00'),
(174, '2', '1', 'artist', '2023-07-02 07:34:24'),
(175, '3', '1', 'album', '2023-07-02 13:08:15'),
(176, '1', '1', 'artist', '2023-07-02 14:32:00'),
(177, '3', '1', 'album', '2023-07-02 14:32:45'),
(178, '3', '1', 'album', '2023-07-02 19:28:16'),
(179, '3', '1', 'album', '2023-07-03 07:25:35'),
(180, '1', '1', 'album', '2023-07-03 07:25:42'),
(181, '2', '1', 'album', '2023-07-03 07:25:46'),
(182, '1', '1', 'artist', '2023-07-03 07:26:05'),
(183, '1', '1', 'album', '2023-07-03 07:26:15'),
(184, '1', '1', 'album', '2023-07-03 09:41:48'),
(185, '4', '1', 'song', '2023-07-03 10:42:58'),
(186, '1', '1', 'artist', '2023-07-03 14:01:41'),
(187, '2', '1', 'artist', '2023-07-03 14:09:28'),
(188, '1', '1', 'album', '2023-07-03 14:09:51'),
(189, '4', '1', 'album', '2023-07-03 15:42:25'),
(190, '1', '1', 'album', '2023-07-03 15:57:33'),
(191, '1', '1', 'song', '2023-07-03 15:59:59'),
(192, '1', '1', 'song', '2023-07-03 16:53:58'),
(193, '1', '1', 'album', '2023-07-03 17:22:16'),
(194, '2', '1', 'artist', '2023-07-03 17:22:21'),
(195, '1', '1', 'album', '2023-07-03 17:23:17'),
(196, '1', '1', 'album', '2023-07-03 17:26:31'),
(197, '1', '1', 'album', '2023-07-03 17:26:44'),
(198, '1', '1', 'album', '2023-07-03 17:27:01'),
(199, '1', '1', 'album', '2023-07-03 17:27:28'),
(200, '1', '1', 'album', '2023-07-03 18:57:24'),
(201, '1', '1', 'album', '2023-07-03 19:09:41'),
(202, '1', '1', 'song', '2023-07-03 19:09:51'),
(203, '1', '1', 'song', '2023-07-03 19:19:41'),
(204, '2', '1', 'song', '2023-07-03 19:20:04'),
(205, '1', '1', 'song', '2023-07-03 19:20:35'),
(206, '2', '1', 'artist', '2023-07-03 19:36:18'),
(207, '2', '1', 'album', '2023-07-03 19:57:35'),
(208, '1', '1', 'album', '2023-07-03 20:05:43'),
(209, '1', '1', 'album', '2023-07-03 20:45:13'),
(210, '2', '1', 'artist', '2023-07-09 22:31:09'),
(211, '1', '1', 'song', '2023-07-09 22:32:27'),
(212, '1', '1', 'song', '2023-07-09 22:32:29'),
(213, '1', '1', 'song', '2023-07-10 11:38:26'),
(214, '2', '1', 'song', '2023-07-10 11:38:31'),
(215, '1', '1', 'artist', '2023-07-10 13:52:39'),
(216, '1', '1', 'song', '2023-07-10 17:44:54'),
(217, '3', '1', 'album', '2023-07-12 05:42:14'),
(218, '1', '1', 'album', '2023-07-12 07:12:59'),
(219, '1', '1', 'album', '2023-07-12 10:13:26'),
(220, '1', '1', 'album', '2023-07-12 10:15:16'),
(221, '1', '1', 'album', '2023-07-12 10:19:57'),
(222, '1', '1', 'album', '2023-07-12 10:22:10'),
(223, '1', '1', 'album', '2023-07-12 10:43:36'),
(224, '1', '1', 'album', '2023-07-12 10:47:22'),
(225, '1', '1', 'album', '2023-07-12 10:47:42'),
(226, '1', '1', 'album', '2023-07-12 10:48:14'),
(227, '1', '1', 'album', '2023-07-12 10:52:02'),
(228, '1', '1', 'album', '2023-07-12 10:52:45'),
(229, '1', '1', 'album', '2023-07-12 10:54:02'),
(230, '1', '1', 'album', '2023-07-12 10:54:10'),
(231, '3', '1', 'song', '2023-07-12 10:55:57'),
(232, '1', '1', 'album', '2023-07-12 11:32:13'),
(233, '1', '1', 'album', '2023-07-12 11:38:00'),
(234, '1', '1', 'album', '2023-07-12 11:40:12'),
(235, '1', '1', 'album', '2023-07-12 11:41:07'),
(236, '1', '1', 'album', '2023-07-12 11:41:30'),
(237, '1', '1', 'album', '2023-07-12 11:42:09'),
(238, '1', '1', 'album', '2023-07-12 11:42:29'),
(239, '1', '1', 'album', '2023-07-12 11:45:45'),
(240, '3', '1', 'album', '2023-07-12 13:20:21'),
(241, '1', '1', 'album', '2023-07-12 13:26:58'),
(242, '1', '1', 'album', '2023-07-12 13:27:16'),
(243, '1', '1', 'album', '2023-07-12 13:27:46'),
(244, '1', '1', 'album', '2023-07-12 13:28:07'),
(245, '1', '1', 'album', '2023-07-12 13:28:27'),
(246, '1', '1', 'album', '2023-07-12 13:28:44'),
(247, '1', '1', 'album', '2023-07-12 13:29:44'),
(248, '1', '1', 'album', '2023-07-12 13:30:03'),
(249, '1', '1', 'album', '2023-07-12 13:30:15'),
(250, '1', '1', 'album', '2023-07-12 13:32:28'),
(251, '1', '1', 'album', '2023-07-12 13:33:34'),
(252, '1', '1', 'album', '2023-07-12 13:34:40'),
(253, '1', '1', 'album', '2023-07-12 13:34:54'),
(254, '1', '1', 'album', '2023-07-12 13:35:06'),
(255, '1', '1', 'album', '2023-07-12 13:35:20'),
(256, '1', '1', 'album', '2023-07-12 13:35:54'),
(257, '1', '1', 'album', '2023-07-12 13:36:11'),
(258, '1', '1', 'album', '2023-07-12 13:37:04'),
(259, '1', '1', 'album', '2023-07-12 13:37:51'),
(260, '1', '1', 'album', '2023-07-12 13:38:06'),
(261, '1', '1', 'album', '2023-07-12 13:38:20'),
(262, '1', '1', 'album', '2023-07-12 13:39:29'),
(263, '1', '1', 'album', '2023-07-12 13:39:44'),
(264, '1', '1', 'album', '2023-07-12 13:39:58'),
(265, '1', '1', 'album', '2023-07-12 13:41:15'),
(266, '1', '1', 'album', '2023-07-12 13:42:16'),
(267, '1', '1', 'album', '2023-07-12 13:42:38'),
(268, '1', '1', 'album', '2023-07-12 13:42:54'),
(269, '1', '1', 'album', '2023-07-12 13:43:06'),
(270, '1', '1', 'album', '2023-07-12 13:43:27'),
(271, '1', '1', 'album', '2023-07-12 13:45:03'),
(272, '1', '1', 'album', '2023-07-12 13:45:23'),
(273, '1', '1', 'album', '2023-07-12 13:45:35'),
(274, '1', '1', 'album', '2023-07-12 13:46:30'),
(275, '1', '1', 'album', '2023-07-12 13:46:39'),
(276, '1', '1', 'album', '2023-07-12 13:46:51'),
(277, '1', '1', 'album', '2023-07-12 13:47:14'),
(278, '1', '1', 'album', '2023-07-12 13:48:36'),
(279, '1', '1', 'album', '2023-07-12 13:48:47'),
(280, '1', '1', 'album', '2023-07-12 13:49:33'),
(281, '1', '1', 'album', '2023-07-12 13:51:33'),
(282, '1', '1', 'album', '2023-07-12 13:51:56'),
(283, '1', '1', 'album', '2023-07-12 13:53:04'),
(284, '1', '1', 'song', '2023-07-12 13:53:29'),
(285, '3', '1', 'album', '2023-07-12 13:59:03'),
(286, '3', '1', 'album', '2023-07-12 14:21:11'),
(287, '1', '1', 'album', '2023-07-12 15:25:09'),
(288, '1', '1', 'album', '2023-07-12 15:25:56'),
(289, '1', '1', 'album', '2023-07-12 15:27:04'),
(290, '1', '1', 'artist', '2023-07-12 15:27:12'),
(291, '1', '1', 'album', '2023-07-12 15:32:01'),
(292, '1', '1', 'album', '2023-07-12 15:32:26'),
(293, '1', '1', 'album', '2023-07-12 15:32:38'),
(294, '1', '1', 'album', '2023-07-12 15:35:36'),
(295, '1', '1', 'album', '2023-07-12 15:35:50'),
(296, '1', '1', 'album', '2023-07-12 15:36:03'),
(297, '1', '1', 'album', '2023-07-12 15:37:00'),
(298, '1', '1', 'album', '2023-07-12 15:43:27'),
(299, '1', '1', 'album', '2023-07-12 15:44:43'),
(300, '1', '1', 'album', '2023-07-12 15:46:01'),
(301, '1', '1', 'album', '2023-07-12 15:46:32'),
(302, '3', '1', 'album', '2023-07-12 18:26:47'),
(303, '1', '1', 'song', '2023-07-12 18:28:33'),
(304, '3', '1', 'album', '2023-07-12 20:07:02'),
(305, '3', '1', 'album', '2023-07-12 20:10:19'),
(306, '3', '1', 'album', '2023-07-12 20:11:04'),
(307, '3', '1', 'album', '2023-07-12 20:11:50'),
(308, '3', '1', 'album', '2023-07-12 20:12:11'),
(309, '3', '1', 'album', '2023-07-12 20:12:17'),
(310, '3', '1', 'album', '2023-07-12 20:12:25'),
(311, '3', '1', 'album', '2023-07-12 20:12:38'),
(312, '3', '1', 'album', '2023-07-12 20:12:46'),
(313, '3', '1', 'album', '2023-07-12 20:13:39'),
(314, '3', '1', 'album', '2023-07-12 20:13:58'),
(315, '3', '1', 'album', '2023-07-12 20:15:04'),
(316, '3', '1', 'album', '2023-07-12 20:15:23'),
(317, '3', '1', 'album', '2023-07-12 20:15:30'),
(318, '3', '1', 'album', '2023-07-12 20:17:16'),
(319, '1', '1', 'album', '2023-07-12 20:22:07'),
(320, '1', '1', 'album', '2023-07-12 20:22:33'),
(321, '1', '1', 'album', '2023-07-12 20:24:59'),
(322, '1', '1', 'song', '2023-07-12 20:25:10'),
(323, '1', '1', 'song', '2023-07-12 20:31:14'),
(324, '2', '1', 'album', '2023-07-12 20:31:37'),
(325, '2', '1', 'album', '2023-07-12 20:33:13'),
(326, '2', '1', 'album', '2023-07-12 20:34:33'),
(327, '2', '1', 'album', '2023-07-12 20:34:50'),
(328, '2', '1', 'album', '2023-07-12 20:35:03'),
(329, '2', '1', 'album', '2023-07-12 20:36:01'),
(330, '2', '1', 'album', '2023-07-12 20:36:55'),
(331, '1', '1', 'song', '2023-07-16 11:10:30'),
(332, '1', '1', 'song', '2023-07-16 11:12:29'),
(333, '1', '1', 'song', '2023-07-16 11:13:13'),
(334, '1', '1', 'song', '2023-07-16 11:14:42'),
(335, '1', '1', 'song', '2023-07-16 11:16:01'),
(336, '1', '1', 'song', '2023-07-16 11:17:56'),
(337, '1', '1', 'song', '2023-07-16 11:19:13'),
(338, '1', '1', 'song', '2023-07-16 11:20:13'),
(339, '1', '1', 'song', '2023-07-16 11:23:01'),
(340, '1', '1', 'song', '2023-07-16 11:24:12'),
(341, '1', '1', 'song', '2023-07-16 11:24:26'),
(342, '1', '1', 'song', '2023-07-16 11:27:03'),
(343, '1', '1', 'song', '2023-07-16 11:27:33'),
(344, '1', '1', 'song', '2023-07-16 11:30:18'),
(345, '1', '1', 'song', '2023-07-16 11:31:49'),
(346, '1', '1', 'song', '2023-07-16 11:32:29'),
(347, '1', '1', 'song', '2023-07-16 11:32:49'),
(348, '1', '1', 'song', '2023-07-16 11:33:27'),
(349, '1', '1', 'song', '2023-07-16 11:33:37'),
(350, '1', '1', 'song', '2023-07-16 11:35:44'),
(351, '1', '1', 'song', '2023-07-16 11:49:47'),
(352, '1', '1', 'song', '2023-07-16 11:52:46'),
(353, '1', '1', 'song', '2023-07-16 11:58:28'),
(354, '1', '1', 'song', '2023-07-16 11:59:35'),
(355, '1', '1', 'song', '2023-07-16 12:04:33'),
(356, '1', '1', 'song', '2023-07-16 12:05:57'),
(357, '1', '1', 'song', '2023-07-16 13:36:58'),
(358, '1', '1', 'song', '2023-07-16 13:46:28'),
(359, '1', '1', 'song', '2023-07-16 13:48:01'),
(360, '1', '1', 'song', '2023-07-16 13:50:09'),
(361, '1', '1', 'song', '2023-07-16 13:51:20'),
(362, '1', '1', 'song', '2023-07-16 13:53:24'),
(363, '1', '1', 'song', '2023-07-16 13:55:04'),
(364, '1', '1', 'song', '2023-07-16 13:55:19'),
(365, '1', '1', 'song', '2023-07-16 13:55:47'),
(366, '1', '1', 'album', '2023-07-16 14:00:37'),
(367, '1', '1', 'artist', '2023-07-16 14:00:47'),
(368, '1', '1', 'album', '2023-07-16 14:01:00'),
(369, '2', '1', 'artist', '2023-07-16 14:01:07'),
(370, '1', '1', 'song', '2023-07-16 14:33:15'),
(371, '1', '1', 'song', '2023-07-16 14:33:17'),
(372, '1', '1', 'song', '2023-07-16 14:39:21'),
(373, '4', '1', 'song', '2023-07-16 14:39:23'),
(374, '1', '1', 'album', '2023-07-16 14:42:51'),
(375, '1', '1', 'album', '2023-07-16 14:43:10'),
(376, '1', '1', 'album', '2023-07-16 14:43:40'),
(377, '1', '1', 'album', '2023-07-16 14:43:50'),
(378, '1', '1', 'album', '2023-07-16 14:44:33'),
(379, '1', '1', 'album', '2023-07-16 14:44:47'),
(380, '1', '1', 'album', '2023-07-16 14:45:29'),
(381, '1', '1', 'album', '2023-07-16 14:46:02'),
(382, '1', '1', 'album', '2023-07-16 14:46:20'),
(383, '1', '1', 'album', '2023-07-16 14:46:47'),
(384, '1', '1', 'album', '2023-07-16 14:46:58'),
(385, '1', '1', 'album', '2023-07-16 15:28:04'),
(386, '1', '1', 'song', '2023-07-16 15:32:28'),
(387, '2', '1', 'song', '2023-07-16 15:32:30'),
(388, '4', '1', 'song', '2023-07-16 15:32:32'),
(389, '1', '1', 'album', '2023-07-16 15:33:12'),
(390, '2', '1', 'album', '2023-07-17 07:12:22'),
(391, '2', '1', 'album', '2023-07-17 07:41:09'),
(392, '3', '1', 'album', '2023-07-17 08:32:29'),
(393, '3', '1', 'album', '2023-07-17 08:45:48'),
(394, '3', '1', 'album', '2023-07-17 08:46:27'),
(395, '3', '1', 'song', '2023-07-17 08:47:39'),
(396, '3', '1', 'song', '2023-07-17 08:49:26'),
(397, '3', '1', 'song', '2023-07-17 08:52:48'),
(398, '3', '1', 'song', '2023-07-17 08:53:19'),
(399, '3', '1', 'song', '2023-07-17 08:53:26'),
(400, '3', '1', 'song', '2023-07-17 08:53:31'),
(401, '3', '1', 'song', '2023-07-17 08:53:35'),
(402, '3', '1', 'album', '2023-07-17 08:54:14'),
(403, '3', '1', 'album', '2023-07-17 08:54:27'),
(404, '3', '1', 'album', '2023-07-17 08:54:31'),
(405, '1', '2', 'artist', '2023-07-17 10:45:49'),
(406, '1', '2', 'artist', '2023-07-17 10:47:52'),
(410, '1', '1', 'album', '2023-07-18 10:51:15'),
(411, '1', '1', 'album', '2023-07-19 06:08:55'),
(412, '1', '1', 'song', '2023-07-19 06:09:02'),
(413, '1', '1', 'song', '2023-07-19 06:55:43'),
(414, '1', '1', 'song', '2023-07-19 06:55:46'),
(415, '1', '1', 'album', '2023-07-19 06:56:39'),
(416, '1', '1', 'album', '2023-07-19 06:56:55'),
(417, '3', '1', 'album', '2023-07-19 06:57:05'),
(418, '2', '1', 'artist', '2023-07-19 06:57:17'),
(419, '2', '1', 'song', '2023-07-19 06:57:39'),
(420, '1', '2', 'album', '2023-07-19 07:14:23'),
(422, '1', '1', 'album', '2023-07-19 18:55:16'),
(424, '1', '1', 'album', '2023-07-19 18:56:21'),
(425, '1', '2', 'album', '2023-07-19 19:01:44'),
(426, '1', '1', 'album', '2023-07-23 07:08:38'),
(438, '1', '1', 'album', '2023-07-23 18:49:33'),
(428, '2', '1', 'album', '2023-07-23 07:14:32'),
(429, '2', '1', 'song', '2023-07-23 07:14:36'),
(430, '1', '1', 'album', '2023-07-23 07:14:43'),
(431, '1', '1', 'song', '2023-07-23 07:14:45'),
(432, '1', '1', 'album', '2023-07-23 07:35:09'),
(433, '2', '1', 'album', '2023-07-23 07:35:30'),
(434, '1', '1', 'album', '2023-07-23 07:37:52'),
(435, '1', '1', 'artist', '2023-07-23 07:43:28'),
(436, '2', '1', 'artist', '2023-07-23 07:43:35'),
(437, '1', '1', 'artist', '2023-07-23 07:43:48'),
(439, '3', '1', 'album', '2023-07-23 18:49:38'),
(440, '2', '1', 'album', '2023-07-23 18:49:41'),
(441, '2', '2', 'artist', '2023-07-26 09:10:30'),
(442, '2', '2', 'artist', '2023-07-26 09:10:30'),
(443, '4', '2', 'song', '2023-07-26 09:10:57'),
(444, '1', '2', 'song', '2023-07-26 09:11:50'),
(445, '2', '1', 'album', '2023-07-30 06:56:14');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
CREATE TABLE IF NOT EXISTS `likes` (
  `like_id` int(11) NOT NULL AUTO_INCREMENT,
  `content_id` varchar(25) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content_type` varchar(50) NOT NULL,
  PRIMARY KEY (`like_id`)
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`like_id`, `content_id`, `user_id`, `timestamp`, `content_type`) VALUES
(48, '1', '2', '2023-06-26 11:56:16', 'album'),
(62, '1', '1', '2023-07-17 10:41:18', 'song'),
(31, '1', '1', '2023-06-25 11:49:09', 'album'),
(49, '3', '2', '2023-06-26 13:08:46', 'song'),
(59, '3', '1', '2023-07-17 08:54:21', 'song'),
(52, '3', '1', '2023-07-01 11:55:03', 'album'),
(38, '1', '1', '2023-06-25 15:38:22', 'artist'),
(68, '4', '2', '2023-07-26 09:11:16', 'song'),
(42, '4', '1', '2023-06-25 18:15:49', 'song'),
(47, '1', '2', '2023-06-26 11:56:13', 'song'),
(51, '3', '2', '2023-07-01 10:27:05', 'album'),
(53, '2', '2', '2023-07-01 13:37:53', 'artist'),
(63, '1', '2', '2023-07-17 10:47:58', 'artist');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`login_id`, `username`, `password`, `user_type`, `status`) VALUES
(1, 'admin', 'Admin', 'admin', 'active'),
(2, 'akshay', 'Akshay', 'user', 'active'),
(3, 'anjuk', 'Anju', 'user', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
CREATE TABLE IF NOT EXISTS `notification` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(25) NOT NULL,
  `content_id` varchar(50) NOT NULL,
  `content` varchar(255) NOT NULL,
  `content_status` varchar(50) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(50) NOT NULL,
  `notification_type` varchar(50) NOT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`notification_id`, `user_id`, `content_id`, `content`, `content_status`, `timestamp`, `status`, `notification_type`) VALUES
(1, '1', '1', 'Song pending for approval', 'pending', '2023-06-07 08:09:26', 'read', 'approvals'),
(2, '2', '1', 'Song Approved', 'approved', '2023-06-07 08:10:34', 'read', 'approvals'),
(3, '1', '2', 'Song pending for approval', 'pending', '2023-06-20 12:32:29', 'read', 'approvals'),
(4, '2', '2', 'Song Approved', 'approved', '2023-06-20 12:34:10', 'read', 'approvals'),
(5, '1', '3', 'Song pending for approval', 'pending', '2023-06-20 18:40:40', 'read', 'approvals'),
(6, '3', '3', 'Song Approved', 'approved', '2023-06-20 18:44:01', 'read', 'approvals'),
(7, '1', '4', 'Song pending for approval', 'pending', '2023-06-20 19:03:08', 'read', 'approvals'),
(8, '3', '4', 'Song Approved', 'approved', '2023-06-20 19:03:25', 'read', 'approvals'),
(9, '2', '2', 'Song removed from artist', 'artistremoved', '2023-06-24 10:22:06', 'read', 'songremoval'),
(10, '2', '2', 'Song removed from artist', 'artistremoved', '2023-06-24 10:25:02', 'read', 'songremoval'),
(11, '2', '2', 'Song removed from artist', 'artistremoved', '2023-06-24 10:41:38', 'read', 'songremoval'),
(12, '2', '2', 'Song removed from artist', 'artistremoved', '2023-06-24 10:59:56', 'read', 'songremoval'),
(13, '2', '2', 'Song removed from album', 'albumremoved', '2023-06-24 11:03:34', 'read', 'songremoval'),
(14, '3', '4', 'Song removed from album', 'albumremoved', '2023-06-24 11:13:31', 'read', 'songremoval'),
(15, '3', '4', 'Song removed from artist', 'artistremoved', '2023-06-24 11:13:51', 'read', 'songremoval'),
(16, '1', '5', 'Song pending for approval', 'pending', '2023-07-17 14:04:33', 'read', 'approvals'),
(17, '3', '5', 'Song Approved', 'approved', '2023-07-17 14:05:43', 'read', 'approvals'),
(18, '1', '6', 'Song pending for approval', 'pending', '2023-07-17 15:20:52', 'read', 'approvals'),
(19, '3', '6', 'Song Approved', 'approved', '2023-07-17 15:21:53', 'read', 'approvals'),
(20, '3', '6', 'Song removed from artist', 'artistremoved', '2023-07-17 15:22:30', 'read', 'songremoval'),
(21, '1', '7', 'Song pending for approval', 'pending', '2023-07-19 07:09:09', 'read', 'approvals'),
(22, '2', '7', 'Song Approved', 'approved', '2023-07-19 07:11:31', 'read', 'approvals'),
(23, '1', '8', 'Song pending for approval', 'pending', '2023-07-19 18:53:40', 'read', 'approvals'),
(24, '2', '8', 'Song Approved', 'approved', '2023-07-19 18:55:02', 'read', 'approvals'),
(25, '1', '9', 'Song pending for approval', 'pending', '2023-07-19 18:58:06', 'read', 'approvals'),
(26, '2', '9', 'Song Approved', 'approved', '2023-07-19 18:58:46', 'read', 'approvals');

-- --------------------------------------------------------

--
-- Table structure for table `playlist`
--

DROP TABLE IF EXISTS `playlist`;
CREATE TABLE IF NOT EXISTS `playlist` (
  `playlist_id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_name` varchar(255) NOT NULL,
  `image_loc` varchar(255) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`playlist_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `playlist`
--

INSERT INTO `playlist` (`playlist_id`, `playlist_name`, `image_loc`, `user_id`, `status`, `type`) VALUES
(1, 'My Songs', 'uploads/playlist/1.jpg', '1', 'active', 'private'),
(2, 'Romantic songs', 'uploads/playlist/2.jpg', '1', 'active', 'private'),
(11, 'Daily', 'uploads/playlist/11.jpg', '0', 'active', 'public'),
(10, 'Discover Weekly', 'uploads/playlist/10.jpg', '0', 'deactive', 'public');

-- --------------------------------------------------------

--
-- Table structure for table `playlisttrack`
--

DROP TABLE IF EXISTS `playlisttrack`;
CREATE TABLE IF NOT EXISTS `playlisttrack` (
  `playlisttrack_id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_id` varchar(50) NOT NULL,
  `song_id` varchar(50) NOT NULL,
  PRIMARY KEY (`playlisttrack_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `playlisttrack`
--

INSERT INTO `playlisttrack` (`playlisttrack_id`, `playlist_id`, `song_id`) VALUES
(6, '1', '3'),
(3, '1', '4'),
(4, '1', '2'),
(7, '2', '1'),
(23, '11', '1'),
(21, '10', '3'),
(25, '10', '1'),
(24, '11', '4');

-- --------------------------------------------------------

--
-- Table structure for table `songartist`
--

DROP TABLE IF EXISTS `songartist`;
CREATE TABLE IF NOT EXISTS `songartist` (
  `songartist_id` int(11) NOT NULL AUTO_INCREMENT,
  `song_id` varchar(25) NOT NULL,
  `artist_id` varchar(25) NOT NULL,
  PRIMARY KEY (`songartist_id`)
) ENGINE=MyISAM AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songartist`
--

INSERT INTO `songartist` (`songartist_id`, `song_id`, `artist_id`) VALUES
(28, '3', '1'),
(26, '4', '2'),
(25, '2', '2'),
(31, '1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

DROP TABLE IF EXISTS `songs`;
CREATE TABLE IF NOT EXISTS `songs` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `album_id` varchar(25) NOT NULL,
  `song_name` varchar(255) NOT NULL,
  `image_loc` varchar(255) NOT NULL,
  `song_loc` varchar(255) NOT NULL,
  `genre` varchar(50) NOT NULL,
  `date` varchar(50) NOT NULL,
  `language` varchar(50) NOT NULL,
  `user_id` varchar(25) NOT NULL,
  `privacy` varchar(25) NOT NULL,
  `duration` varchar(25) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`song_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`song_id`, `album_id`, `song_name`, `image_loc`, `song_loc`, `genre`, `date`, `language`, `user_id`, `privacy`, `duration`, `status`) VALUES
(1, '1', 'Pavizha Mazha', 'uploads/songs/image/Pavizha Mazha.jpg', '/static/uploads/songs/Akshayb53e7184-bec9-4076-95ea-8cc27f07012a.mp3', 'classical', '2023-06-04', 'Malayalam', '1', 'public', '3:53', 'approved'),
(2, '2', 'Manasse Manasse', 'uploads/songs/image/Manasse Manasse.jpg', '/static/uploads/songs/Akshayed1039ee-0be8-4e5b-9372-09d376affae3.mp3', 'classical', '2023-06-20', 'Malayalam', '1', 'public', '3:10', 'approved'),
(3, '3', 'Kannil Kannil', 'uploads/songs/image/Kannil Kannil.jpg', '/static/uploads/songs/Anju3f9b800d-9613-40dc-b668-f34a9c11c30b.mp3', 'pop', '2023-06-21', 'Malayalam', '2', 'public', '3:52', 'approved'),
(4, '2', 'Onakka Munthiri', 'uploads/songs/image/Onakka Munthiri.jpg', '/static/uploads/songs/Anjud120f52c-920d-493b-bb91-0d7e45a4d316.mp3', 'pop', '2023-06-21', 'Malayalam', '2', 'public', '1:58', 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` varchar(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(50) NOT NULL,
  `image_loc` varchar(200) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `login_id`, `fname`, `lname`, `email`, `mobile`, `image_loc`, `status`) VALUES
(1, '2', 'Akshay', 'K S', 'akshaykeenath@gmail.com', '8848223249', 'uploads/users/1.jpg', 'active'),
(2, '3', 'Anju', 'K', 'anjugangadharan00@gmail.com', '8765986451', 'uploads/Anju3.jpg', 'active');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
