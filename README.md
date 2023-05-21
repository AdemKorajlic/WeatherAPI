# WeatherAPI

WeatherBit API Key: 1d9546c0a8d644719d74176fec92b35a (or use your own API key from other API provider)

Install pip and dependencies:

(IMPORTANT: use latest version of pip, CMD run: python.exe -m pip install --upgrade pip)
-pip install python
-pip install django
-pip install djangorestframework
-pip install requests
-pip install logging 
-pip install django_http_basic_auth
-pip install django-rest-swagger
-pip install drf-yasg django-filter         
-pip install pyyaml   

Run next commands to run the server:

-djangoenv/Scripts/activate
-python manage.py runserver

First you have to login:

http://127.0.0.1:8000/admin/login/?next=/admin/
User credentials:
Username: admin
Password: admin

After logging in you can access to the rest of the urls:

http://localhost:8000/api/weather/current/?location={location} to retrieve the current weather conditions. (http://127.0.0.1:8000/api/weather/current/?location=Sarajevo)
http://localhost:8000/api/weather/forecast/?location={location} to retrieve the weather forecast. (http://127.0.0.1:8000/api/weather/forecast/?location=Sarajevo)
http://localhost:8000/api/weather/history/?location={location}&start={start_date}&end={end_date} to retrieve the historical weather data.
(History is currently not allowed since the API is a free version, you can check it by going to: http://127.0.0.1:8000/api/weather/history/?location=Sarajevo&start=2023-05-01&end=2023-05-10)

Postman json file is located within the WeatherApp folder.
To access Swagger UI API Documentation go to the next url: http://localhost:8000/swagger/
