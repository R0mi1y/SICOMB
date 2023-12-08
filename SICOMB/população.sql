CREATE DATABASE `sicomb` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_police_police_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_police_police_id` FOREIGN KEY (`user_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_bullet` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activated` tinyint(1) NOT NULL,
  `amount` int(11) NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_equipment` (
  `date_register` datetime(6) NOT NULL,
  `activated` tinyint(1) NOT NULL,
  `serial_number` varchar(20) DEFAULT NULL,
  `uid` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `model_id` int(10) unsigned NOT NULL CHECK (`model_id` >= 0),
  `model_type_id` int(11) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `equipment_equipment_model_type_id_5e24e40c_fk_django_co` (`model_type_id`),
  CONSTRAINT `equipment_equipment_model_type_id_5e24e40c_fk_django_co` FOREIGN KEY (`model_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_model_accessory` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_model_armament` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_model_grenada` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `equipment_model_wearable` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activated` tinyint(1) NOT NULL,
  `model` longtext NOT NULL,
  `size` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `load_equipment_load` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL,
  `observation` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `bullet_id` bigint(20) DEFAULT NULL,
  `equipment_id` varchar(20) DEFAULT NULL,
  `load_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` (`bullet_id`),
  KEY `load_equipment_load_equipment_id_41d867d3_fk_equipment` (`equipment_id`),
  KEY `load_equipment_load_load_id_f3cd723b_fk_load_load_id` (`load_id`),
  CONSTRAINT `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` FOREIGN KEY (`bullet_id`) REFERENCES `equipment_bullet` (`id`),
  CONSTRAINT `load_equipment_load_equipment_id_41d867d3_fk_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment_equipment` (`uid`),
  CONSTRAINT `load_equipment_load_load_id_f3cd723b_fk_load_load_id` FOREIGN KEY (`load_id`) REFERENCES `load_load` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `load_load` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date_load` datetime(6) NOT NULL,
  `expected_load_return_date` datetime(6) DEFAULT NULL,
  `returned_load_date` datetime(6) DEFAULT NULL,
  `turn_type` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL,
  `adjunct_id` bigint(20) NOT NULL,
  `police_id` bigint(20) NOT NULL,
  `load_unload_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `load_load_adjunct_id_896d6c02_fk_police_police_id` (`adjunct_id`),
  KEY `load_load_police_id_99893b6d_fk_police_police_id` (`police_id`),
  KEY `load_load_load_unload_id_4661658e_fk_load_load_id` (`load_unload_id`),
  CONSTRAINT `load_load_adjunct_id_896d6c02_fk_police_police_id` FOREIGN KEY (`adjunct_id`) REFERENCES `police_police` (`id`),
  CONSTRAINT `load_load_load_unload_id_4661658e_fk_load_load_id` FOREIGN KEY (`load_unload_id`) REFERENCES `load_load` (`id`),
  CONSTRAINT `load_load_police_id_99893b6d_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `police_police` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
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
  `posto` varchar(10) NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `telefone` (`telefone`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `police_police_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `police_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `police_police_groups_police_id_group_id_64b060f7_uniq` (`police_id`,`group_id`),
  KEY `police_police_groups_group_id_aff6a325_fk_auth_group_id` (`group_id`),
  CONSTRAINT `police_police_groups_group_id_aff6a325_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `police_police_groups_police_id_e73596cf_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE `police_police_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `police_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `police_police_user_permi_police_id_permission_id_2238c6b7_uniq` (`police_id`,`permission_id`),
  KEY `police_police_user_p_permission_id_fb01c691_fk_auth_perm` (`permission_id`),
  CONSTRAINT `police_police_user_p_permission_id_fb01c691_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `police_police_user_p_police_id_744319bf_fk_police_po` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

INSERT INTO sicomb.police_police_groups (police_id,group_id) VALUES
	 (2,1);

INSERT INTO sicomb.auth_group (name) VALUES
	 ('adjunct'),
	 ('police');

INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can add log entry',1,'add_logentry'),
	 ('Can change log entry',1,'change_logentry'),
	 ('Can delete log entry',1,'delete_logentry'),
	 ('Can view log entry',1,'view_logentry'),
	 ('Can add permission',2,'add_permission'),
	 ('Can change permission',2,'change_permission'),
	 ('Can delete permission',2,'delete_permission'),
	 ('Can view permission',2,'view_permission'),
	 ('Can add group',3,'add_group'),
	 ('Can change group',3,'change_group');
INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can delete group',3,'delete_group'),
	 ('Can view group',3,'view_group'),
	 ('Can add content type',4,'add_contenttype'),
	 ('Can change content type',4,'change_contenttype'),
	 ('Can delete content type',4,'delete_contenttype'),
	 ('Can view content type',4,'view_contenttype'),
	 ('Can add session',5,'add_session'),
	 ('Can change session',5,'change_session'),
	 ('Can delete session',5,'delete_session'),
	 ('Can view session',5,'view_session');
INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can add Policial',6,'add_police'),
	 ('Can change Policial',6,'change_police'),
	 ('Can delete Policial',6,'delete_police'),
	 ('Can view Policial',6,'view_police'),
	 ('Can add bullet',7,'add_bullet'),
	 ('Can change bullet',7,'change_bullet'),
	 ('Can delete bullet',7,'delete_bullet'),
	 ('Can view bullet',7,'view_bullet'),
	 ('Can add model_accessory',8,'add_model_accessory'),
	 ('Can change model_accessory',8,'change_model_accessory');
INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can delete model_accessory',8,'delete_model_accessory'),
	 ('Can view model_accessory',8,'view_model_accessory'),
	 ('Can add model_armament',9,'add_model_armament'),
	 ('Can change model_armament',9,'change_model_armament'),
	 ('Can delete model_armament',9,'delete_model_armament'),
	 ('Can view model_armament',9,'view_model_armament'),
	 ('Can add model_grenada',10,'add_model_grenada'),
	 ('Can change model_grenada',10,'change_model_grenada'),
	 ('Can delete model_grenada',10,'delete_model_grenada'),
	 ('Can view model_grenada',10,'view_model_grenada');
INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can add model_wearable',11,'add_model_wearable'),
	 ('Can change model_wearable',11,'change_model_wearable'),
	 ('Can delete model_wearable',11,'delete_model_wearable'),
	 ('Can view model_wearable',11,'view_model_wearable'),
	 ('Can add Equipamento',12,'add_equipment'),
	 ('Can change Equipamento',12,'change_equipment'),
	 ('Can delete Equipamento',12,'delete_equipment'),
	 ('Can view Equipamento',12,'view_equipment'),
	 ('Can add load',13,'add_load'),
	 ('Can change load',13,'change_load');
INSERT INTO sicomb.auth_permission (name,content_type_id,codename) VALUES
	 ('Can delete load',13,'delete_load'),
	 ('Can view load',13,'view_load'),
	 ('Can add equipment_load',14,'add_equipment_load'),
	 ('Can change equipment_load',14,'change_equipment_load'),
	 ('Can delete equipment_load',14,'delete_equipment_load'),
	 ('Can view equipment_load',14,'view_equipment_load');

INSERT INTO sicomb.django_content_type (app_label,model) VALUES
	 ('admin','logentry'),
	 ('auth','group'),
	 ('auth','permission'),
	 ('contenttypes','contenttype'),
	 ('equipment','bullet'),
	 ('equipment','equipment'),
	 ('equipment','model_accessory'),
	 ('equipment','model_armament'),
	 ('equipment','model_grenada'),
	 ('equipment','model_wearable');
INSERT INTO sicomb.django_content_type (app_label,model) VALUES
	 ('load','equipment_load'),
	 ('load','load'),
	 ('police','police'),
	 ('sessions','session');

INSERT INTO sicomb.django_migrations (app,name,applied) VALUES
	 ('contenttypes','0001_initial','2023-10-06 22:29:22.030792'),
	 ('contenttypes','0002_remove_content_type_name','2023-10-06 22:29:22.187666'),
	 ('auth','0001_initial','2023-10-06 22:29:22.687740'),
	 ('auth','0002_alter_permission_name_max_length','2023-10-06 22:29:22.747905'),
	 ('auth','0003_alter_user_email_max_length','2023-10-06 22:29:22.762415'),
	 ('auth','0004_alter_user_username_opts','2023-10-06 22:29:22.770509'),
	 ('auth','0005_alter_user_last_login_null','2023-10-06 22:29:22.797828'),
	 ('auth','0006_require_contenttypes_0002','2023-10-06 22:29:22.813849'),
	 ('auth','0007_alter_validators_add_error_messages','2023-10-06 22:29:22.831580'),
	 ('auth','0008_alter_user_username_max_length','2023-10-06 22:29:22.847630');
