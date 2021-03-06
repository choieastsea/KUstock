drop database kustock;
create database kustock;
use kustock;
-- user
CREATE TABLE user (
   uid INTEGER NOT NULL,
   gid VARCHAR(50) NOT NULL,
   uname VARCHAR(50) NOT NULL,
   seed INTEGER NOT NULL,
   profit INTEGER NOT NULL,
   status INTEGER NOT NULL,
   instruction VARCHAR(100) DEFAULT 'empty instruction'
);

-- user
ALTER TABLE user
   ADD CONSTRAINT PK_user -- user 기본키
   PRIMARY KEY (
   uid -- uid
   );

ALTER TABLE user
   MODIFY COLUMN uid INTEGER NOT NULL AUTO_INCREMENT;

-- trade
CREATE TABLE trade (
   tid INTEGER NOT NULL,
   uid INTEGER NOT NULL,
   date DATE NOT NULL,
   price INTEGER NOT NULL,
   count INTEGER NOT NULL,
   buysell ENUM('TRUE','FALSE') NOT NULL,
   code CHAR(7) NOT NULL
);

-- trade
ALTER TABLE trade
   ADD CONSTRAINT PK_trade -- trade 기본키
   PRIMARY KEY (
   tid, -- tid
   uid  -- uid
   );

ALTER TABLE trade
   MODIFY COLUMN tid INTEGER NOT NULL AUTO_INCREMENT;

-- alarm
CREATE TABLE alarm (
   aid INTEGER NOT NULL,
   uid INTEGER NOT NULL,
   code CHAR(7) NOT NULL,
   time TIME NOT NULL,
   onoff ENUM('TRUE','FALSE') NOT NULL
);

-- alarm
ALTER TABLE alarm
   ADD CONSTRAINT PK_alarm -- alarm 기본키
   PRIMARY KEY (
   aid, -- aid
   uid  -- uid
   );

ALTER TABLE alarm
   MODIFY COLUMN aid INTEGER NOT NULL AUTO_INCREMENT;

-- 새 테이블
CREATE TABLE stock (
   code CHAR(7) NOT NULL,
   sname VARCHAR(50) NOT NULL
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
   ADD CONSTRAINT FK_user_TO_alarm -- user -> alarm
   FOREIGN KEY (
   uid -- uid
   )
   REFERENCES user ( -- user
   uid -- uid
   );

-- theme
CREATE TABLE theme (
   thid INTEGER NOT NULL,
   code VARCHAR(50) NOT NULL,
   url VARCHAR(200)
);

-- theme
ALTER TABLE theme
   ADD CONSTRAINT PK_theme -- theme 기본키
   PRIMARY KEY (
   thid -- thid
   );

ALTER TABLE theme
   MODIFY COLUMN thid INTEGER NOT NULL AUTO_INCREMENT;
