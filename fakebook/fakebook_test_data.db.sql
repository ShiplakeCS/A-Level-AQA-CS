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
	`bio`	TEXT DEFAULT 'A fatnastic FakeBook member!',
	`dob`	TEXT
);
INSERT INTO `User` (id,username,email,password_hash,first_name,surname,joined,profile_pic_id,bio,dob) VALUES 
 (1,'ad','adimmick@shiplake.org.uk','123456','Adam','Dimmick','2018-04-02 12:00:00',NULL,'I created FakeBook.','1983-12-06'),
 (2,'louise','louisedimmick@hotmail.com','654321','Louise','Dimmick','2018-04-02 12:05:00',NULL,'A fatnastic FakeBook member!','1988-12-28'),
 (3,'cat','annabelle@dimmick.com','dreamies','Annabelle','Dimmick','2018-04-02 12:10:00',NULL,'A fatnastic FakeBook member!','2013-10-01');

CREATE TABLE IF NOT EXISTS `Tag` (
	`post_id`	INTEGER,
	`tagged_user_id`	INTEGER,
	PRIMARY KEY(`tagged_user_id`,`post_id`)
);
INSERT INTO `Tag` (post_id,tagged_user_id) VALUES (2,1);

CREATE TABLE IF NOT EXISTS `Post` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`author_id`	INTEGER NOT NULL,
	`text`	TEXT NOT NULL,
	`media_id`	INTEGER,
	`timestamp`	TEXT,
	`public`	INTEGER NOT NULL DEFAULT 0
);
INSERT INTO `Post` (id,author_id,text,media_id,timestamp,public) VALUES
 (1,1,'The very first post on FakeBook!','','2018-04-02 14:00:00',1),
 (2,2,'Louise''s first post','','2018-04-02 14:05:00',1),
 (3,1,'My first private (friends only) post.',NULL,'2018-04-02 14:05:00',0),
 (4,3,'Meow','','2018-04-02 16:00:00',1);

CREATE TABLE IF NOT EXISTS `Message` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`chatgroup_id`	INTEGER NOT NULL,
	`author_id`	INTEGER NOT NULL,
	`text`	TEXT NOT NULL,
	`timestamp`	TEXT NOT NULL
);
INSERT INTO `Message` (id,chatgroup_id,author_id,text,timestamp) VALUES
 (1,1,1,'Hey there! This is the messaging platform!','2018-04-02 16:00:00'),
 (2,1,2,'Hey! This is cool!','2018-04-02 16:01:00'),
 (3,1,1,'Thanks! It will be even cooler when it actually works properly via a website!','2018-04-02 16:02:00');

CREATE TABLE IF NOT EXISTS `Media` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`file_path`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Like` (
	`post_id`	INTEGER,
	`user_id`	INTEGER,
	PRIMARY KEY(`post_id`,`user_id`)
);
INSERT INTO `Like` (post_id,user_id) VALUES
 (1,2),
 (2,1);
CREATE TABLE IF NOT EXISTS `Friendship` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`initiator_id`	INTEGER NOT NULL,
	`recipient_id`	INTEGER NOT NULL,
	`accepted`	INTEGER NOT NULL DEFAULT 0,
	`established_date`	TEXT
);
INSERT INTO `Friendship` (id,initiator_id,recipient_id,accepted,established_date) VALUES 
 (1,1,2,1,'2018-04-02 13:00:00'),
 (2,2,3,1,'2018-04-02 13:00:00'),
 (3,1,3,0,NULL);

CREATE TABLE IF NOT EXISTS `ChatGroupMember` (
	`chatgroup_id`	INTEGER,
	`user_id`	INTEGER,
	PRIMARY KEY(`chatgroup_id`,`user_id`)
);
INSERT INTO `ChatGroupMember` (chatgroup_id,user_id) VALUES 
 (1,1),
 (1,2);

CREATE TABLE IF NOT EXISTS `ChatGroup` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL
);
INSERT INTO `ChatGroup` (id,name) VALUES
 (1,'The Dimmicks');
COMMIT;
