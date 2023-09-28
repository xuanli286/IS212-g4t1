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
    Staff_password varchar(20) NOT NULL,
    Dept ENUM("Sales", "Consultancy", "System Solutioning", "Engineering Operation", "HR and Admin", "Finance", "IT"),
    Country ENUM("Malaysia", "Indonesia", "Vietnam", "Hong Kong"),
    Email varchar(50) NOT NULL,
    Access_ID int NOT NULL,
    CONSTRAINT staff_fk FOREIGN KEY (Access_ID) REFERENCES access_control(Access_ID)
);

CREATE TABLE IF NOT EXISTS `role` (
	Role_Name varchar(20) NOT NULL PRIMARY KEY,
	Role_Desc LONGTEXT
);

CREATE TABLE IF NOT EXISTS skill (
	Skill_Name varchar(20) NOT NULL PRIMARY KEY,
    Skill_Desc LONGTEXT
);

CREATE TABLE IF NOT EXISTS role_skill (
	Role_Name varchar(20) NOT NULL,
    Skill_Name varchar(20) NOT NULL,
    CONSTRAINT role_skill_pk PRIMARY KEY (Role_Name, Skill_Name),
    CONSTRAINT role_skill_fk1 FOREIGN KEY (Role_Name) REFERENCES `role`(Role_Name),
    CONSTRAINT role_skill_fk2 FOREIGN KEY (Skill_Name) REFERENCES skill(Skill_Name)
);

CREATE TABLE IF NOT EXISTS staff_skill (
	Staff_ID int NOT NULL,
    Skill_Name varchar(20) NOT NULL,
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
    Dept ENUM("Sales", "Consultancy", "System Solutioning", "Engineering Operation", "HR and Admin", "Finance", "IT"),
    Country ENUM("Malaysia", "Indonesia", "Vietnam", "Hong Kong"),
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
-- INSERT VALUES INTO TABLES
-- ---------------------------------------------------------

INSERT INTO access_control (Access_ID, Access_Control_Name) values
	(0, "User"), 
    (1, "Manager"), 
    (2, "Admin");
    

INSERT INTO staff (Staff_ID, Staff_FName, Staff_LName, Staff_password, Dept, Country, Email, Access_ID) values
	(1030, "Derek", "Tan", "derektan@123", "Sales", "Vietnam", "derektan@allinone.com", 1), 
    (1031, "Ernst", "Sim", "ernstsim@123", "Consultancy", "Hong Kong", "ernstsim@allinone.com", 0), 
    (1032, "Eric", "Loh", "ericloh@123", "System Solutioning", "Indonesia", "ericloh@allinone.com", 0), 
	(1033, "Philip", "Lee", "philiplee@123", "Engineering Operation", "Malaysia", "philiplee@allinone.com", 2), 
    (1034, "Sally", "Loh", "sallyloh@123", "HR and Admin", "Vietnam", "sallyloh@allinone.com", 2), 
    (1035, "David", "Yap", "davidyap@123", "Finance", "Malaysia", "davidyap@allinone.com", 1), 
    (1036, "Peter", "Yap", "peteryap@123", "IT", "Indonesia", "peteryap@allinone.com", 0);
    
INSERT INTO `role` (Role_Name, Role_Desc) values
	("Account Manager", "Account Managers are responsible for building and maintaining relationships with clients or customers. They serve as the main point of contact, understand client needs, and ensure that products or services meet their expectations. Account Managers may also identify opportunities for upselling or cross-selling to increase revenue."), 
    ("Consultant", "Consultants provide expert advice and solutions to clients or organizations. They typically specialize in a specific field, such as management, technology, or finance. Consultants assess problems, analyze data, and develop recommendations to help clients achieve their objectives. Effective communication and problem-solving skills are vital in this role."), 
    ("Software Engineer", "As a Software Engineer, you will be responsible for designing, developing, and maintaining software applications. You will collaborate with cross-functional teams to understand requirements, write code, and perform testing to ensure the software meets quality standards. Strong programming skills and problem-solving abilities are essential for success in this role."), 
    ("Database Admin", "Database Administrators are responsible for managing and maintaining an organization's databases. They ensure data integrity, security, and availability. DBAs design and optimize database structures, perform backups, and assist with data migration and recovery."), 
    ("Financial Analyst", "Financial Analysts analyze financial data, prepare reports, and provide insights to support business decision-making. They assess company financial performance, create forecasts, and identify trends. Strong analytical and spreadsheet skills, as well as knowledge of financial modeling, are crucial in this role.");
    
   
INSERT INTO skill (Skill_Name, Skill_Desc)  values
    ("Communication Skills", "Communication Skills description"),
    ("Account Planning", "Account Planning description"),
    ("Problem Solving", "Problem Solving description"),
    ("Data Analysis", "Data Analysis description"),
    ("Data Structures", "Data Structures description"),
    ("Web Development", "Web Development description"),
    ("Version Control", "Version Control description"),
    ("Database Management", "Database Management description"),
    ("Database Security", "Database Security description"),
    ("Financial Modeling", "Financial Modeling description"),
    ("Risk Management", "Risk Management description"),
    ("Financial Reporting", "Financial Reporting description");
      
    
INSERT INTO role_skill (Role_Name, Skill_Name) values
    ("Account Manager", "Communication Skills"),
    ("Account Manager", "Account Planning"),
    ("Account Manager", "Problem Solving"),
    ("Consultant", "Problem Solving"),
    ("Consultant", "Communication Skills"),
    ("Consultant", "Data Analysis"),
    ("Software Engineer", "Problem Solving"),
    ("Software Engineer", "Communication Skills"),
    ("Software Engineer", "Data Structures"),
    ("Software Engineer", "Version Control"),
    ("Software Engineer", "Web Development"),
    ("Database Admin", "Problem Solving"),
    ("Database Admin", "Database Management"),
    ("Database Admin", "Database Security"),
    ("Financial Analyst", "Data Analysis"),
    ("Financial Analyst", "Risk Management"),
    ("Financial Analyst", "Financial Modeling");


INSERT INTO staff_skill (Staff_ID, Skill_Name) values
    (1034, "Communication Skills"),
    (1030, "Account Planning"),
    (1034, "Problem Solving"),
    (1031, "Problem Solving"),
    (1033, "Communication Skills"),
    (1035, "Data Analysis"),
    (1032, "Problem Solving"),
    (1036, "Communication Skills"),
    (1033, "Data Structures"),
    (1036, "Version Control"),
    (1036, "Web Development"),
    (1030, "Problem Solving"),
    (1034, "Database Management"),
    (1032, "Database Security"),
    (1033, "Data Analysis"),
    (1031, "Risk Management");

-- 1033 - engineering, 1030 - sales, 1035 - finance
INSERT INTO role_listing (Role_Name, Application_Opening, Application_Deadline, Dept, Country, Manager_ID) values 
	("Software Engineer", "2023-09-15", "2023-12-31", "Engineering Operation", "Hong Kong", 1033),
    ("Database Admin", "2023-09-20", "2023-11-18", "Engineering Operation", "Indonesia", 1033),
    ("Financial Analyst", "2023-05-02", "2023-08-23", "Finance", "Vietnam", 1035);

INSERT INTO application (Staff_ID, RoleListing_ID, Application_Date, Percentage_Match) values 
	(1036, 1, "2023-10-18", 60),
    (1035, 1, "2023-11-16", 50),
    (1034, 2, "2023-10-01", 66.67),
    (1031, 3, "2023-06-05", 33.33);

    

