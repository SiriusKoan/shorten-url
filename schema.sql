DROP TABLE IF EXISTS short;
CREATE TABLE short (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    who     BINARY  NOT NULL,
    old     TEXT    NOT NULL,
    new     TEXT    NOT NULL
);
