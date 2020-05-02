DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    insert_time    DATETIME    NOT NULL,
    who     BINARY  NOT NULL,
    old     TEXT    NOT NULL,
    new     TEXT    NOT NULL
);