INSERT INTO sicomb.django_migrations (app,name,applied) VALUES
	 ('auth','0009_alter_user_last_name_max_length','2023-10-06 22:29:22.867754'),
	 ('auth','0010_alter_group_name_max_length','2023-10-06 22:29:22.948078'),
	 ('auth','0011_update_proxy_permissions','2023-10-06 22:29:22.960470'),
	 ('auth','0012_alter_user_first_name_max_length','2023-10-06 22:29:22.979427'),
	 ('police','0001_initial','2023-10-06 22:29:23.585516'),
	 ('admin','0001_initial','2023-10-06 22:29:23.786142'),
	 ('admin','0002_logentry_remove_auto_add','2023-10-06 22:29:23.797870'),
	 ('admin','0003_logentry_add_action_flag_choices','2023-10-06 22:29:23.810799'),
	 ('equipment','0001_initial','2023-10-06 22:29:24.074223'),
	 ('load','0001_initial','2023-10-06 22:29:24.692951');
INSERT INTO sicomb.django_migrations (app,name,applied) VALUES
	 ('sessions','0001_initial','2023-10-06 22:29:24.757666'),
	 ('police','0002_police_name','2023-10-07 00:24:35.112762'),
	 ('load','0002_load_load_unload','2023-10-12 14:45:40.522911'),
	 ('police','0003_alter_police_name','2023-10-12 14:45:40.533003');

INSERT INTO sicomb.django_session (session_key,session_data,expire_date) VALUES
	 ('2ho4gdk82h1tvqzifh9tcyexfla8lj7c','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r699v:Qpf7WS9EPG30J5qM-34T38kqrYSC6dyKgwlJgvBLa_s','2023-12-07 12:50:19.723220'),
	 ('dw4se5e7un1n1nj32f4rsyivc95uihpk','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvGsl:-4NKqafmHZvybe4vTTE4ptgxEJMjJdWiUelOi3zSoMM','2023-11-07 12:51:39.984836'),
	 ('pajez12bttgv0c3hsknn0oizgaa0l65b','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvIzk:eYBLmUTFkSACDzMNQB_9lGQvjhiPjrgLncZNY4zRMOE','2023-11-07 15:07:00.510097'),
	 ('ptxkq5cs09bzxe9fccf51kkhg6cp2b66','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKl:BJ5TiKMUhiNDDNgXZbWvNevdTRiC0i1Es2SLySIaTD4','2023-10-20 22:30:11.047838'),
	 ('t2mzc5h671xgtffbl9yqu6j99038gu1o','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKk:MBT624Zu9fh9LcGTovilp7t-oRxxX5hS4-lqPgMbXjE','2023-10-20 22:30:10.217902'),
	 ('tjzn302xih6e5npv5z3sj194vbm3j6jg','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r68yv:7EXghYUCB3eV4BoJ6WMkeoUfOeUWRf4GpDJKjZeNydg','2023-12-07 12:38:57.779138'),
	 ('xh862ugeohf7ytozuf76q33wk487og0y','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qqkER:OFX3kn3mw42evVPyDtsu3KRuzlr-1IcZFwTPT5hI8cU','2023-10-26 01:11:19.681578'),
	 ('yzmiww2e9z9918ydzlmeki9boqmg3vsm','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qwNqJ:EWTvoWHy7xGzwOE92xnrvbI5FS2JnY7n-bzr711kE6g','2023-11-10 14:29:43.638501');

INSERT INTO sicomb.equipment_bullet (activated,amount,image_path,caliber,description) VALUES
	 (1,1150,'Modelos/municoes/45acp.png','.45 ACP','Munição ACP'),
	 (1,1109,'Modelos/municoes/municao-9mm.jpg','9mm','Munição 9mm');

