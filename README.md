# Logs Analysis Project
Made during Google Scholarship of Full Stack Web Developer Nanodegree Program at Udacity - 2018

This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
* Vagrant
* VirtualBox

or

* Python 3
* PostgreSQL
* psycopg2

## Getting started
### Vagrantfile
If you are using the Vagrantfile supplied by Udacity, the database is ready and you can start the Python script inside the VirtualBox.
Go to the vagrant folder and start the virtual machine:
```bash
$ vagrant up
```
log in:
```bash
$ vagrant ssh
```
and you are able to start the script:
```bash
$ python3 logs_project.py
```

### Without Vagrantfile

In the case you are not using the Vagrantfile, download and unzip the database from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
Set-up the news database.
```bash
$ psql -d news -f newsdata.sql
```
## Usage
You can run the script by:
```
$ python3 logs_project.py
```
