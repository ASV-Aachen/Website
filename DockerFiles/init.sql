
-- Wiki
CREATE user 'wiki'@'%' WITH PASSWORD = 'my-secret-pw';
CREATE DATABASE wikiDB;
GRANT ALL PRIVILEGES ON DATABASE wikiDB to wiki;


-- Website
CREATE user 'website'@'%' WITH PASSWORD = 'my-secret-pw';
CREATE DATABASE websiteDB;
GRANT ALL PRIVILEGES ON DATABASE websiteDB to website;

-- Keycloak
CREATE USER 'Keycloack'@'%' WITH PASSWORD = 'my-secret-pw';
CREATE DATABASE KeycloackDB;
GRANT ALL PRIVILEGES ON DATABASE KeycloackDB TO Keycloack;