INSERT INTO sicomb.equipment_equipment (date_register,activated,serial_number,uid,status,model_id,model_type_id) VALUES
	 ('2023-10-26 14:56:55.795986',1,'35021305412','612','CONSERTO',1,9),
	 ('2023-10-07 00:13:28.309925',1,'1234525621681','ac1','CONSERTO',1,8),
	 ('2023-10-07 00:13:55.444752',1,'61532531565','ac2','Disponível',2,8),
	 ('2023-10-07 00:14:17.024423',1,'33126516','ar1','Disponível',1,9),
	 ('2023-10-07 00:14:37.863759',1,'94861651','ar2','CONSERTO',2,9),
	 ('2023-10-07 00:16:13.769051',1,'654168415','gd1','Disponível',1,10),
	 ('2023-10-07 00:16:33.088851',1,'6452651','gd2','Disponível',2,10),
	 ('2023-10-07 00:15:04.314881',1,'65165165','wb1','Disponível',1,11),
	 ('2023-10-07 00:15:27.264505',1,'5422247857','wb2','Disponível',2,11);

INSERT INTO sicomb.equipment_model_accessory (activated,model,description,image_path) VALUES
	 (1,'Bastão','Bastão','Modelos/acessorios/bastao.jpg'),
	 (1,'Cone','Cone','Modelos/acessorios/cone.jpg');

INSERT INTO sicomb.equipment_model_armament (activated,model,caliber,description,image_path) VALUES
	 (1,'Glok G22','.22 LR','Glok G22, munição .22 LR','Modelos/armamentos/Glock_g22_GNtS5RI.jpg'),
	 (1,'Glok 9mm','9mm','Pistola Glok 9mm','Modelos/armamentos/1016504_pistola-taurus-th380-oxidada-cal-380-cth380-ox_s1_636711376069468013.jpg');

INSERT INTO sicomb.equipment_model_grenada (activated,model,image_path,description) VALUES
	 (1,'Granada de Fumaça','Modelos/granadas/Granada_de_Fumaça.jpg','Granada de Fumaça'),
	 (1,'Granada de Fogo','Modelos/granadas/granada-fogo.jpg','Granada de Fogo');

INSERT INTO sicomb.equipment_model_wearable (activated,model,`size`,description,image_path) VALUES
	 (1,'Capacete','M','Capacete','Modelos/vestiveis/capacete.jpg'),
	 (1,'Colete','M','Colete','Modelos/vestiveis/colete.jpg');

INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Devolvido',NULL,'ac1',1),
	 (1,'','Devolvido',NULL,'ar2',1),
	 (1,'','Devolvido',NULL,'wb1',1),
	 (1,'','Devolvido',NULL,'wb2',1),
	 (1,'','Devolvido',NULL,'ac2',1),
	 (1,'','Devolvido',NULL,'ar1',1),
	 (1,'','Retorno',NULL,'ac2',2),
	 (1,'','Retorno',NULL,'wb2',2),
	 (1,'','Retorno',NULL,'wb1',2),
	 (1,'','Retorno',NULL,'ar2',2);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Retorno',NULL,'ar1',2),
	 (1,'','Retorno',NULL,'ac1',2),
	 (1,'','Devolvido',NULL,'ac2',3),
	 (1,'','Devolvido',NULL,'ar1',3),
	 (1,'','Devolvido',NULL,'ac1',3),
	 (1,'','Devolvido',NULL,'ar2',3),
	 (1,'','Devolvido',NULL,'gd1',3),
	 (1,'','Devolvido',NULL,'gd2',3),
	 (1,'','Devolvido',NULL,'wb1',3),
	 (1,'','Devolvido',NULL,'wb2',3);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (2,'','Devolvido',2,NULL,3),
	 (1,'','Retorno',NULL,'ar2',4),
	 (1,'','Retorno',NULL,'ac2',4),
	 (1,'','Retorno',NULL,'wb2',4),
	 (1,'','Devolvido',2,NULL,5),
	 (1,'','Devolvido',1,NULL,5),
	 (1,'','Devolvido',NULL,'ar2',6),
	 (1,'','Devolvido',NULL,'wb2',6),
	 (23,'','Retorno',2,NULL,7),
	 (1,'','Retorno',NULL,'ac1',7);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Retorno',NULL,'ar1',7),
	 (1,'','Retorno',NULL,'gd2',7),
	 (1,'','Retorno',NULL,'wb1',7),
	 (1,'','Retorno',NULL,'gd1',7),
	 (104,'','Devolvido',2,NULL,8),
	 (1,'','Devolvido',NULL,'ac2',8),
	 (1,'','Devolvido',NULL,'ar1',8),
	 (1,'','Devolvido',NULL,'ac1',8),
	 (1,'','Devolvido',NULL,'612',8),
	 (104,'','Retorno',2,NULL,9);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Retorno',NULL,'612',9),
	 (1,'','Retorno',NULL,'ac1',9),
	 (1,'','Retorno',NULL,'ac2',9),
	 (1,'','Retorno',NULL,'ar1',9),
	 (1,'','Retorno',NULL,'ar2',10),
	 (1,'','Retorno',NULL,'wb2',10),
	 (5,'','Retorno',2,NULL,11),
	 (1,'','Devolvido',NULL,'612',13),
	 (1,'','Devolvido',NULL,'ac2',13),
	 (1,'','Devolvido',NULL,'gd1',13);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (100,'','Devolvido',2,NULL,13),
	 (100,'','Devolvido',1,NULL,13),
	 (1,'','Retorno',1,NULL,21),
	 (1,'','Retorno',NULL,'612',22),
	 (1,'','Retorno',NULL,'ac2',22),
	 (1,'','Retorno',NULL,'gd1',22),
	 (209,'','Retorno',2,NULL,22),
	 (150,'','Retorno',1,NULL,22),
	 (1,'','Devolvido',NULL,'gd1',23),
	 (1,'','Devolvido',NULL,'ar1',23);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Devolvido',NULL,'ac2',23),
	 (1,'','Devolvido',NULL,'ar2',23),
	 (1,'','Devolvido',NULL,'wb1',23),
	 (1,'eeeuu','Devolvido',NULL,'wb2',23),
	 (1,'','Devolvido',2,NULL,23),
	 (1,'','Retorno',NULL,'ac2',24),
	 (1,'','Retorno',NULL,'ar2',24),
	 (1,'','Retorno',NULL,'wb2',24),
	 (1,'','Retorno',NULL,'ar1',24),
	 (1,'','Retorno',NULL,'gd1',24);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (1,'','Retorno',NULL,'wb1',24),
	 (1,'','Retorno',2,NULL,24),
	 (50,'svdjhubdv','Devolvido',2,NULL,25),
	 (50,'','Devolvido',2,NULL,25),
	 (50,'','Retorno',2,NULL,26),
	 (50,'','Retorno',2,NULL,27),
	 (1,'','Pendente',NULL,'612',28),
	 (1,'','Pendente',NULL,'ac1',28),
	 (1,'perdido em campo','Pendente',NULL,'ar2',28),
	 (25,'Usados em campo','Pendente',2,NULL,28);
INSERT INTO sicomb.load_equipment_load (amount,observation,status,bullet_id,equipment_id,load_id) VALUES
	 (25,'','Devolvido',2,NULL,28),
	 (25,'','Retorno',2,NULL,29);

INSERT INTO sicomb.load_load (date_load,expected_load_return_date,returned_load_date,turn_type,status,adjunct_id,police_id,load_unload_id) VALUES
	 ('2023-10-07 00:34:36.732143','2023-10-07 06:34:36.730071','2023-10-12 14:35:09.925474','6H','DESCARREGADA COM ATRASO',1,2,NULL),
	 ('2023-10-12 14:35:02.050592',NULL,'2023-10-12 14:35:02.081821','descarga','descarga',1,2,1),
	 ('2023-10-12 14:49:32.871118','2023-10-12 20:49:32.869595','2023-10-26 14:37:23.105328','6H','DESCARREGADA COM ATRASO',1,2,NULL),
	 ('2023-10-12 14:50:10.778163',NULL,'2023-10-12 14:50:10.792432','descarga','descarga',1,2,3),
	 ('2023-10-12 15:28:59.296646','2023-10-12 21:28:59.294403','2023-10-26 17:01:29.979186','6H','DESCARREGADA COM ATRASO',1,2,NULL),
	 ('2023-10-24 15:31:22.663649','2023-10-24 21:31:22.660647','2023-10-26 15:40:27.037106','6H','DESCARREGADA COM ATRASO',1,2,NULL),
	 ('2023-10-26 14:37:18.994377',NULL,'2023-10-26 14:37:19.011945','descarga','descarga',1,2,3),
	 ('2023-10-26 15:37:18.103738','2023-10-26 21:37:18.097887','2023-10-26 15:39:21.927302','6H','DESCARREGADA',1,2,NULL),
	 ('2023-10-26 15:39:17.518599',NULL,'2023-10-26 15:39:17.527111','descarga','descarga',1,2,8),
	 ('2023-10-26 15:40:21.698658',NULL,'2023-10-26 15:40:21.703734','descarga','descarga',1,2,6);
