# DocumentConverter
[![Build Status](https://travis-ci.com/LoDThe/DocumentConverter.svg?branch=master)](https://travis-ci.com/LoDThe/DocumentConverter)
[![codecov](https://codecov.io/gh/LoDThe/DocumentConverter/branch/master/graph/badge.svg)](https://codecov.io/gh/LoDThe/DocumentConverter)
    
DocumentConverter is a simple realization of web-application, which purpose is converting document between different types

To convert a document you need to execute a POST query with file by following URL

`http://<server-name>:<server-port>/convert/<output-type>`

You can read task description in more details [here](https://docs.google.com/document/d/1lDirPrxqhrIkkDXW3sbIWr6cRhFdlra0rSmd0RHjH8s/edit) (RUSSIAN LANGUAGE)

[Flask](https://palletsprojects.com/p/flask/) was chosen as web-application creating framework, [Pandoc](https://pandoc.org/) as files convertation library.

There is [Travis](https://travis-ci.com) as CI and pytest as a testing tool also.

## Requirements
Python at least 3.7 version, installed [Pandoc](https://pandoc.org/) library and python-libraries from [requirements.txt](requirements.txt)

Example of requirements installing:

**Ubuntu**
```shell script
apt-get install pandoc
pip install -r requirements.txt
```
**Arch**
```shell script
pacman -S pandoc
pip install -r requirements.txt
```

## How to use it?
Execute is `src` directory
```shell script
flask run --host=127.0.0.2 --port=1234
```
Default arguments:

| Variable   | Value     |
|------------|-----------|
| host       | 127.0.0.1 |
| port       | 5000      |

By following link you can receive available conversions list in JSON format:
```http://host:port/get_available_conversions```

This will run application with possibility of execution POST queries by the following URL
```http://host:port/convert/<output-type>```

Query should be execute like it's user is sending file from input form with name *file*. For instance, through the html form `<input type=file name=file>`

## Available conversion types

| Input format   |      Output formats      | 
|----------------|----------------------------|
| html           |html, markdown, plain       |
| markdown       |markdown, html, plain       |
| docx           |docx, html, markdown, plain |
| odt            |odt, html, markdown, plain  |

## To-do
- [x] Create application
- [x] Create
  - [x] Unit tests
  - [x] Integration tests
- [x] Start using code coverage
- [x] Start using CI (Travis was chose)
- [x] Fix input file format recognizing