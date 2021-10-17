CREATE TABLE home (
    id int NOT NULL AUTO_INCREMENT,
    F_name VARCHAR(100),
    L_name VARCHAR(100),
    Contect_Number INT(15),
    email VARCHAR(255),
    message varchar(255),
    date_created  DATETIME DEFAULT   CURRENT_TIMESTAMP,
PRIMARY KEY (id)
);


CREATE TABLE sign(
    id int NOT NULL AUTO_INCREMENT,
    F_Name VARCHAR(255),
    L_Name VARCHAR(255),
    email VARCHAR(255),
    password varchar(255),
    date_created  DATETIME DEFAULT   CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
    CONSTRAINT constraint_name UNIQUE (email)
);


CREATE TABLE login(
    id int NOT NULL AUTO_INCREMENT,
	email VARCHAR(255),
    password varchar(255),
    date_created  DATETIME DEFAULT   CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
);
