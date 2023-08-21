-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.28-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.4.0.6659
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for approval_system_db
CREATE DATABASE IF NOT EXISTS `approval_system_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `approval_system_db`;

-- Dumping structure for table approval_system_db.buying_requests
CREATE TABLE IF NOT EXISTS `buying_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `process_step_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `approve_before` datetime DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `is_done` tinyint(1) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  KEY `process_step_id` (`process_step_id`),
  KEY `ix_buying_requests_id` (`id`),
  CONSTRAINT `buying_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `buying_requests_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
  CONSTRAINT `buying_requests_ibfk_3` FOREIGN KEY (`process_step_id`) REFERENCES `process_steps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.buying_requests: ~14 rows (approximately)
DELETE FROM `buying_requests`;
INSERT INTO `buying_requests` (`id`, `user_id`, `department_id`, `process_step_id`, `title`, `description`, `approve_before`, `place`, `created_at`, `updated_at`, `status`, `is_done`, `is_deleted`) VALUES
	(6, 3, 1, 6, 'string', 'string', '2023-08-10 06:49:36', 'string', '2023-08-09 00:09:09', '2023-08-09 00:38:04', 'TBP đã từ chối', 1, 0),
	(7, 3, 1, 8, 'string', 'string', '2023-08-10 06:49:36', 'string', '2023-08-09 00:09:28', '2023-08-09 20:41:43', 'Phòng Kỹ thuật đã từ chối', 1, 0),
	(8, 3, 1, 7, 'string', 'string', '2023-08-10 06:49:36', 'string', '2023-08-09 00:09:28', '2023-08-09 01:30:06', 'TBP đã phê duyệt', 0, 0),
	(9, 3, 1, 10, 'string', 'string', '2023-08-10 06:49:36', 'string', '2023-08-09 00:09:28', '2023-08-09 00:53:47', 'Đã hoàn thành', 1, 0),
	(10, 3, 8, 6, 'string', 'string', '2023-08-10 12:00:00', 'string', '2023-08-09 00:09:28', '2023-08-09 20:41:43', 'Đang chờ xử lý', 0, 0),
	(11, 3, 1, 6, 'string', 'string', '2023-08-09 06:49:36', 'string', '2023-08-09 00:09:28', NULL, 'Đang chờ xử lý', 0, 0),
	(12, 3, 1, 6, 'string', 'string', '2023-08-09 06:49:36', 'string', '2023-08-09 00:09:28', '2023-08-09 00:53:47', 'TBP đã từ chối', 1, 0),
	(13, 3, 6, 9, 'string', 'string', '2023-08-12 07:00:00', 'string', '2023-08-09 01:37:03', '2023-08-14 23:34:45', 'HCNS đã từ chối', 1, 0),
	(14, 3, 4, 6, 'string', 'string', '2023-08-09 06:49:36', 'string', '2023-08-09 01:37:17', NULL, 'Đang chờ xử lý', 0, 0),
	(15, 3, 4, 6, 'string', 'string', '2023-08-09 06:49:36', 'string', '2023-08-09 01:37:28', NULL, 'Đang chờ xử lý', 0, 0),
	(16, 3, 5, 7, 'acb', 'abc', '2023-08-12 10:00:00', 'hanoi', '2023-08-09 18:35:10', '2023-08-09 18:41:51', 'TBP đã phê duyệt', 0, 0),
	(17, 3, 5, 6, 'acb', 'abc', '2023-08-12 10:00:00', 'hanoi', '2023-08-09 18:35:10', '2023-08-09 18:43:41', 'TBP đã từ chối', 1, 0),
	(18, 3, 5, 10, 'tieu de', 'mo ta', '2023-08-16 10:00:00', 'hanoi', '2023-08-14 18:17:41', '2023-08-14 18:17:41', 'Đã hoàn thành', 1, 0),
	(19, 3, 2, 6, '123', '123', '2023-08-17 10:00:00', '123', '2023-08-14 19:30:45', NULL, 'Đang chờ xử lý', 0, 0),
	(20, 3, 4, 6, '234', '234', '2023-08-16 16:00:00', 'hai phong', '2023-08-14 19:38:58', NULL, 'Đang chờ xử lý', 0, 0),
	(21, 3, 5, 6, 'cbab', 'cba', '2023-08-16 16:00:00', 'hai phong', '2023-08-14 19:40:09', '2023-08-15 19:15:52', 'Đang chờ xử lý', 0, 0);

