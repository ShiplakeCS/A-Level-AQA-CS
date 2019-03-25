BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `User` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT NOT NULL UNIQUE,
	`email`	TEXT NOT NULL UNIQUE,
	`password_hash`	TEXT NOT NULL,
	`first_name`	TEXT NOT NULL,
	`surname`	TEXT NOT NULL,
	`joined`	TEXT NOT NULL,
	`profile_pic_id`	INTEGER,
	`bio`	TEXT DEFAULT 'A fatnastic FakeBook member!'
);
CREATE TABLE IF NOT EXISTS `Tag` (
	`post_id`	INTEGER,
	`tagged_user_id`	INTEGER,
	PRIMARY KEY(`tagged_user_id`,`post_id`)
);
CREATE TABLE IF NOT EXISTS `Post` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`author_id`	INTEGER NOT NULL,
	`text`	TEXT NOT NULL,
	`media_id`	INTEGER,
	`timestamp`	TEXT
);
CREATE TABLE IF NOT EXISTS `Message` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`chatgroup_id`	INTEGER NOT NULL,
	`author_id`	INTEGER NOT NULL,
	`text`	TEXT NOT NULL,
	`timestamp`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Media` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`file_path`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Like` (
	`post_id`	INTEGER,
	`user_id`	INTEGER,
	PRIMARY KEY(`post_id`,`user_id`)
);
CREATE TABLE IF NOT EXISTS `Friendship` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`initiator_id`	INTEGER NOT NULL,
	`recipient_id`	INTEGER NOT NULL,
	`accepted`	INTEGER NOT NULL DEFAULT 0,
	`established_date`	TEXT
);
CREATE TABLE IF NOT EXISTS `ChatGroupMember` (
	`chatgroup_id`	INTEGER,
	`user_id`	INTEGER,
	PRIMARY KEY(`chatgroup_id`,`user_id`)
);
CREATE TABLE IF NOT EXISTS `ChatGroup` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL
);
COMMIT;
