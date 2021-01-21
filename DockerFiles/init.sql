
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