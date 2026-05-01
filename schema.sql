--  Book Tracker Database Schema

-- Create and select the database
CREATE DATABASE IF NOT EXISTS book_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE book_tracker;

--  TABLE: publisher
--  One publisher can release many books (1:M)

DROP TABLE IF EXISTS publisher; 
CREATE TABLE publisher (
  publisher_id  INT            NOT NULL AUTO_INCREMENT,
  name          VARCHAR(150)   NOT NULL,
  website       VARCHAR(255)       NULL,
  country       VARCHAR(100)       NULL,
  PRIMARY KEY (publisher_id)
);

--  TABLE: author
--  Core info and credentials for each author

DROP TABLE IF EXISTS author; 
CREATE TABLE author (
  author_id          INT           NOT NULL AUTO_INCREMENT,
  first_name         VARCHAR(100)  NOT NULL,
  last_name          VARCHAR(100)  NOT NULL,
  bio                TEXT              NULL,
  field_of_expertise VARCHAR(150)      NULL,
  credentials        TEXT              NULL,
  PRIMARY KEY (author_id)
);

--  TABLE: category
--  Applicable use areas: finance, marketing, habits, etc.

DROP TABLE IF EXISTS category; 
CREATE TABLE category (
  category_id  INT           NOT NULL AUTO_INCREMENT,
  name         VARCHAR(100)  NOT NULL UNIQUE,
  description  TEXT              NULL,
  PRIMARY KEY (category_id)
);

--  TABLE: book
--  Core book record — links to publisher (FK)

DROP TABLE IF EXISTS book; 
CREATE TABLE book (
  book_id         INT            NOT NULL AUTO_INCREMENT,
  title           VARCHAR(255)   NOT NULL,
  publisher_id    INT                NULL,
  page_count      INT                NULL,
  word_count      INT                NULL,
  read_time_hours DECIMAL(5, 1)      NULL  COMMENT 'Estimated hours to read',
  depth_level     ENUM(
                    'broad',
                    'moderate',
                    'in-depth'
                  )              NOT NULL DEFAULT 'moderate',
  approval_rating DECIMAL(4, 2)      NULL  COMMENT 'Rating out of 10.00',
  description     TEXT               NULL,
  PRIMARY KEY (book_id),
  CONSTRAINT fk_book_publisher
    FOREIGN KEY (publisher_id)
    REFERENCES publisher (publisher_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT chk_approval_rating
    CHECK (approval_rating BETWEEN 0 AND 10),
  CONSTRAINT chk_page_count
    CHECK (page_count > 0),
  CONSTRAINT chk_word_count
    CHECK (word_count > 0),
  CONSTRAINT chk_read_time
    CHECK (read_time_hours > 0)
);

--  TABLE: book_author  (junction — M:N)
--  Resolves the many-to-many between book and author

DROP TABLE IF EXISTS book_author; 
CREATE TABLE book_author (
  book_id    INT  NOT NULL,
  author_id  INT  NOT NULL,
  PRIMARY KEY (book_id, author_id),
  CONSTRAINT fk_ba_book
    FOREIGN KEY (book_id)
    REFERENCES book (book_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_ba_author
    FOREIGN KEY (author_id)
    REFERENCES author (author_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--  TABLE: book_category  (junction — M:N)
--  Resolves the many-to-many between book and category

DROP TABLE IF EXISTS book_category; 
CREATE TABLE book_category (
  book_id      INT  NOT NULL,
  category_id  INT  NOT NULL,
  PRIMARY KEY (book_id, category_id),
  CONSTRAINT fk_bc_book
    FOREIGN KEY (book_id)
    REFERENCES book (book_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_bc_category
    FOREIGN KEY (category_id)
    REFERENCES category (category_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--  INDEXES
--  Speed up common lookups

CREATE INDEX idx_book_title       ON book          (title);
CREATE INDEX idx_book_rating      ON book          (approval_rating);
CREATE INDEX idx_book_depth       ON book          (depth_level);
CREATE INDEX idx_author_last      ON author        (last_name);
CREATE INDEX idx_category_name    ON category      (name);
CREATE INDEX idx_ba_author        ON book_author   (author_id);
CREATE INDEX idx_bc_category      ON book_category (category_id);
