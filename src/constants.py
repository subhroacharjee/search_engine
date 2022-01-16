URL_REGEX = "(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"


CREATE_SEARCH_TABLE_QUERIES = """
CREATE TABLE IF NOT EXISTS websites (
    id integer PRIMARY KEY,
    url text NOT NULL UNIQUE,
    title text NOT NULL,
    description text DEFAULT NULL,
    tags text DEFAULT NULL,
    created_at text DEFAULT DATE('now')
);
""";
CREATE_QUEUE_TABLE_QUERIES = """
CREATE TABLE IF NOT EXISTS queue (
    id integer PRIMARY KEY,
    url text not NULL UNIQUE,
    completed integer DEFAULT 0,
    created_at text DEFAULT DATE('now')
);
        """

ADD_TO_SEARCH_TABLE = """
INSERT INTO websites(
    url, 
    title, 
    description, 
    tags
) 
VALUES(
    ?,?,?,?
)
"""

ADD_TO_QUEUE_TABLE = """
INSERT INTO queue(
    url
) VALUES(?)
"""

MARK_URL_COMPLETED_STATUS = """
UPDATE 
    SET completed = 1
WHERE
    url = ?
"""

CHECK_IF_URL_EXISTS = """
SELECT 
    *
FROM queue
WHERE url=?
LIMIT 1
"""

GET_ALL_UNPARSED_URLS = """
SELECT 
    url
FROM queue
WHERE completed=0
ORDER BY created_at
"""
