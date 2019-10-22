# DocumentConverter

DocumentConverter представляет из себя реализацию http-сервиса для конвертации документов из одного формата в другой.

Конвертация осуществляется с помощью посылки POST-запроса, содержащего файл, по url `http://<server-name>:<server-port>/convert/<output-type>`

Подробнее о задании для курса *Методы разработки программного обесечения* можно прочитать [здесь](https://docs.google.com/document/d/1lDirPrxqhrIkkDXW3sbIWr6cRhFdlra0rSmd0RHjH8s/edit)

Для создания сервиса выбран фреймворк [Flask](https://palletsprojects.com/p/flask/), библиотека для конвертации файлов - [Pandoc](https://pandoc.org/)

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
```shell script
python -m flask run --host=127.0.0.2 --port=1234
```
Значения по умолчанию:

| Переменная | Значение  |
|------------|-----------|
| host       | 127.0.0.1 |
| port       | 5000      |

Запускает приложение с возможностью отправлять POST-запрос, содержащего файл, по url 
```http://host:port/convert/<output-type>```

Формат запрос должен быть аналогичен формату отсылки файла через форму с именем *file*. Например, через форму вида `<input type=file name=file>`


## Поддерживаемые форматы

| html | docx | odt | markdown |
|------|------|-----|----------|

## To-do
- [x] Запускающееся приложение
- [ ] Сделать тесты
- [ ] Использовать Travis
- [ ] Добавить поддержку большего числа форматов
- [ ] Исправить идентификацию формата получаемового файла