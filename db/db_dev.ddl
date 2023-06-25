CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "sec_user_role" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"role_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("user_id","role_id")
);
CREATE TABLE IF NOT EXISTS "message_payload" (
	"id"	INTEGER NOT NULL UNIQUE,
	"uid"	VARCHAR(36),
	"payload"	TEXT,
	"created_on"	TIMESTAMP,
	"created_by"	VARCHAR(15),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "message_log" (
	"id"	INTEGER NOT NULL UNIQUE,
	"level_id"	INTEGER,
	"category_id"	INTEGER,
	"provider_id"	INTEGER,
	"study_id"	INTEGER,
	"status_id"	INTEGER,
	"description"	VARCHAR(255),
	"payload_id"	INTEGER,
	"created_on"	TIMESTAMP,
	"created_by"	VARCHAR(15),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "message_category" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	VARCHAR(45),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "data_provider" (
	"id"	INTEGER NOT NULL UNIQUE,
	"provider"	VARCHAR(15) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "study_status" (
	"id"	INTEGER NOT NULL UNIQUE,
	"status"	VARCHAR(45),
	PRIMARY KEY("id" AUTOINCREMENT)
);
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
CREATE TABLE IF NOT EXISTS "device" (
	"id"	INTEGER NOT NULL UNIQUE,
	"kind"	VARCHAR(15),
	"description"	VARCHAR(128),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sec_user_device" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"device_id"	INTEGER NOT NULL,
	UNIQUE("user_id","device_id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
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
CREATE INDEX "idx_user_name" ON "user" (
	"username"
);
CREATE TABLE IF NOT EXISTS "role" (
	"id"	INTEGER NOT NULL UNIQUE,
	"rolename"	VARCHAR(45) NOT NULL,
	"description"	VARCHAR(128),
	UNIQUE("rolename"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "study_data" (
	"id"	INTEGER NOT NULL UNIQUE,
	"description"	VARCHAR(128),
	"device_id"	INTEGER,
	"status_id"	INTEGER,
	"start_ts"	TIMESTAMP,
	"end_ts"	TIMESTAMP,
	"info"	JSON,
	PRIMARY KEY("id" AUTOINCREMENT)
);