-- Dumping structure for table approval_system_db.cars
CREATE TABLE IF NOT EXISTS `cars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `seats` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_cars_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.cars: ~4 rows (approximately)
DELETE FROM `cars`;
INSERT INTO `cars` (`id`, `name`, `seats`, `is_deleted`) VALUES
	(1, 'Xe 1', 7, 0),
	(2, 'Xe 2', 16, 0),
	(3, 'Xe 3', 25, 0),
	(4, 'Xe 4', 50, 0);

-- Dumping structure for table approval_system_db.car_bookings
CREATE TABLE IF NOT EXISTS `car_bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `car_id` int(11) DEFAULT NULL,
  `process_step_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `origin` varchar(255) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `distance` float DEFAULT NULL,
  `number_of_people` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `is_done` tinyint(1) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `car_id` (`car_id`),
  KEY `process_step_id` (`process_step_id`),
  KEY `ix_car_bookings_id` (`id`),
  CONSTRAINT `car_bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `car_bookings_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`),
  CONSTRAINT `car_bookings_ibfk_3` FOREIGN KEY (`process_step_id`) REFERENCES `process_steps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.car_bookings: ~2 rows (approximately)
DELETE FROM `car_bookings`;
INSERT INTO `car_bookings` (`id`, `user_id`, `car_id`, `process_step_id`, `title`, `place`, `start_time`, `end_time`, `origin`, `destination`, `distance`, `number_of_people`, `created_at`, `updated_at`, `status`, `is_done`, `is_deleted`) VALUES
	(1, 3, 2, 22, 'dat xe 1', 'ha noi', '2023-08-16 09:00:00', '2023-08-16 15:00:00', 'hanoi', 'quangninh', 100, 12, '2023-08-14 23:34:45', '2023-08-15 02:15:11', 'Đã hoàn thành', 1, 0),
	(2, 3, 2, 22, 'dat xe 2', 'hanoi', '2023-08-16 07:00:00', '2023-08-16 12:00:00', 'hanoi', 'quangninh', 100, 10, '2023-08-15 01:52:04', '2023-08-15 02:15:11', 'Lái xe đã từ chối', 1, 0);

-- Dumping structure for table approval_system_db.departments
CREATE TABLE IF NOT EXISTS `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_departments_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.departments: ~8 rows (approximately)
DELETE FROM `departments`;
INSERT INTO `departments` (`id`, `name`, `is_deleted`) VALUES
	(1, 'Phòng Lập trình', 0),
	(2, 'Phòng Hành chính nhân sự', 0),
	(3, 'Phòng Kỹ thuật', 0),
	(4, 'Phòng Marketing', 0),
	(5, 'Phòng Kế toán', 0),
	(6, 'Phòng Kinh doanh', 0),
	(7, 'Phòng BOD', 0),
	(8, 'Phòng Sản phẩm', 0);

-- Dumping structure for table approval_system_db.processes
CREATE TABLE IF NOT EXISTS `processes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_processes_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.processes: ~2 rows (approximately)
DELETE FROM `processes`;
INSERT INTO `processes` (`id`, `name`, `is_deleted`) VALUES
	(1, 'Quy trình đặt phòng', 0),
	(2, 'Quy trình đặt xe', 0),
	(3, 'Quy trình mua hàng', 0);

-- Dumping structure for table approval_system_db.process_steps
CREATE TABLE IF NOT EXISTS `process_steps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `process_id` int(11) DEFAULT NULL,
  `step` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `approve_status` varchar(255) DEFAULT NULL,
  `deny_status` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `process_id_step` (`process_id`,`step`),
  KEY `ix_process_steps_id` (`id`),
  CONSTRAINT `process_steps_ibfk_1` FOREIGN KEY (`process_id`) REFERENCES `processes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.process_steps: ~10 rows (approximately)
DELETE FROM `process_steps`;
INSERT INTO `process_steps` (`id`, `process_id`, `step`, `name`, `role`, `approve_status`, `deny_status`, `is_deleted`) VALUES
	(6, 3, 1, 'TBP phê duyệt', 'manager', 'TBP đã phê duyệt', 'TBP đã từ chối', 0),
	(7, 3, 2, 'HCNS', 'hr', 'HCNS đã phê duyệt', 'HCNS đã từ chối', 0),
	(8, 3, 3, 'Phòng Kỹ thuật check', 'tech', 'Phòng Kỹ thuật đã phê duyệt', 'Phòng Kỹ thuật đã từ chối', 0),
	(9, 3, 4, 'HCNS xử lý thông tin', 'hr', 'Đang mua hàng', 'HCNS đã từ chối', 0),
	(10, 3, 5, 'Mua hàng', 'hr', 'Đã hoàn thành', 'HCNS đã từ chối', 0),
	(19, 1, 2, 'HCNS', 'hr', 'Đã hoàn thành', 'HCNS đã từ chối', 0),
	(21, 1, 1, 'TBP', 'manager', 'TBP đã phê duyệt', 'TBP đã từ chối', 0),
	(22, 2, 2, 'Lái xe', 'driver', 'Đã hoàn thành', 'Lái xe đã từ chối', 0),
	(23, 2, 1, 'TBP', 'manager', 'TBP đã phê duyệt', 'TBP đã từ chối', 0);

-- Dumping structure for table approval_system_db.rooms
CREATE TABLE IF NOT EXISTS `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_rooms_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.rooms: ~4 rows (approximately)
DELETE FROM `rooms`;
INSERT INTO `rooms` (`id`, `name`, `capacity`, `is_deleted`) VALUES
	(11, '203', 40, 0),
	(12, '101', 30, 0),
	(13, '102', 50, 0),
	(21, '103', 20, 0),
	(22, '201', 30, 0);

