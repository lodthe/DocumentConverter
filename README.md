# DocumentConverter
[![Build Status](https://travis-ci.com/LoDThe/DocumentConverter.svg?branch=master)](https://travis-ci.com/LoDThe/DocumentConverter)
[![codecov](https://codecov.io/gh/LoDThe/DocumentConverter/branch/master/graph/badge.svg)](https://codecov.io/gh/LoDThe/DocumentConverter)
    
DocumentConverter is a simple web-application that purpose is converting document between different filetypes.

To convert a document you need to execute a POST request with file by following URL

`http://<server-name>:<server-port>/convert/<output-type>`

You can read the task description more detaily [here](https://docs.google.com/document/d/1lDirPrxqhrIkkDXW3sbIWr6cRhFdlra0rSmd0RHjH8s/edit) (in Russian)

[Flask](https://palletsprojects.com/p/flask/) was chosen as web-application framework, [Pandoc](https://pandoc.org/) as files convertation library.

I used [Travis](https://travis-ci.com) as CI and pytest as a testing tool.

## Requirements
Python at least 3.7 version, installed [Pandoc](https://pandoc.org/) library and python-libraries from [requirements.txt](requirements.txt)

### Requirements installation examples:

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
Run in `src` directory
```shell script
flask run --host=127.0.0.2 --port=1234
```
Default arguments:

| Variable   | Value     |
|------------|-----------|
| host       | 127.0.0.1 |
| port       | 5000      |

The next endpoint returns supported conversion list in JSON format:
```http://host:port/get_available_conversions```

By the next endpoint you can change the file's format to <output->:
```http://host:port/convert/<output-type>```

The application tries to guess the given file's extension by themselves. 

You have to execute the conversion request like it's an user is sending file from input form with the name *file*. For instance, through the html form `<input type=file name=file>`

## Web client
At first, build the client JS files:
```shell script
cd src/client-web
.\gradlew runDceKotlinJs
```

Afterwards you can use `http://host:port/` page to upload and covert your files.

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