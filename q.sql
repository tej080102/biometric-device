CREATE DATABASE IF NOT EXISTS att_records;
USE att_records;
CREATE TABLE IF NOT EXISTS att_logs (UID VARCHAR(20), Time TIMESTAMP(0), PRIMARY KEY(UID));
CREATE TABLE IF NOT EXISTS users (UID VARCHAR(20), Name VARCHAR(100), Privilege VARCHAR(20), PRIMARY KEY(UID));
COMMIT;