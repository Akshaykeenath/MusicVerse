-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jun 06, 2023 at 09:02 PM
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
  PRIMARY KEY (`album_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `album`
--

INSERT INTO `album` (`album_id`, `album_name`, `image_loc`, `cover_pic`) VALUES
(1, 'Hridhyam', 'uploads/album/Hridhyampropic.jpg', 'uploads/album/Hridhyamcoverpic.webp'),
(2, 'Athiran', 'uploads/album/Athiranpropic.jpg', 'uploads/album/Athirancoverpic.jpg'),
(3, 'Sita Ramam', 'uploads/album/Sita Ramampropic.jpg', 'uploads/album/Sita Ramamcoverpic.jpg'),
(4, 'Urumi', 'uploads/album/Urumipropic.jpg', 'uploads/album/Urumicoverpic.jpg');

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
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `artist`
--

INSERT INTO `artist` (`artist_id`, `artist_name`, `image_loc`, `cover_pic`, `user_id`) VALUES
(1, 'Vineeth Sreenivasan', 'uploads/artist/Vineeth Sreenivasanpropic.jpg', 'uploads/artist/Vineeth Sreenivasancoverpic.jpg', '1'),
(2, 'K S Harishankar', 'uploads/artist/K S Harishankarpropic.png', 'uploads/artist/K S Harishankarcoverpic.jpg', '1'),
(4, 'Swetha Mohan', 'uploads/artist/Swetha Mohanpropic.jpg', 'uploads/artist/Swetha Mohancoverpic.jpg', '1'),
(5, 'Shreya Ghoshal', 'uploads/artist/Shreya Ghoshalpropic.jpeg', 'uploads/artist/Shreya Ghoshalcoverpic.jpg', '1');

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
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`login_id`, `username`, `password`, `user_type`, `status`) VALUES
(1, 'admin', 'admin', 'admin', 'active'),
(3, 'akshay@gmail.com', 'Akshay', 'user', 'active'),
(5, 'anjuk@gmail.com', 'Anju', 'user', 'active');

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
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`notification_id`, `user_id`, `content_id`, `content`, `content_status`, `timestamp`, `status`, `notification_type`) VALUES
(1, '1', '5', 'Song pending for approval', 'pending', '2023-06-05 13:49:42', 'read', 'approvals'),
(2, '1', '6', 'Song pending for approval', 'pending', '2023-06-05 20:09:26', 'read', 'approvals'),
(3, '1', '7', 'Song pending for approval', 'pending', '2023-06-05 20:18:04', 'read', 'approvals'),
(4, '5', '7', 'Song Approved', 'approved', '2023-06-06 20:08:44', 'toread', 'approvals');

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
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songartist`
--

INSERT INTO `songartist` (`songartist_id`, `song_id`, `artist_id`) VALUES
(24, '1', '4'),
(28, '2', '4'),
(3, '3', '2'),
(4, '4', '2'),
(27, '2', '1'),
(23, '1', '1'),
(16, '7', '1'),
(15, '7', '4');

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

DROP TABLE IF EXISTS `songs`;
CREATE TABLE IF NOT EXISTS `songs` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `artist_id` varchar(25) NOT NULL,
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
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`song_id`, `artist_id`, `album_id`, `song_name`, `image_loc`, `song_loc`, `genre`, `date`, `language`, `user_id`, `privacy`, `duration`, `status`) VALUES
(1, '1', '1', 'Pottu Thotta pournami', 'uploads/songs/image/Pottu Thotta pournami.jpg', '/static/uploads/songs/Akshay1a57810e-0aab-4aab-9c6d-295f7c7f1cec.mp3', 'classic', '2023-05-27', 'Malayalam', '1', 'public', '178', 'approved'),
(2, '1', '1', 'Puthiyoru Lokam', 'uploads/songs/image/Puthiyoru Lokam.jpg', '/static/uploads/songs/Akshay7c2f28a8-4a34-4f95-82d2-25aa892eecef.mp3', 'classic', '2023-05-28', 'Malayalam', '1', 'public', '201', 'approved'),
(3, '2', '2', 'Pavizha Mazha', 'uploads/songs/image/Pavizha Mazha.jpg', '/static/uploads/songs/Akshay2f800a5c-63c5-400d-b7bf-91bb4a6c19ff.mp3', 'classic', '2023-05-27', 'malayalam', '1', 'public', '3:53', 'approved'),
(4, '2', '3', 'Kannil Kannil', 'uploads/songs/image/Kannil Kannil.jpg', '/static/uploads/songs/Akshay702a51eb-faba-4e3c-83b2-d7a9e8562458.mp3', 'classic', '2023-05-31', 'malayalam', '1', 'public', '3:52', 'rejected'),
(5, '4', '4', 'Aaro Nee Aaro', 'uploads/songs/image/Aaro Nee Aaro.jpg', '/static/uploads/songs/Anju743d1d6b-dfd5-46c7-8ccc-76316563752b.mp3', 'classic', '2023-06-04', 'Malayalam', '3', 'public', '6:20', 'approved'),
(6, '1', '4', 'Aaro Nilavay', 'uploads/songs/image/Aaro Nilavay.jpeg', '/static/uploads/songs/Anju0579792d-5c43-41c1-b311-9e597016e8cf.mp3', 'classic', '2023-06-01', 'malayalam', '3', 'public', '4:19', 'rejected'),
(7, 'null', '4', 'Aaro Nilavai', 'uploads/songs/image/Aaro Nilavai 2.jpg', '/static/uploads/songs/Anju5b7157d5-7937-43bf-b370-bf803bb4d8e8.mp3', 'classic', '2023-06-02', 'malayalam', '3', 'public', '4:19', 'approved');

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
(1, '3', 'Akshay', 'K S', 'akshay@gmail.com', '9846524187', 'uploads/Akshay3.jpg', 'active'),
(3, '5', 'Anju', 'K', 'anjuk@gmail.com', '8781243901', 'uploads/Anju5.jpg', 'active');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
