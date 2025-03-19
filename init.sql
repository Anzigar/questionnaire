-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS questionnaire_db;

-- Grant permissions to questionnaire_user
GRANT ALL PRIVILEGES ON questionnaire_db.* TO 'questionnaire_user'@'%';
FLUSH PRIVILEGES;
