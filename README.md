# DocumentConverter
[![Build Status](https://travis-ci.com/LoDThe/DocumentConverter.svg?branch=master)](https://travis-ci.com/LoDThe/DocumentConverter)
[![codecov](https://codecov.io/gh/LoDThe/DocumentConverter/branch/master/graph/badge.svg)](https://codecov.io/gh/LoDThe/DocumentConverter)
    
DocumentConverter представляет из себя реализацию http-сервиса для конвертации документов из одного формата в другой.

Конвертация осуществляется с помощью посылки POST-запроса, содержащего файл, по url 

`http://<server-name>:<server-port>/convert/<output-type>`

Подробнее о задании для курса *Методы разработки программного обесечения* можно прочитать [здесь](https://docs.google.com/document/d/1lDirPrxqhrIkkDXW3sbIWr6cRhFdlra0rSmd0RHjH8s/edit)

Для создания сервиса выбран фреймворк [Flask](https://palletsprojects.com/p/flask/), библиотека для конвертации файлов - [Pandoc](https://pandoc.org/)

Также используется [Travis](https://travis-ci.com) в качестве CI и pytest для тестирования.

## Требования
Python версии не менее 3.7, установленную библиотеку [Pandoc](https://pandoc.org/) и python-библиотеки из файла [requirements.txt](requirements.txt)

Пример установки библиотек:

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

## Использование
Запуск в папке `src`
```shell script
flask run --host=127.0.0.2 --port=1234
```
Значения по умолчанию:

| Переменная | Значение  |
|------------|-----------|
| host       | 127.0.0.1 |
| port       | 5000      |

Запускает приложение с возможностью отправлять POST-запрос, содержащего файл, по url 
```http://host:port/convert/<output-type>```

Формат запрос должен быть аналогичен формату отсылки файла через форму с именем *file*. Например, через форму вида `<input type=file name=file>`

Отослать файл для конвертации можно по url `http://host:port/<output-type>`
## Поддерживаемые варианты конвертации

| Входной формат |      Выходные форматы      | 
|----------------|----------------------------|
| html           |html, markdown, plain       |
| markdown       |markdown, html, plain       |
| docx           |docx, html, markdown, plain |
| odt            |odt, html, markdown, plain  |

## To-do
- [x] Запускающееся приложение
- [x] Сделать тесты
  - [x] Unit тесты
  - [x] Интеграционные тесты
- [x] Использовать codecov
- [x] Использовать Travis
- [ ] Добавить поддержку большего числа форматов
- [x] Исправить идентификацию формата получаемового файла