INSERT INTO sicomb.load_load (date_load,expected_load_return_date,returned_load_date,turn_type,status,adjunct_id,police_id,load_unload_id) VALUES
	 ('2023-10-26 16:29:50.845224',NULL,'2023-10-26 16:29:50.853085','descarga','descarga',1,2,5),
	 ('2023-10-26 16:30:23.929747',NULL,'2023-10-26 16:30:23.937209','descarga','descarga',1,2,5),
	 ('2023-10-26 16:31:13.139698','2023-10-27 16:31:13.135826','2023-10-26 17:18:45.560578','24H','DESCARREGADA',1,2,NULL),
	 ('2023-10-26 16:34:03.139916',NULL,'2023-10-26 16:34:03.149423','descarga','descarga',1,2,5),
	 ('2023-10-26 16:35:59.215997',NULL,'2023-10-26 16:35:59.228237','descarga','descarga',1,2,5),
	 ('2023-10-26 16:45:16.603200',NULL,'2023-10-26 16:45:16.613994','descarga','descarga',1,2,5),
	 ('2023-10-26 16:47:09.961924',NULL,'2023-10-26 16:47:09.966626','descarga','descarga',1,2,5),
	 ('2023-10-26 16:49:01.159206',NULL,'2023-10-26 16:49:01.165208','descarga','descarga',1,2,5),
	 ('2023-10-26 16:49:54.453697',NULL,'2023-10-26 16:49:54.458932','descarga','descarga',1,2,5),
	 ('2023-10-26 16:50:50.202967',NULL,'2023-10-26 16:50:50.219385','descarga','descarga',1,2,5);
INSERT INTO sicomb.load_load (date_load,expected_load_return_date,returned_load_date,turn_type,status,adjunct_id,police_id,load_unload_id) VALUES
	 ('2023-10-26 17:01:24.352591',NULL,'2023-10-26 17:01:24.365819','descarga','descarga',1,2,5),
	 ('2023-10-26 17:18:41.755334',NULL,'2023-10-26 17:18:41.760622','descarga','descarga',1,2,13),
	 ('2023-10-26 21:30:01.328455','2023-10-27 03:30:01.325913','2023-10-26 23:45:15.920010','6H','DESCARREGADA',1,2,NULL),
	 ('2023-10-26 23:45:12.336925',NULL,'2023-10-26 23:45:12.350449','descarga','descarga',1,2,23),
	 ('2023-10-26 23:45:51.663572','2023-10-27 11:45:51.660463','2023-11-23 14:10:49.820218','12H','DESCARREGADA COM ATRASO',1,2,NULL),
	 ('2023-10-26 23:53:37.997485',NULL,'2023-10-26 23:53:38.003422','descarga','descarga',1,2,25),
	 ('2023-11-23 14:10:42.038069',NULL,'2023-11-23 14:10:42.045218','descarga','descarga',1,2,25),
	 ('2023-11-23 14:18:23.828872',NULL,NULL,'CONSERTO','PARCIALMENTE DESCARREGADA',1,2,NULL),
	 ('2023-11-23 16:26:56.118601',NULL,'2023-11-23 16:26:56.135010','descarga','descarga',1,2,28);

INSERT INTO sicomb.police_police (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined,activated,matricula,telefone,lotacao,posto,image_path,tipo,name) VALUES
	 ('pbkdf2_sha256$600000$fiybkJKRz68peKGpKEsJFJ$LizSOOPQSePooPiZNyon1t4eh3zlO2fq55IkWRI4czg=','2023-11-23 12:50:19.714865',1,'admin','','','',1,1,'2023-10-06 22:29:56.561030',1,'','','','','','Police','Ediel'),
	 ('pbkdf2_sha256$600000$LwqKCEhT0c7Os7ZR2bmMYB$hYtR3DD1F2fWH6CWzRTXMLUWQlUKo84Z4VczHbshOIY=','2023-10-12 01:10:51.392855',0,'','','','edielromily7@gmail.com',0,1,'2023-10-07 00:27:39.840923',1,'ediel123','+5577991083244','GBI','Policial','policiais/2023-10-06/ediel_dStLppJ.jpg','Police','ediel romily');
