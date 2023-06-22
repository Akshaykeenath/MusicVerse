-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2023 at 03:49 PM
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
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `album`
--

INSERT INTO `album` (`album_id`, `album_name`, `image_loc`, `cover_pic`, `user_id`) VALUES
(1, 'Athiran', 'uploads/album/Athiranpropic.jpg', 'uploads/album/Athirancoverpic.jpg', '1'),
(2, 'Hridhyam', 'uploads/album/Hridhyampropic.jpg', 'uploads/album/Hridhyamcoverpic.jpg', '1'),
(3, 'Sita Ramam', 'uploads/album/Sita Ramampropic.jpg', 'uploads/album/Sita Ramamcoverpic.jpg', '2');

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
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `artist`
--

INSERT INTO `artist` (`artist_id`, `artist_name`, `image_loc`, `cover_pic`, `user_id`) VALUES
(1, 'K S Harishankar', 'uploads/artist/K S Harishankarpropic.png', 'uploads/artist/K S Harishankarcoverpic.jpg', '1'),
(2, 'Vineeth Sreenivasan', 'uploads/artist/Vineeth Sreenivasanpropic.jpg', 'uploads/artist/Vineeth Sreenivasancoverpic.jpg', '1'),
(3, 'Swetha Mohan', 'uploads/artist/Swetha Mohanpropic.jpg', 'uploads/artist/Swetha Mohancoverpic.jpg', '2');

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
(1, 'admin@musicverse.com', 'Admin', 'admin', 'active'),
(2, 'akshay@gmail.com', 'Akshay', 'user', 'active'),
(3, 'anjuk@gmail.com', 'Anju', 'user', 'active');

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
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

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
(8, '3', '4', 'Song Approved', 'approved', '2023-06-20 19:03:25', 'read', 'approvals');

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
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songartist`
--

INSERT INTO `songartist` (`songartist_id`, `song_id`, `artist_id`) VALUES
(13, '1', '1'),
(6, '3', '1'),
(4, '4', '2'),
(9, '2', '2');

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
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`song_id`, `album_id`, `song_name`, `image_loc`, `song_loc`, `genre`, `date`, `language`, `user_id`, `privacy`, `duration`, `status`) VALUES
(1, '1', 'Pavizha Mazha', 'uploads/songs/image/Pavizha Mazha.jpg', '/static/uploads/songs/Akshayb53e7184-bec9-4076-95ea-8cc27f07012a.mp3', 'classic', '2023-06-04', 'Malayalam', '1', 'public', '3:53', 'approved'),
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
(1, '2', 'Akshay', 'K S', 'akshay@gmail.com', '8848223249', 'uploads/Akshay2.jpg', 'active'),
(2, '3', 'Anju', 'K', 'anjuk@gmail.com', '8765986451', 'uploads/Anju3.jpg', 'active');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
