USE demo_oath;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    oath_secret VARCHAR(255) DEFAULT NULL,
    mfa_enabled BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS backup_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    backup_code VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (username, password) VALUES ('CarlosMagno', 'TestPassword');
