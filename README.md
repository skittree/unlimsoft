# Тестовое задание на _Python_-программиста

## Ответы
1. Высказать идеи рефакторинга файла `external_requests.py`
- Проблемы `external_requests.py`:
   - слишком много описаний к функциям, нам вовсе необязательно подписывать/документировать перегруженный `__init__`, например;
   - необязательно выделять код в отдельную функцию если он не будет использоваться повторно, некоторые функции можно "слепить";
   - идет повторение методов `get_weather_url` и `send_request` в классах `GetWeatherRequest` и `CheckCityExisting`, также повторно инициализируется сессия `requests`;
   - ключ доступа в коде
- Идеи рефакторинга:
   - оставить описания только у функций (и возможно у класса), которыми будем пользоваться мы;
   - объединить функции `get_weather_url` с `send_request`; `get_weather_from_response` с `get_weather`;
   - объединить два класса в один, так мы можем избавиться от повторения и использовать методы класса в зависимости от потребности;
   - убрать ключ доступа из кода, доставать из env переменных
   - при нетрепетности к названию функции, возможно вовсе свести все к одной функции `get_weather` для проверки существования и для получения температуры
1. Описать возможные проблемы при масштабировании проекта
- Возможные проблемы при масштабировании:
  - Файл `main.py` станет очень громоздким, так как на данный момент в нем происходит обработка запросов всех сущностей.
  - По тому же поводу, отсутствие стандартизированной архитектуры эндпойнтов по REST приведёт к путанице. Намного интуитивнее создать пользователя с помощью `POST /users/`, нежели подбором названия конкретного эндпоинта (`/register-user/`).
  - В зависимости от количества сущностей, также можно разбить `models.py` на более модулярную систему описывания Pydantic моделей (например, `CreatePicnicModel` в `models/picnics.py`).
  - Также, возможно выделить функционал из эндпойнтов в отдельный `crud.py` файл, чтобы файл с эндпойнтами был более читабельный.
  - В приложении не используются Pydantic модели для всех запросов на вход и выход, что ограничивает возможности приложения для парсинга/валидации данных, а также не предоставляет подробные данные автоматической документации Swagger. Валидацию придётся описывать в методах эндпоинтов, что приведёт к дополнительной громоздкости.
  - Также, рекомендуется использовать параметр `response_model` всех декораторов `@app` для документирования данных, проверки и преобразования с фильтрацией выходных данных в соответствии с объявленным типом.
  - При масштабировании БД, необходимо поставить ограничения по количеству данных в GET запросах. Неограниченные запросы могут быстро перегрузить систему.
  - Можно перейти на асинхронный вариант функций для повышения производительности (в частности CRUD). Зависит от потребностей приложения.


## Невыполненные задания
  - Сделать логирование в файл, который не будет очищаться после перезапуска в докере
  - Описать правильную архитектуру для проекта

## Тестирование
```
> pytest tests.py -vv

tests.py::test_create_city1 PASSED
tests.py::test_create_city2 PASSED
tests.py::test_create_city2_lowercase PASSED
tests.py::test_create_city3_error PASSED
tests.py::test_create_nofield PASSED
tests.py::test_create_city3 PASSED
tests.py::test_get PASSED
tests.py::test_get_city3 PASSED
tests.py::test_get_city3_wrongfilter PASSED
tests.py::test_get_empty_userlist PASSED
tests.py::test_create_user1 PASSED
tests.py::test_create_user_nofield PASSED
tests.py::test_create_user2_nofield PASSED
tests.py::test_create_user2 PASSED
tests.py::test_create_user3 PASSED
tests.py::test_get_userlist PASSED
tests.py::test_get_filtered_userlist PASSED
tests.py::test_get_empty PASSED
tests.py::test_create_picnic_error PASSED
tests.py::test_create_picnic1 PASSED
tests.py::test_create_nofield1_picnic2 PASSED
tests.py::test_create_nofield2_picnic2 PASSED
tests.py::test_get_without_users1 PASSED
tests.py::test_create_picnic2 PASSED
tests.py::test_get_without_users_both PASSED
tests.py::test_get_without_users2 PASSED
tests.py::test_register1_picnic1 PASSED
tests.py::test_register2_picnic1 PASSED
tests.py::test_get_both PASSED
tests.py::test_get_by_time PASSED

30 passed in 8.31s
```
