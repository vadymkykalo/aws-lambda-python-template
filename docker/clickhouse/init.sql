-- create your init query if you need

--CREATE USER OR REPLACE monitoring PROFILE 'default';
CREATE ROLE IF NOT EXISTS test;
CREATE ROLE IF NOT EXISTS readonly;

GRANT SELECT ON test.* TO test;
GRANT INSERT ON test.* TO test;
GRANT DROP TABLE ON test.* TO test;

GRANT CREATE DATABASE ON test.* TO test;
GRANT CREATE TABLE ON test.* TO test;
GRANT CREATE VIEW ON test.* TO test;
GRANT CREATE DICTIONARY ON test.* TO test;
GRANT SHOW TABLES ON test.* TO test;
GRANT SHOW COLUMNS ON test.* TO test;
GRANT SHOW DICTIONARIES ON test.* TO test;

GRANT SELECT ON *.* TO readonly;
GRANT CREATE TEMPORARY TABLE ON *.* TO readonly;
GRANT SHOW DATABASES ON * TO readonly;
GRANT SHOW TABLES ON *.* TO readonly;
GRANT SHOW COLUMNS ON *.* TO readonly;
GRANT SHOW DICTIONARIES ON *.* TO readonly;

CREATE USER IF NOT EXISTS test_lambda IDENTIFIED WITH sha256_password BY 'secret' DEFAULT ROLE test;
CREATE DATABASE IF NOT EXISTS test;

CREATE TABLE IF NOT EXISTS test.tester
(
    id UUID,
    name Nullable(String),
    create_at DateTime

) ENGINE = MergeTree()
PARTITION BY toYYYYMM(create_at)
ORDER BY (create_at)
TTL create_at + toIntervalDay(730);