-- Dumping structure for table approval_system_db.room_bookings
CREATE TABLE IF NOT EXISTS `room_bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `process_step_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `participation` int(11) DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `is_done` tinyint(1) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `room_id` (`room_id`),
  KEY `process_step_id` (`process_step_id`),
  KEY `ix_room_bookings_id` (`id`),
  CONSTRAINT `room_bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `room_bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`),
  CONSTRAINT `room_bookings_ibfk_3` FOREIGN KEY (`process_step_id`) REFERENCES `process_steps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.room_bookings: ~5 rows (approximately)
DELETE FROM `room_bookings`;
INSERT INTO `room_bookings` (`id`, `user_id`, `room_id`, `process_step_id`, `title`, `place`, `participation`, `booking_date`, `start_time`, `end_time`, `created_at`, `updated_at`, `status`, `is_done`, `is_deleted`) VALUES
	(3, 3, 12, 21, 'string', 'string', 10, '2023-08-15', '17:09:40', '18:09:40', '2023-08-14 20:13:53', '2023-08-14 20:22:55', 'TBP đã từ chối', 1, 0),
	(4, 3, 12, 19, 'string', 'string', 10, '2023-08-15', '12:09:40', '13:09:40', '2023-08-14 20:13:53', '2023-08-14 21:17:40', 'Đã hoàn thành', 1, 0),
	(5, 3, 13, 19, 'string', 'string', 10, '2023-08-16', '08:09:40', '09:09:40', '2023-08-14 20:13:53', '2023-08-14 23:34:45', 'Đã hoàn thành', 1, 0),
	(6, 3, 12, 21, 'dat phong 1', 'ha noi', 20, '2023-08-15', '14:00:00', '15:00:00', '2023-08-14 23:34:45', '2023-08-15 01:19:24', 'Đang chờ xử lý', 0, 0),
	(7, 3, 13, 19, 'dat phong 2', 'dia diem 1', 30, '2023-08-16', '08:00:00', '09:00:00', '2023-08-15 01:30:43', '2023-08-15 01:34:31', 'TBP đã phê duyệt', 0, 0);

-- Dumping structure for table approval_system_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table approval_system_db.users: ~4 rows (approximately)
DELETE FROM `users`;
INSERT INTO `users` (`id`, `username`, `email`, `password`, `name`, `role`, `created_at`, `is_deleted`) VALUES
	(3, 'hung', 'hung', '$2b$12$FazOxemQRXMDdj8RX.zST.JrA85a3xYLXdwygGrWQWSRSSldA3HO6', 'hung', 'user', '2023-07-11 20:16:31', 0),
	(4, 'manager1', 'manager', '$2b$12$Yzqgh74J6xvaF78XRZsDrOFaRtQ4EZZ/glFdgzOdmjbJcZpZ6jrI2', 'manager', 'manager', '2023-07-12 00:00:27', 0),
	(5, 'hr1', 'hr', '$2b$12$MVDy.i4EBV4/V8bI.ArShOq1hqtSdhD3XJyD5sV1Qz13rJrw2lItW', 'hr', 'hr', '2023-07-12 00:07:24', 0),
	(6, 'hr2', 'hr@example.com', '$2b$12$qduX612Re49z3/yiAJ5YSOBkPOpiXjnntp6a6XMX60YfBuOGbYf/K', 'hr2', 'hr', '2023-07-18 00:22:34', 0),
	(7, 'driver1', 'driver1@example.com', '$2b$12$xzrLQ/9qW7cnq/oAm8SkfeftfuvN5dA0TjCeGAoeWgIL11Z63b6Lu', 'driver1', 'driver', '2023-07-25 23:43:26', 0),
	(8, 'tech', 'tech@example.com', '$2b$12$QpHmPCNowsforTNGxCQq8ebXaOTwJQxr36CkJ4xdW63hb6y5aMb66', 'tech', 'tech', '2023-08-01 00:45:22', 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
