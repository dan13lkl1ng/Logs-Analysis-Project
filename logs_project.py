#!/usr/bin/env python3
import psycopg2 as pg

db = pg.connect("dbname=news")
c = db.cursor()

c.execute("select c.title as Title, b.num as Number from ( select l.path, "
          "count(*) as num from (select path from log where path like '/articl"
          "e/%') "
          "as l,"
          "(select distinct slug from articles) as a where l.path like "
          "concat('%',a.slug,'%') group by l.path order by num desc) as b, (se"
          "lect s"
          "lug,"
          "title from articles) as c where b.path like concat('/article/',"
          "c.slug);")

query = c.fetchall()

print("The most popular three articles of all time: \n")
print("+---------------------------------------------------------+")
print(": ARTICLE                                   |   VIEWS     :")
print("+---------------------------------------------------------+")
for row in query:
    print(":", row[0], " "*(40-len(row[0])), "|  ", row[1], " "*(8 -
          len(str(row[1]))), ':')

print("+---------------------------------------------------------+")
print("\t")

c.execute("select count(*) as enum, n.name from (select b.name, a.author, a.sl"
          "ug, a.title from articles as a, authors as b where b.id = a.author)"
          "as n, (select path from log where path like '/article/%') as l wher"
          "e l.path = concat('/article/', n.slug) group by n.name order by enu"
          "m desc limit 4;")
q2 = c.fetchall()

print("The most popular article authors of all time: \n")
print("+---------------------------------------------------------+")
print(": AUTHOR                                    |   VIEWS     :")
print("+---------------------------------------------------------+")

for row in q2:
    print(":", row[1], " "*(40-len(row[1])), "|  ", row[0], " "*(8 -
          len(str(row[0]))), ':')

print("+---------------------------------------------------------+")
print("\t")

c.execute("select * from (select day, total, sum_error, sum_error::decimal"
          "/ total::decimal as percent from (select count(status) as total , d"
          "ate_part('day', time) as day from log group by date_part('day',time"
          ")) as a, (select count(status) as sum_error, date_part('day', time)"
          "as day2 from log where status ='404 NOT FOUND' group by date_part('"
          "day',time)) as b where a.day = b.day2) c where c.percent >0.01;")

q3 = c.fetchall()

print("\nDays with more than 1% of requests leading to errors: \n")

print("+------------------------------------------+")
print(": DAY                        |  PERCENTAGE :")
print("+------------------------------------------+")

for row in q3:
    print(': {0:2d}                         | {1:.4f}      :'.format(int(
          row[0]), row[3]))

print("+------------------------------------------+")

db.close
