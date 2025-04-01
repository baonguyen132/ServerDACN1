-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th4 01, 2025 lúc 05:25 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `dacn1`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `images`
--

CREATE TABLE `images` (
  `id` int(11) NOT NULL,
  `path` mediumtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `id_user` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `images`
--

INSERT INTO `images` (`id`, `path`, `status`, `id_user`) VALUES
(4, 'uploads\\048204007137\\IMG_20250308_114323.jpg', '0', 15);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `type_books`
--

CREATE TABLE `type_books` (
  `id` int(11) NOT NULL,
  `name_book` varchar(100) NOT NULL,
  `type_book` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `type_books`
--

INSERT INTO `type_books` (`id`, `name_book`, `type_book`, `image`, `description`, `created_at`, `updated_at`) VALUES
(6, 'TIENG VIET LOP 1', 'Sách lớp 1', '/public/image/Tieng-Vieti-1-Tap-1-Ket-noi-tri-thuc.jpg', 'abc\nabc', '2025-03-31 15:39:52', '2025-03-31 15:39:52'),
(9, 'TIENG VIET', 'Sách lớp ', '/public/image/Tieng-Vieti-1-Tap-1-Ket-noi-tri-thuc.jpg', 'hahaa', '2025-04-01 03:10:40', '2025-04-01 03:10:40');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT 0,
  `cccd` varchar(12) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(6) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `pob` varchar(100) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `address` varchar(100) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `point` int(11) NOT NULL DEFAULT 0,
  `token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `status`, `cccd`, `dob`, `gender`, `pob`, `address`, `point`, `token`, `created_at`, `updated_at`) VALUES
(15, 'Hồ Bảo Nguyên', 'nguyenhb.22it@vku.udn.vn', 'Baonguyen-132', 5, '048204007137', '2004-02-13', 'Male', '', 'Tổ 33, Hòa Quý, Ngũ Hành Sơn, Đà Nẵng', 0, 'some_token', '2025-02-21 14:44:42', '2025-02-21 14:44:42'),
(16, 'Tôn Nữ Linh Chi', 'baonguyen182pht@gmail.com', '1234', 4, '046169006890', '1969-08-07', 'Male', '', 'Tổ 33, Hòa Quý, Ngũ Hành Sơn, Đà Nẵng', 0, 'some_token', '2025-03-11 06:54:32', '2025-03-11 06:54:32');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Chỉ mục cho bảng `type_books`
--
ALTER TABLE `type_books`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `images`
--
ALTER TABLE `images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT cho bảng `type_books`
--
ALTER TABLE `type_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
