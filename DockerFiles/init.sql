
-- Wiki
CREATE USER 'wiki'@'%' IDENTIFIED BY 'my-secret-pw';
CREATE DATABASE wikiDB;
GRANT ALL PRIVILEGES ON wikiDB.* to 'wiki'@'%';

-- Website
CREATE USER 'website'@'%' IDENTIFIED BY 'my-secret-pw';
CREATE DATABASE websiteDB;
GRANT ALL PRIVILEGES ON websiteDB.* to 'website'@'%';

-- Keycloak
CREATE USER 'Keycloack'@'%' IDENTIFIED BY 'my-secret-pw';
CREATE DATABASE KeycloackDB;
GRANT ALL PRIVILEGES ON KeycloackDB.* TO 'Keycloack'@'%';


-- for SSO
SET GLOBAL innodb_file_format = Barracuda;
SET GLOBAL innodb_file_per_table = on;
SET GLOBAL innodb_default_row_format = dynamic;
SET GLOBAL innodb_large_prefix = 1;
SET GLOBAL innodb_file_format_max = Barracuda;