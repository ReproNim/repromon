PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sec_user_role" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"role_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("user_id","role_id")
);
INSERT INTO sec_user_role VALUES(1,4,1);
INSERT INTO sec_user_role VALUES(2,1,2);
INSERT INTO sec_user_role VALUES(3,2,3);
INSERT INTO sec_user_role VALUES(4,3,4);
INSERT INTO sec_user_role VALUES(5,5,4);
INSERT INTO sec_user_role VALUES(6,5,2);
INSERT INTO sec_user_role VALUES(7,5,3);
INSERT INTO sec_user_role VALUES(8,6,5);
INSERT INTO sec_user_role VALUES(9,1,1);
INSERT INTO sec_user_role VALUES(10,5,5);
CREATE TABLE IF NOT EXISTS "message_category" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	VARCHAR(45),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO message_category VALUES(1,'Feedback');
CREATE TABLE IF NOT EXISTS "data_provider" (
	"id"	INTEGER NOT NULL UNIQUE,
	"provider"	VARCHAR(15) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO data_provider VALUES(1,'ReproIn');
INSERT INTO data_provider VALUES(2,'ReproStim');
INSERT INTO data_provider VALUES(3,'ReproEvents');
INSERT INTO data_provider VALUES(4,'PACS');
INSERT INTO data_provider VALUES(5,'Noisseur');
INSERT INTO data_provider VALUES(6,'DICOM/QA');
INSERT INTO data_provider VALUES(7,'MRI');
CREATE TABLE IF NOT EXISTS "study_status" (
	"id"	INTEGER NOT NULL UNIQUE,
	"status"	VARCHAR(45),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO study_status VALUES(100,'New');
INSERT INTO study_status VALUES(101,'Collecting MRI Data');
INSERT INTO study_status VALUES(190,'Completed');
INSERT INTO study_status VALUES(191,'Failed');
INSERT INTO study_status VALUES(200,'Entering Participant Data');
INSERT INTO study_status VALUES(300,'Designing Sequences');
CREATE TABLE IF NOT EXISTS "todo_study_session" (
	"id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "todo_study_screen" (
	"id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "message_level" (
	"id"	INTEGER NOT NULL UNIQUE,
	"level"	VARCHAR(8),
	PRIMARY KEY("id")
);
INSERT INTO message_level VALUES(1,'INFO');
INSERT INTO message_level VALUES(2,'WARNING');
INSERT INTO message_level VALUES(3,'ERROR');
CREATE TABLE IF NOT EXISTS "device" (
	"id"	INTEGER NOT NULL UNIQUE,
	"kind"	VARCHAR(15),
	"description"	VARCHAR(128),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO device VALUES(1,'MRI','DBIC 3T Siemens Prisma MRI');
CREATE TABLE IF NOT EXISTS "sec_user_device" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"device_id"	INTEGER NOT NULL,
	UNIQUE("user_id","device_id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO sec_user_device VALUES(1,1,1);
INSERT INTO sec_user_device VALUES(2,2,1);
INSERT INTO sec_user_device VALUES(3,3,1);
INSERT INTO sec_user_device VALUES(4,4,1);
INSERT INTO sec_user_device VALUES(5,5,1);
INSERT INTO sec_user_device VALUES(6,6,1);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	VARCHAR(15) NOT NULL UNIQUE,
	"is_active"	CHAR(1) DEFAULT 'N',
	"is_system"	CHAR(1) NOT NULL DEFAULT 'N',
	"first_name"	VARCHAR(45),
	"last_name"	VARCHAR(45),
	"email"	VARCHAR(128) UNIQUE,
	"phone"	VARCHAR(16),
	"description"	VARCHAR(128),
	"password"	VARCHAR(45),
	"password_changed_on"	TIMESTAMP,
	"last_login"	TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("email")
);
INSERT INTO user VALUES(1,'user1','Y','N','John','Smith','user1@repromon.com','321',NULL,'$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(2,'user2','Y','N','Dave','Cooper','user2@repromon.com','231',NULL,'$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(3,'user3','Y','N','Lucy','Nelson','user3@repromon.com','111',NULL,'$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(4,'admin','Y','N','Admin','Admin','admin@repromon.com',NULL,'Administrator','$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(5,'poweruser','Y','N','Power','User','poweruser@repromon.com',NULL,'Power user','$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(6,'noisseur','Y','Y','noisseur','noisseur','',NULL,'System con/noisseur user','$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(7,'reprostim','Y','Y','reprostim','reprostim',NULL,NULL,replace('ReproStim Screen Capture\n','\n',char(10)),'$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(8,'reproevt','Y','Y','reproevt','reproevt',NULL,NULL,replace('ReproEvents Capture\n','\n',char(10)),'$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
INSERT INTO user VALUES(9,'dicomqa','Y','Y','dicomqa','dicomqa',NULL,NULL,'DICOMS/QA','$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq',NULL,NULL);
CREATE TABLE IF NOT EXISTS "role" (
	"id"	INTEGER NOT NULL UNIQUE,
	"rolename"	VARCHAR(45) NOT NULL,
	"description"	VARCHAR(128),
	UNIQUE("rolename"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO role VALUES(1,'admin','Administrator');
INSERT INTO role VALUES(2,'data_collector','Data Collector');
INSERT INTO role VALUES(3,'mri_operator','MRI Operator');
INSERT INTO role VALUES(4,'participant','Participant');
INSERT INTO role VALUES(5,'sys_data_entry','System Data Entry');
INSERT INTO role VALUES(6,'tester','Automatic System Tester');
CREATE TABLE IF NOT EXISTS "study_data" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	VARCHAR(128),
	"device_id"	INTEGER,
	"status_id"	INTEGER,
	"start_ts"	TIMESTAMP,
	"end_ts"	TIMESTAMP,
	"info"	JSON,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO study_data VALUES(1,'Halchenko/Horea/1020_animal_mri',1,101,'2023-06-07 10:41:25',NULL,replace('{\n	"data_collector": ["user1", "poweruser"],\n	"mri_operator": ["user2"],\n	"participant": ["user3"]\n}','\n',char(10)));
CREATE TABLE IF NOT EXISTS "message_log" (
	"id"	INTEGER NOT NULL UNIQUE,
	"level_id"	INTEGER,
	"category_id"	INTEGER,
	"device_id"	INTEGER,
	"provider_id"	INTEGER,
	"study_id"	INTEGER,
	"study_name"	VARCHAR(128),
	"is_visible"	INTEGER NOT NULL DEFAULT 'Y',
	"visible_updated_on"	TIMESTAMP,
	"visible_updated_by"	VARCHAR(15),
	"description"	VARCHAR(255),
	"payload"	JSON,
	"event_on"	TIMESTAMP,
	"registered_on"	TIMESTAMP,
	"recorded_on"	TIMESTAMP,
	"recorded_by"	VARCHAR(15),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO message_log VALUES(1,1,1,1,2,NULL,NULL,'Y',NULL,NULL,'stimuli display dis-connected',NULL,'2023-06-07 10:49:31','2023-06-07 10:50:01','2023-06-07 10:50:31','reprostim');
INSERT INTO message_log VALUES(2,1,1,1,2,NULL,NULL,'Y',NULL,NULL,replace('stimuli display connected(1024x768, …)\n','\n',char(10)),NULL,'2023-06-07 10:50:22','2023-06-07 10:51:02','2023-06-07 10:51:22','reprostim');
INSERT INTO message_log VALUES(3,3,1,1,5,1,'Halchenko/Horea/1020_animal_mri','Y',NULL,NULL,replace('subject “John” is not conformant, must match [0-9]{6} regular expression. [link to screen with highlight]\n','\n',char(10)),NULL,'2023-06-07 10:51:44','2023-06-07 10:52:04','2023-06-07 10:52:44','noisseur');
INSERT INTO message_log VALUES(4,1,1,1,5,1,'Halchenko/Horea/1020_animal_mri','Y',NULL,NULL,'proceeded with compliant data on study Halchenko/Horea/1020_animal_mri',NULL,'2023-06-07 10:54:17','2023-06-07 10:55:07','2023-06-07 10:55:17','noisseur');
INSERT INTO message_log VALUES(5,1,1,1,3,NULL,NULL,'Y',NULL,NULL,'MRI trigger event received',NULL,'2023-06-07 10:55:45','2023-06-07 10:56:05','2023-06-07 10:56:45','reproevt');
INSERT INTO message_log VALUES(6,3,1,1,6,NULL,NULL,'Y',NULL,NULL,'MRI data lacks rear head coils data [link to PACS recording to review]',NULL,'2023-06-07 10:58:01','2023-06-07 10:59:00','2023-06-07 10:59:01','dicomqa');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('sec_user_role',10);
INSERT INTO sqlite_sequence VALUES('message_category',1);
INSERT INTO sqlite_sequence VALUES('data_provider',7);
INSERT INTO sqlite_sequence VALUES('study_status',300);
INSERT INTO sqlite_sequence VALUES('todo_study_session',0);
INSERT INTO sqlite_sequence VALUES('todo_study_screen',0);
INSERT INTO sqlite_sequence VALUES('device',1);
INSERT INTO sqlite_sequence VALUES('sec_user_device',6);
INSERT INTO sqlite_sequence VALUES('user',9);
INSERT INTO sqlite_sequence VALUES('role',6);
INSERT INTO sqlite_sequence VALUES('study_data',1);
INSERT INTO sqlite_sequence VALUES('message_log',6);
CREATE INDEX "idx_user_name" ON "user" (
	"username"
);
COMMIT;
