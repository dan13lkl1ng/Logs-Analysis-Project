#!/usr/bin/env python3
import psycopg2 as pg


def db_connect():
    """
    Creates and returns a connection to the database defined by DBNAME,
    as well as a cursor for the database.
    Returns:
        db, c - a tuple. The first element is a connection to the database.
                The second element is a cursor for the database.
    """
    db = pg.connect("dbname=news")
    c = db.cursor()

    return (db, c)


def execute_query(query):
    """
    Takes an SQL query as a parameter.
    Executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    d = db_connect()
    d[1].execute(query)
    results = d[1].fetchall()
    d[0].close()
    return results


def print_top_authors():
    """Prints a list of authors ranked by article views."""
    query = """
        SELECT count(*) AS enum, n.name
        FROM (
            SELECT b.name, a.author, a.slug, a.title
            FROM articles AS a, authors AS b
            WHERE b.id = a.author) AS n,
            (
            SELECT path
            FROM log
            WHERE path LIKE '/article/%') AS l
            WHERE l.path = concat('/article/', n.slug)
            GROUP BY n.name
            ORDER BY enum DESC
        LIMIT 4;
    """
    results = execute_query(query)

    print("The most popular article authors of all time: \n")
    print("+---------------------------------------------------------+")
    print(": AUTHOR                                    |   VIEWS     :")
    print("+---------------------------------------------------------+")

    for row in results:
        print(":", row[1], " "*(40-len(row[1])), "|  ", row[0], " "*(8 -
              len(str(row[0]))), ':')

    print("+---------------------------------------------------------+")
    print("\t")


def print_top_articles():
    """Prints out the top 3 articles of all time."""
    query = """
    SELECT c.title AS Title, b.num as Number
    FROM (
        SELECT l.path, count(*) AS num
        FROM (
            SELECT path
            FROM log
            WHERE path LIKE '/article/%') as l,
            (
            SELECT DISTINCT slug
            FROM articles) AS a
            WHERE l.path LIKE concat('%',a.slug,'%')
            GROUP BY l.path
            ORDER BY num DESC) AS b,
        (
        SELECT slug, title
        FROM articles) AS c
        WHERE b.path LIKE concat('/article/', c.slug
        )
    LIMIT 3;
    """

    results = execute_query(query)

    print("The most popular three articles of all time: \n")
    print("+---------------------------------------------------------+")
    print(": ARTICLE                                   |   VIEWS     :")
    print("+---------------------------------------------------------+")
    for row in results:
        print(":", row[0], " "*(40-len(row[0])), "|  ", row[1], " "*(8 -
              len(str(row[1]))), ':')

    print("+---------------------------------------------------------+")
    print("\t")


def print_errors_over_one():
    """
    Prints out the days where more than 1% of logged access requests were
    errors.
    """

    query = """
            SELECT a.day as day, (sum_error::decimal / total::decimal) AS error
            FROM (
                SELECT count(*) AS total, time::date AS day
                FROM log
                GROUP BY day) AS a,
                (
                SELECT count(*) AS sum_error, time::date AS day
                FROM log
                WHERE status='404 NOT FOUND'
                GROUP BY day) AS b
            WHERE a.day = b.day
            AND (sum_error::decimal / total::decimal) > 0.01;
            """

    results = execute_query(query)
    print("\nDays with more than 1% of requests leading to errors: \n")

    print("+------------------------------------------+")
    print(": DAY                        |  PERCENTAGE :")
    print("+------------------------------------------+")

    for row in results:
        print(': {0:}                 |  {1:.2f}%      :'.format(row[0],
              row[1]*100))

    print("+------------------------------------------+")


"""
Code in this section only runs when program is executed
directly.
"""
if __name__ == '__main__':
    db_connect()
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
