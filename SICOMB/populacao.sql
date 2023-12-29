-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 29/12/2023 às 23:03
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `sicomb`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(3, 'adjunct'),
(4, 'police');

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(113, 'Can add content type', 18, 'add_contenttype'),
(114, 'Can change content type', 18, 'change_contenttype'),
(115, 'Can delete content type', 18, 'delete_contenttype'),
(116, 'Can view content type', 18, 'view_contenttype'),
(117, 'Can add log entry', 15, 'add_logentry'),
(118, 'Can change log entry', 15, 'change_logentry'),
(119, 'Can delete log entry', 15, 'delete_logentry'),
(120, 'Can view log entry', 15, 'view_logentry'),
(121, 'Can add permission', 17, 'add_permission'),
(122, 'Can change permission', 17, 'change_permission'),
(123, 'Can delete permission', 17, 'delete_permission'),
(124, 'Can view permission', 17, 'view_permission'),
(125, 'Can add group', 16, 'add_group'),
(126, 'Can change group', 16, 'change_group'),
(127, 'Can delete group', 16, 'delete_group'),
(128, 'Can view group', 16, 'view_group'),
(129, 'Can add session', 28, 'add_session'),
(130, 'Can change session', 28, 'change_session'),
(131, 'Can delete session', 28, 'delete_session'),
(132, 'Can view session', 28, 'view_session'),
(133, 'Can add Policial', 27, 'add_police'),
(134, 'Can change Policial', 27, 'change_police'),
(135, 'Can delete Policial', 27, 'delete_police'),
(136, 'Can view Policial', 27, 'view_police'),
(137, 'Can add bullet', 19, 'add_bullet'),
(138, 'Can change bullet', 19, 'change_bullet'),
(139, 'Can delete bullet', 19, 'delete_bullet'),
(140, 'Can view bullet', 19, 'view_bullet'),
(141, 'Can add model_accessory', 21, 'add_model_accessory'),
(142, 'Can change model_accessory', 21, 'change_model_accessory'),
(143, 'Can delete model_accessory', 21, 'delete_model_accessory'),
(144, 'Can view model_accessory', 21, 'view_model_accessory'),
(145, 'Can add model_armament', 22, 'add_model_armament'),
(146, 'Can change model_armament', 22, 'change_model_armament'),
(147, 'Can delete model_armament', 22, 'delete_model_armament'),
(148, 'Can view model_armament', 22, 'view_model_armament'),
(149, 'Can add model_grenada', 23, 'add_model_grenada'),
(150, 'Can change model_grenada', 23, 'change_model_grenada'),
(151, 'Can delete model_grenada', 23, 'delete_model_grenada'),
(152, 'Can view model_grenada', 23, 'view_model_grenada'),
(153, 'Can add model_wearable', 24, 'add_model_wearable'),
(154, 'Can change model_wearable', 24, 'change_model_wearable'),
(155, 'Can delete model_wearable', 24, 'delete_model_wearable'),
(156, 'Can view model_wearable', 24, 'view_model_wearable'),
(157, 'Can add Equipamento', 20, 'add_equipment'),
(158, 'Can change Equipamento', 20, 'change_equipment'),
(159, 'Can delete Equipamento', 20, 'delete_equipment'),
(160, 'Can view Equipamento', 20, 'view_equipment'),
(161, 'Can add load', 26, 'add_load'),
(162, 'Can change load', 26, 'change_load'),
(163, 'Can delete load', 26, 'delete_load'),
(164, 'Can view load', 26, 'view_load'),
(165, 'Can add equipment_load', 25, 'add_equipment_load'),
(166, 'Can change equipment_load', 25, 'change_equipment_load'),
(167, 'Can delete equipment_load', 25, 'delete_equipment_load'),
(168, 'Can view equipment_load', 25, 'view_equipment_load'),
(169, 'Can add report', 43, 'add_report'),
(170, 'Can change report', 43, 'change_report'),
(171, 'Can delete report', 43, 'delete_report'),
(172, 'Can view report', 43, 'view_report'),
(173, 'Can add report_field', 44, 'add_report_field'),
(174, 'Can change report_field', 44, 'change_report_field'),
(175, 'Can delete report_field', 44, 'delete_report_field'),
(176, 'Can view report_field', 44, 'view_report_field');

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(15, 'admin', 'logentry'),
(16, 'auth', 'group'),
(17, 'auth', 'permission'),
(18, 'contenttypes', 'contenttype'),
(19, 'equipment', 'bullet'),
(20, 'equipment', 'equipment'),
(21, 'equipment', 'model_accessory'),
(22, 'equipment', 'model_armament'),
(23, 'equipment', 'model_grenada'),
(24, 'equipment', 'model_wearable'),
(25, 'load', 'equipment_load'),
(26, 'load', 'load'),
(27, 'police', 'police'),
(43, 'report', 'report'),
(44, 'report', 'report_field'),
(28, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(25, 'contenttypes', '0001_initial', '2023-10-06 22:29:22.030792'),
(26, 'contenttypes', '0002_remove_content_type_name', '2023-10-06 22:29:22.187666'),
(27, 'auth', '0001_initial', '2023-10-06 22:29:22.687740'),
(28, 'auth', '0002_alter_permission_name_max_length', '2023-10-06 22:29:22.747905'),
(29, 'auth', '0003_alter_user_email_max_length', '2023-10-06 22:29:22.762415'),
(30, 'auth', '0004_alter_user_username_opts', '2023-10-06 22:29:22.770509'),
(31, 'auth', '0005_alter_user_last_login_null', '2023-10-06 22:29:22.797828'),
(32, 'auth', '0006_require_contenttypes_0002', '2023-10-06 22:29:22.813849'),
(33, 'auth', '0007_alter_validators_add_error_messages', '2023-10-06 22:29:22.831580'),
(34, 'auth', '0008_alter_user_username_max_length', '2023-10-06 22:29:22.847630'),
(35, 'auth', '0009_alter_user_last_name_max_length', '2023-10-06 22:29:22.867754'),
(36, 'auth', '0010_alter_group_name_max_length', '2023-10-06 22:29:22.948078'),
(37, 'auth', '0011_update_proxy_permissions', '2023-10-06 22:29:22.960470'),
(38, 'auth', '0012_alter_user_first_name_max_length', '2023-10-06 22:29:22.979427'),
(39, 'police', '0001_initial', '2023-10-06 22:29:23.585516'),
(40, 'admin', '0001_initial', '2023-10-06 22:29:23.786142'),
(41, 'admin', '0002_logentry_remove_auto_add', '2023-10-06 22:29:23.797870'),
(42, 'admin', '0003_logentry_add_action_flag_choices', '2023-10-06 22:29:23.810799'),
(43, 'equipment', '0001_initial', '2023-10-06 22:29:24.074223'),
(44, 'load', '0001_initial', '2023-10-06 22:29:24.692951'),
(45, 'sessions', '0001_initial', '2023-10-06 22:29:24.757666'),
(46, 'police', '0002_police_name', '2023-10-07 00:24:35.112762'),
(47, 'load', '0002_load_load_unload', '2023-10-12 14:45:40.522911'),
(48, 'police', '0003_alter_police_name', '2023-10-12 14:45:40.533003'),
(49, 'contenttypes', '0001_initial', '2023-10-06 22:29:22.030792'),
(50, 'contenttypes', '0002_remove_content_type_name', '2023-10-06 22:29:22.187666'),
(51, 'auth', '0001_initial', '2023-10-06 22:29:22.687740'),
(52, 'auth', '0002_alter_permission_name_max_length', '2023-10-06 22:29:22.747905'),
(53, 'auth', '0003_alter_user_email_max_length', '2023-10-06 22:29:22.762415'),
(54, 'auth', '0004_alter_user_username_opts', '2023-10-06 22:29:22.770509'),
(55, 'auth', '0005_alter_user_last_login_null', '2023-10-06 22:29:22.797828'),
(56, 'auth', '0006_require_contenttypes_0002', '2023-10-06 22:29:22.813849'),
(57, 'auth', '0007_alter_validators_add_error_messages', '2023-10-06 22:29:22.831580'),
(58, 'auth', '0008_alter_user_username_max_length', '2023-10-06 22:29:22.847630'),
(59, 'auth', '0009_alter_user_last_name_max_length', '2023-10-06 22:29:22.867754'),
(60, 'auth', '0010_alter_group_name_max_length', '2023-10-06 22:29:22.948078'),
(61, 'auth', '0011_update_proxy_permissions', '2023-10-06 22:29:22.960470'),
(62, 'auth', '0012_alter_user_first_name_max_length', '2023-10-06 22:29:22.979427'),
(63, 'police', '0001_initial', '2023-10-06 22:29:23.585516'),
(64, 'admin', '0001_initial', '2023-10-06 22:29:23.786142'),
(65, 'admin', '0002_logentry_remove_auto_add', '2023-10-06 22:29:23.797870'),
(66, 'admin', '0003_logentry_add_action_flag_choices', '2023-10-06 22:29:23.810799'),
(67, 'equipment', '0001_initial', '2023-10-06 22:29:24.074223'),
(68, 'load', '0001_initial', '2023-10-06 22:29:24.692951'),
(69, 'sessions', '0001_initial', '2023-10-06 22:29:24.757666'),
(70, 'police', '0002_police_name', '2023-10-07 00:24:35.112762'),
(71, 'load', '0002_load_load_unload', '2023-10-12 14:45:40.522911'),
(72, 'police', '0003_alter_police_name', '2023-10-12 14:45:40.533003'),
(73, 'equipment', '0002_bullet_activator_equipment_activator_and_more', '2023-12-29 21:43:27.381064'),
(74, 'equipment', '0003_alter_equipment_uid', '2023-12-29 21:43:27.831124'),
(75, 'equipment', '0004_alter_equipment_serial_number', '2023-12-29 21:43:27.863410'),
(76, 'load', '0003_alter_equipment_load_status_alter_load_status', '2023-12-29 21:43:27.884899'),
(77, 'police', '0004_police_activator', '2023-12-29 21:43:28.035725'),
(78, 'police', '0005_alter_police_tipo', '2023-12-29 21:43:28.051409'),
(79, 'police', '0006_police_fingerprint', '2023-12-29 21:43:28.073925'),
(80, 'police', '0007_alter_police_posto', '2023-12-29 21:43:28.101589'),
(81, 'report', '0001_initial', '2023-12-29 21:43:28.233135'),
(82, 'report', '0002_report_date_creation', '2023-12-29 21:43:28.297755'),
(83, 'report', '0003_alter_report_date_creation_alter_report_title', '2023-12-29 22:02:58.676994');

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2ho4gdk82h1tvqzifh9tcyexfla8lj7c', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r699v:Qpf7WS9EPG30J5qM-34T38kqrYSC6dyKgwlJgvBLa_s', '2023-12-07 12:50:19.723220'),
('dw4se5e7un1n1nj32f4rsyivc95uihpk', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvGsl:-4NKqafmHZvybe4vTTE4ptgxEJMjJdWiUelOi3zSoMM', '2023-11-07 12:51:39.984836'),
('pajez12bttgv0c3hsknn0oizgaa0l65b', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvIzk:eYBLmUTFkSACDzMNQB_9lGQvjhiPjrgLncZNY4zRMOE', '2023-11-07 15:07:00.510097'),
('ptxkq5cs09bzxe9fccf51kkhg6cp2b66', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKl:BJ5TiKMUhiNDDNgXZbWvNevdTRiC0i1Es2SLySIaTD4', '2023-10-20 22:30:11.047838'),
('t2mzc5h671xgtffbl9yqu6j99038gu1o', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKk:MBT624Zu9fh9LcGTovilp7t-oRxxX5hS4-lqPgMbXjE', '2023-10-20 22:30:10.217902'),
('tjzn302xih6e5npv5z3sj194vbm3j6jg', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r68yv:7EXghYUCB3eV4BoJ6WMkeoUfOeUWRf4GpDJKjZeNydg', '2023-12-07 12:38:57.779138'),
('xh862ugeohf7ytozuf76q33wk487og0y', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qqkER:OFX3kn3mw42evVPyDtsu3KRuzlr-1IcZFwTPT5hI8cU', '2023-10-26 01:11:19.681578'),
('yzmiww2e9z9918ydzlmeki9boqmg3vsm', '.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qwNqJ:EWTvoWHy7xGzwOE92xnrvbI5FS2JnY7n-bzr711kE6g', '2023-11-10 14:29:43.638501');

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_bullet`
--

CREATE TABLE `equipment_bullet` (
  `id` bigint(20) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `amount` int(11) NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `equipment_bullet`
--

INSERT INTO `equipment_bullet` (`id`, `activated`, `amount`, `image_path`, `caliber`, `description`, `activator_id`) VALUES
(3, 1, 1150, 'Modelos/municoes/45acp.png', '.45 ACP', 'Munição ACP', NULL),
(4, 1, 1109, 'Modelos/municoes/municao-9mm.jpg', '9mm', 'Munição 9mm', NULL),
(5, 1, 1150, 'Modelos/municoes/45acp.png', '.45 ACP', 'Munição ACP', NULL),
(6, 1, 1109, 'Modelos/municoes/municao-9mm.jpg', '9mm', 'Munição 9mm', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_equipment`
--

CREATE TABLE `equipment_equipment` (
  `date_register` datetime(6) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `serial_number` varchar(200) DEFAULT NULL,
  `uid` varchar(200) NOT NULL,
  `status` varchar(20) NOT NULL,
  `model_id` int(10) UNSIGNED NOT NULL CHECK (`model_id` >= 0),
  `model_type_id` int(11) NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_model_accessory`
--

CREATE TABLE `equipment_model_accessory` (
  `id` bigint(20) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `equipment_model_accessory`
--

INSERT INTO `equipment_model_accessory` (`id`, `activated`, `model`, `description`, `image_path`, `activator_id`) VALUES
(3, 1, 'Bastão', 'Bastão', 'Modelos/acessorios/bastao.jpg', NULL),
(4, 1, 'Cone', 'Cone', 'Modelos/acessorios/cone.jpg', NULL),
(5, 1, 'Bastão', 'Bastão', 'Modelos/acessorios/bastao.jpg', NULL),
(6, 1, 'Cone', 'Cone', 'Modelos/acessorios/cone.jpg', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_model_armament`
--

CREATE TABLE `equipment_model_armament` (
  `id` bigint(20) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `equipment_model_armament`
--

INSERT INTO `equipment_model_armament` (`id`, `activated`, `model`, `caliber`, `description`, `image_path`, `activator_id`) VALUES
(3, 1, 'Glok G22', '.22 LR', 'Glok G22, munição .22 LR', 'Modelos/armamentos/Glock_g22_GNtS5RI.jpg', NULL),
(4, 1, 'Glok 9mm', '9mm', 'Pistola Glok 9mm', 'Modelos/armamentos/1016504_pistola-taurus-th380-oxidada-cal-380-cth380-ox_s1_636711376069468013.jpg', NULL),
(5, 1, 'Glok G22', '.22 LR', 'Glok G22, munição .22 LR', 'Modelos/armamentos/Glock_g22_GNtS5RI.jpg', NULL),
(6, 1, 'Glok 9mm', '9mm', 'Pistola Glok 9mm', 'Modelos/armamentos/1016504_pistola-taurus-th380-oxidada-cal-380-cth380-ox_s1_636711376069468013.jpg', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_model_grenada`
--

CREATE TABLE `equipment_model_grenada` (
  `id` bigint(20) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `equipment_model_grenada`
--

INSERT INTO `equipment_model_grenada` (`id`, `activated`, `model`, `image_path`, `description`, `activator_id`) VALUES
(3, 1, 'Granada de Fumaça', 'Modelos/granadas/Granada_de_Fumaça.jpg', 'Granada de Fumaça', NULL),
(4, 1, 'Granada de Fogo', 'Modelos/granadas/granada-fogo.jpg', 'Granada de Fogo', NULL),
(5, 1, 'Granada de Fumaça', 'Modelos/granadas/Granada_de_Fumaça.jpg', 'Granada de Fumaça', NULL),
(6, 1, 'Granada de Fogo', 'Modelos/granadas/granada-fogo.jpg', 'Granada de Fogo', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `equipment_model_wearable`
--

CREATE TABLE `equipment_model_wearable` (
  `id` bigint(20) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `size` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `equipment_model_wearable`
--

INSERT INTO `equipment_model_wearable` (`id`, `activated`, `model`, `size`, `description`, `image_path`, `activator_id`) VALUES
(3, 1, 'Capacete', 'M', 'Capacete', 'Modelos/vestiveis/capacete.jpg', NULL),
(4, 1, 'Colete', 'M', 'Colete', 'Modelos/vestiveis/colete.jpg', NULL),
(5, 1, 'Capacete', 'M', 'Capacete', 'Modelos/vestiveis/capacete.jpg', NULL),
(6, 1, 'Colete', 'M', 'Colete', 'Modelos/vestiveis/colete.jpg', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `load_equipment_load`
--

CREATE TABLE `load_equipment_load` (
  `id` bigint(20) NOT NULL,
  `amount` int(11) DEFAULT NULL,
  `observation` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `bullet_id` bigint(20) DEFAULT NULL,
  `equipment_id` varchar(200) DEFAULT NULL,
  `load_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `load_load`
--

CREATE TABLE `load_load` (
  `id` bigint(20) NOT NULL,
  `date_load` datetime(6) NOT NULL,
  `expected_load_return_date` datetime(6) DEFAULT NULL,
  `returned_load_date` datetime(6) DEFAULT NULL,
  `turn_type` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL,
  `adjunct_id` bigint(20) NOT NULL,
  `police_id` bigint(20) NOT NULL,
  `load_unload_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `police_police`
--

CREATE TABLE `police_police` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `telefone` varchar(20) NOT NULL,
  `lotacao` varchar(50) NOT NULL,
  `posto` varchar(50) NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `activator_id` bigint(20) DEFAULT NULL,
  `fingerprint` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `police_police`
--

INSERT INTO `police_police` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `activated`, `matricula`, `telefone`, `lotacao`, `posto`, `image_path`, `tipo`, `name`, `activator_id`, `fingerprint`) VALUES
(3, 'pbkdf2_sha256$600000$fiybkJKRz68peKGpKEsJFJ$LizSOOPQSePooPiZNyon1t4eh3zlO2fq55IkWRI4czg=', '2023-11-23 12:50:19.714865', 1, 'admin', '', '', '', 1, 1, '2023-10-06 22:29:56.561030', 1, '', '', '', '', '', 'Police', 'Ediel', NULL, NULL),
(4, 'pbkdf2_sha256$600000$LwqKCEhT0c7Os7ZR2bmMYB$hYtR3DD1F2fWH6CWzRTXMLUWQlUKo84Z4VczHbshOIY=', '2023-10-12 01:10:51.392855', 0, '', '', '', 'edielromily7@gmail.com', 0, 1, '2023-10-07 00:27:39.840923', 1, 'ediel123', '+5577991083244', 'GBI', 'Policial', 'policiais/2023-10-06/ediel_dStLppJ.jpg', 'Police', 'ediel romily', NULL, NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `police_police_groups`
--

CREATE TABLE `police_police_groups` (
  `id` bigint(20) NOT NULL,
  `police_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `police_police_user_permissions`
--

CREATE TABLE `police_police_user_permissions` (
  `id` bigint(20) NOT NULL,
  `police_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `report_report`
--

CREATE TABLE `report_report` (
  `id` bigint(20) NOT NULL,
  `title` varchar(256) NOT NULL,
  `date_creation` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `report_report_field`
--

CREATE TABLE `report_report_field` (
  `id` bigint(20) NOT NULL,
  `field` longtext DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  `report_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Índices de tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Índices de tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Índices de tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_police_police_id` (`user_id`);

--
-- Índices de tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Índices de tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Índices de tabela `equipment_bullet`
--
ALTER TABLE `equipment_bullet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_bullet_activator_id_0ccab690_fk_police_police_id` (`activator_id`);

--
-- Índices de tabela `equipment_equipment`
--
ALTER TABLE `equipment_equipment`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `serial_number` (`serial_number`),
  ADD KEY `equipment_equipment_model_type_id_5e24e40c_fk_django_co` (`model_type_id`),
  ADD KEY `equipment_equipment_activator_id_6db463cb_fk_police_police_id` (`activator_id`);

--
-- Índices de tabela `equipment_model_accessory`
--
ALTER TABLE `equipment_model_accessory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_model_acce_activator_id_4ec27a1d_fk_police_po` (`activator_id`);

--
-- Índices de tabela `equipment_model_armament`
--
ALTER TABLE `equipment_model_armament`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_model_arma_activator_id_929159ee_fk_police_po` (`activator_id`);

--
-- Índices de tabela `equipment_model_grenada`
--
ALTER TABLE `equipment_model_grenada`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_model_gren_activator_id_117d0e77_fk_police_po` (`activator_id`);

--
-- Índices de tabela `equipment_model_wearable`
--
ALTER TABLE `equipment_model_wearable`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_model_wear_activator_id_008b8112_fk_police_po` (`activator_id`);

--
-- Índices de tabela `load_equipment_load`
--
ALTER TABLE `load_equipment_load`
  ADD PRIMARY KEY (`id`),
  ADD KEY `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` (`bullet_id`),
  ADD KEY `load_equipment_load_equipment_id_41d867d3_fk_equipment` (`equipment_id`),
  ADD KEY `load_equipment_load_load_id_f3cd723b_fk_load_load_id` (`load_id`);

--
-- Índices de tabela `load_load`
--
ALTER TABLE `load_load`
  ADD PRIMARY KEY (`id`),
  ADD KEY `load_load_adjunct_id_896d6c02_fk_police_police_id` (`adjunct_id`),
  ADD KEY `load_load_police_id_99893b6d_fk_police_police_id` (`police_id`),
  ADD KEY `load_load_load_unload_id_4661658e_fk_load_load_id` (`load_unload_id`);

--
-- Índices de tabela `police_police`
--
ALTER TABLE `police_police`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `telefone` (`telefone`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `police_police_activator_id_cc99b9cc_fk_police_police_id` (`activator_id`);

--
-- Índices de tabela `police_police_groups`
--
ALTER TABLE `police_police_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `police_police_groups_police_id_group_id_64b060f7_uniq` (`police_id`,`group_id`),
  ADD KEY `police_police_groups_group_id_aff6a325_fk_auth_group_id` (`group_id`);

--
-- Índices de tabela `police_police_user_permissions`
--
ALTER TABLE `police_police_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `police_police_user_permi_police_id_permission_id_2238c6b7_uniq` (`police_id`,`permission_id`),
  ADD KEY `police_police_user_p_permission_id_fb01c691_fk_auth_perm` (`permission_id`);

--
-- Índices de tabela `report_report`
--
ALTER TABLE `report_report`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `report_report_field`
--
ALTER TABLE `report_report_field`
  ADD PRIMARY KEY (`id`),
  ADD KEY `report_report_field_report_id_c2172ca6_fk_report_report_id` (`report_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=177;

--
-- AUTO_INCREMENT de tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT de tabela `equipment_bullet`
--
ALTER TABLE `equipment_bullet`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `equipment_model_accessory`
--
ALTER TABLE `equipment_model_accessory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `equipment_model_armament`
--
ALTER TABLE `equipment_model_armament`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `equipment_model_grenada`
--
ALTER TABLE `equipment_model_grenada`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `equipment_model_wearable`
--
ALTER TABLE `equipment_model_wearable`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `load_equipment_load`
--
ALTER TABLE `load_equipment_load`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT de tabela `load_load`
--
ALTER TABLE `load_load`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT de tabela `police_police`
--
ALTER TABLE `police_police`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `police_police_groups`
--
ALTER TABLE `police_police_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `police_police_user_permissions`
--
ALTER TABLE `police_police_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `report_report`
--
ALTER TABLE `report_report`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `report_report_field`
--
ALTER TABLE `report_report_field`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Restrições para tabelas `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Restrições para tabelas `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_police_police_id` FOREIGN KEY (`user_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `equipment_bullet`
--
ALTER TABLE `equipment_bullet`
  ADD CONSTRAINT `equipment_bullet_activator_id_0ccab690_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `equipment_equipment`
--
ALTER TABLE `equipment_equipment`
  ADD CONSTRAINT `equipment_equipment_activator_id_6db463cb_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`),
  ADD CONSTRAINT `equipment_equipment_model_type_id_5e24e40c_fk_django_co` FOREIGN KEY (`model_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Restrições para tabelas `equipment_model_accessory`
--
ALTER TABLE `equipment_model_accessory`
  ADD CONSTRAINT `equipment_model_acce_activator_id_4ec27a1d_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `equipment_model_armament`
--
ALTER TABLE `equipment_model_armament`
  ADD CONSTRAINT `equipment_model_arma_activator_id_929159ee_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `equipment_model_grenada`
--
ALTER TABLE `equipment_model_grenada`
  ADD CONSTRAINT `equipment_model_gren_activator_id_117d0e77_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `equipment_model_wearable`
--
ALTER TABLE `equipment_model_wearable`
  ADD CONSTRAINT `equipment_model_wear_activator_id_008b8112_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `load_equipment_load`
--
ALTER TABLE `load_equipment_load`
  ADD CONSTRAINT `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` FOREIGN KEY (`bullet_id`) REFERENCES `equipment_bullet` (`id`),
  ADD CONSTRAINT `load_equipment_load_equipment_id_41d867d3_fk` FOREIGN KEY (`equipment_id`) REFERENCES `equipment_equipment` (`uid`),
  ADD CONSTRAINT `load_equipment_load_load_id_f3cd723b_fk_load_load_id` FOREIGN KEY (`load_id`) REFERENCES `load_load` (`id`);

--
-- Restrições para tabelas `load_load`
--
ALTER TABLE `load_load`
  ADD CONSTRAINT `load_load_adjunct_id_896d6c02_fk_police_police_id` FOREIGN KEY (`adjunct_id`) REFERENCES `police_police` (`id`),
  ADD CONSTRAINT `load_load_load_unload_id_4661658e_fk_load_load_id` FOREIGN KEY (`load_unload_id`) REFERENCES `load_load` (`id`),
  ADD CONSTRAINT `load_load_police_id_99893b6d_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `police_police`
--
ALTER TABLE `police_police`
  ADD CONSTRAINT `police_police_activator_id_cc99b9cc_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `police_police_groups`
--
ALTER TABLE `police_police_groups`
  ADD CONSTRAINT `police_police_groups_group_id_aff6a325_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `police_police_groups_police_id_e73596cf_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `police_police_user_permissions`
--
ALTER TABLE `police_police_user_permissions`
  ADD CONSTRAINT `police_police_user_p_permission_id_fb01c691_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `police_police_user_p_police_id_744319bf_fk_police_po` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`);

--
-- Restrições para tabelas `report_report_field`
--
ALTER TABLE `report_report_field`
  ADD CONSTRAINT `report_report_field_report_id_c2172ca6_fk_report_report_id` FOREIGN KEY (`report_id`) REFERENCES `report_report` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
