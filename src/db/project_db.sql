CREATE TABLE users (
  ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  the_user_name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(255),
  auto_login_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE history (
  ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_id int,
  task_type varchar(20),
  task_date datetime,
  FOREIGN KEY (user_id) REFERENCES users (ID)
);

CREATE TABLE pfp_path (
  user_id int,
  img_path VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users (ID)
);