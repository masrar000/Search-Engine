-- Create Database named MY_CUSTOM_BOT
CREATE DATABASE MY_CUSTOM_BOT;
COMMIT;

-- Define MY_CUSTOM_BOT as the database to perform actions on
USE MY_CUSTOM_BOT;

-- Table for search queries
CREATE TABLE searches (
    search_id INT NOT NULL AUTO_INCREMENT,
    query VARCHAR(255) NULL,
    engine VARCHAR(10) NOT NULL,
    PRIMARY KEY(search_id)
);
COMMIT;

-- Table for search results
CREATE TABLE search_results (
    url_id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(768) NOT NULL,
    search_id INT NOT NULL,
    word_counts JSON,
    PRIMARY KEY(url_id),
    FOREIGN KEY (search_id) REFERENCES searches(search_id) ON DELETE CASCADE,
    UNIQUE(url)
) ENGINE=InnoDB;
COMMIT;

-- Table for search_results_v2
/*CREATE TABLE search_results_v2 (
    url_id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(768) NOT NULL,
    search_id INT NOT NULL,
    title VARCHAR(248),
    PRIMARY KEY(url_id),
    FOREIGN KEY (search_id) REFERENCES searches(search_id) ON DELETE CASCADE,
    UNIQUE(url)
) ENGINE=InnoDB;
COMMIT;
*/


