drop database kustock;
create database kustock;
use kustock;
-- user
CREATE TABLE user (
<<<<<<< HEAD
	uid INTEGER NOT NULL,
	gid INTEGER NOT NULL,
	uname VARCHAR(50) NOT NULL,
	seed INTEGER NOT NULL,
	profit INTEGER NOT NULL
=======
   uid INTEGER NOT NULL,
   gid INTEGER NOT NULL,
   uname VARCHAR(50) NOT NULL,
   seed INTEGER NOT NULL,
   profit INTEGER NOT NULL
>>>>>>> main
);

-- user
ALTER TABLE user
	ADD CONSTRAINT PK_user -- user 기본키
	PRIMARY KEY (
	uid -- uid
	);

ALTER TABLE user
	MODIFY COLUMN uid INTEGER NOT NULL AUTO_INCREMENT(1,1);

-- trade
CREATE TABLE trade (
<<<<<<< HEAD
	tid INTEGER NOT NULL,
	uid INTEGER NOT NULL,
	date DATE NOT NULL,
	price INTEGER NOT NULL,
	count INTEGER NOT NULL,
	buysell ENUM('TRUE','FALSE') NOT NULL,
	code CHAR(7) NOT NULL
=======
   tid INTEGER NOT NULL,
   uid INTEGER NOT NULL,
   date DATE NOT NULL,
   price INTEGER NOT NULL,
   count INTEGER NOT NULL,
   buysell ENUM('TRUE','FALSE') NOT NULL,
   code CHAR(7) NOT NULL
>>>>>>> main
);

-- trade
ALTER TABLE trade
	ADD CONSTRAINT PK_trade -- trade 기본키
	PRIMARY KEY (
	tid, -- tid
	uid  -- uid
	);

ALTER TABLE trade
	MODIFY COLUMN tid INTEGER NOT NULL AUTO_INCREMENT(1,1);

-- alarm
CREATE TABLE alarm (
<<<<<<< HEAD
	aid INTEGER NOT NULL,
	uid INTEGER NOT NULL,
	code CHAR(7) NOT NULL,
	time TIME NOT NULL,
	onoff ENUM('TRUE','FALSE') NOT NULL
=======
   aid INTEGER NOT NULL,
   uid INTEGER NOT NULL,
   code CHAR(7) NOT NULL,
   time TIME NOT NULL,
   onoff ENUM('TRUE','FALSE') NOT NULL
>>>>>>> main
);

-- alarm
ALTER TABLE alarm
	ADD CONSTRAINT PK_alarm -- alarm 기본키
	PRIMARY KEY (
	aid, -- aid
	uid  -- uid
	);

ALTER TABLE alarm
	MODIFY COLUMN aid INTEGER NOT NULL AUTO_INCREMENT(1,1);

-- 새 테이블
CREATE TABLE stock (
<<<<<<< HEAD
	code CHAR(7) NOT NULL,
	sname VARCHAR(50) NOT NULL
=======
   code CHAR(7) NOT NULL,
   sname VARCHAR(50) NOT NULL
>>>>>>> main
);

-- trade
ALTER TABLE trade
	ADD CONSTRAINT FK_user_TO_trade -- user -> trade
	FOREIGN KEY (
	uid -- uid
	)
	REFERENCES user ( -- user
	uid -- uid
	);

-- alarm
ALTER TABLE alarm
<<<<<<< HEAD
	ADD CONSTRAINT FK_user_TO_alarm -- user -> alarm
	FOREIGN KEY (
	uid -- uid
	)
	REFERENCES user ( -- user
	uid -- uid
	);
=======
   ADD CONSTRAINT FK_user_TO_alarm -- user -> alarm
   FOREIGN KEY (
   uid -- uid
   )
   REFERENCES user ( -- user
   uid -- uid
   );
>>>>>>> main
