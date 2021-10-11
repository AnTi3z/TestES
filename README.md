# Тестовое задание для стажера

### Ссылка на тестовое задание
https://freezing-helicopter-7fb.notion.site/67777c95bdbe4e59856c59b707349f2d

### Инструкция по запуску тестового сервиса
1. git clone git://github.com/AnTi3z/TestES.git 
2. cd TestES 
3. docker-compose build 
4. docker-compose up 

### Примеры запросов:  
"GET 127.0.0.1:5000/search?q=Текст" - поиск записей по тексту   
"DELETE 127.0.0.1:5000/1043" - удалить запись с id 1043
см. документацию https://app.swaggerhub.com/apis-docs/AnTi3z/TestES/1.0.0 или в файле docs.json
