CREATE DATABASE IF NOT EXISTS g4t1;

USE g4t1;

-- ---------------------------------------------------------
-- CREATE TABLES
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS access_control (
	Access_ID int NOT NULL PRIMARY KEY,
    Access_Control_Name varchar(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS staff (
    Staff_ID int NOT NULL PRIMARY KEY,
    Staff_FName varchar(50) NOT NULL,
    Staff_LName varchar(50) NOT NULL,
    Staff_password varchar(50) NOT NULL,
    Dept ENUM("Chairman", "CEO", "Sales", "Consultancy", "Solutioning", "Engineering", "HR", "Finance", "IT"),
    Country ENUM("Malaysia", "Indonesia", "Vietnam", "Hong Kong", "Singapore"),
    Email varchar(50) NOT NULL,
    Access_ID int NOT NULL,
    CONSTRAINT staff_fk FOREIGN KEY (Access_ID) REFERENCES access_control(Access_ID)
);

CREATE TABLE IF NOT EXISTS `role` (
	Role_Name varchar(20) NOT NULL PRIMARY KEY,
	Role_Desc LONGTEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skill (
	Skill_Name varchar(50) NOT NULL PRIMARY KEY,
    Skill_Desc LONGTEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS role_skill (
	Role_Name varchar(20) NOT NULL,
    Skill_Name varchar(50) NOT NULL,
    CONSTRAINT role_skill_pk PRIMARY KEY (Role_Name, Skill_Name),
    CONSTRAINT role_skill_fk1 FOREIGN KEY (Role_Name) REFERENCES `role`(Role_Name),
    CONSTRAINT role_skill_fk2 FOREIGN KEY (Skill_Name) REFERENCES skill(Skill_Name)
);

CREATE TABLE IF NOT EXISTS staff_skill (
	Staff_ID int NOT NULL,
    Skill_Name varchar(50) NOT NULL,
    CONSTRAINT staff_skill_pk PRIMARY KEY (Staff_ID, Skill_Name),
    CONSTRAINT staff_skill_fk1 FOREIGN KEY (Staff_ID) REFERENCES staff(Staff_ID),
    CONSTRAINT staff_skill_fk2 FOREIGN KEY (Skill_Name) REFERENCES skill(Skill_Name)
);

CREATE TABLE IF NOT EXISTS role_listing (
	RoleListing_ID int auto_increment primary key,
	Role_Name varchar(20) NOT NULL,
    Application_Opening date NOT NULL,
    Application_Deadline date NOT NULL,
	Manager_ID int NOT NULL,
    Dept ENUM("Chairman", "CEO", "Sales", "Consultancy", "Solutioning", "Engineering", "HR", "Finance", "IT"),
    Country ENUM("Malaysia", "Indonesia", "Vietnam", "Hong Kong", "Singapore"),
    CONSTRAINT role_listing_fk1 FOREIGN KEY (Role_Name) REFERENCES `role`(Role_Name),
    CONSTRAINT role_listing_fk2 FOREIGN KEY (Manager_ID) REFERENCES staff(Staff_ID)
);

CREATE TABLE IF NOT EXISTS application (
	Staff_ID int NOT NULL,
	RoleListing_ID int NOT NULL,
    Application_Date date NOT NULL,
	Percentage_Match decimal(5,2) NOT NULL,
    CONSTRAINT application_pk PRIMARY KEY (Staff_ID, RoleListing_ID),
    CONSTRAINT application_fk1 FOREIGN KEY (RoleListing_ID) REFERENCES role_listing(RoleListing_ID),
    CONSTRAINT application_fk2 FOREIGN KEY (Staff_ID) REFERENCES staff(Staff_ID)
);


-- ---------------------------------------------------------
-- Load Data into tables (for local db only)
-- Please refer to CD Setup Documentation on how to load data
-- Please change file reference link to where the directory pointed by secure_file_priv
-- Example: "C:/wamp64/tmp/"
-- ---------------------------------------------------------

-- uncomment this line to find which directory to save sbrp_data in
-- SHOW VARIABLES LIKE "secure_file_priv"

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/Access_Control.csv"
INTO TABLE access_control
CHARACTER SET latin1
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
LINES TERMINATED BY "\r\n"
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/staff.csv"
INTO TABLE staff
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/role.csv"
INTO TABLE `role`
CHARACTER SET latin1
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
LINES TERMINATED BY "\r\n"
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/skill.csv"
INTO TABLE skill
CHARACTER SET latin1
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
LINES TERMINATED BY "\r\n"
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/role_skill.csv"
INTO TABLE role_skill
CHARACTER SET latin1
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
LINES TERMINATED BY "\r\n"
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/staff_skill.csv"
INTO TABLE staff_skill
CHARACTER SET latin1
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
LINES TERMINATED BY "\r\n"
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/rolelisting.csv"
INTO TABLE role_listing
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
IGNORE 1 LINES;

LOAD DATA INFILE "C:/wamp64/tmp/sbrp_data/application.csv"
INTO TABLE application
FIELDS TERMINATED BY ","
ENCLOSED BY '"'
IGNORE 1 LINES;

    

