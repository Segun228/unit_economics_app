
# 📊 Unit Economics Telegram Bot (Microservice Architecture)

## 🛠️ Технологический стек

### 🔧 Backend
![Django](https://img.shields.io/badge/Django-4.2.23-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16.0-800000?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-9.10-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)

### 🤖 Bot
![Aiogram](https://img.shields.io/badge/Aiogram-3.21.0-00BFFF?logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

### 📊 Analytics
![ClickHouse](https://img.shields.io/badge/ClickHouse-Analytics-FF6B00?logo=clickhouse&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-231F20?logo=apachekafka&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3.1-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9.4-11557c?logo=python&logoColor=white)

### 🚀 Deployment
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?logo=python&logoColor=white)

### 🔐 Auth & API
![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?logo=fastapi&logoColor=white)
![REST](https://img.shields.io/badge/REST-API-FF6C37?logo=rest&logoColor=white)

## 🧭 Описание проекта

Этот проект — Telegram-бот с микросервисной архитектурой для **расчёта, визуализации и анализа юнит-экономики** бизнеса. Он предоставляет пользователям интерфейс на основе Telegram, через который можно загружать данные, создавать юниты, рассчитывать показатели и получать отчёты в текстовом, графическом или табличном виде.

Проект состоит из следующих компонентов:

- **Бот (Aiogram)** — фронт для пользователей
- **Бэкенд (Django + DRF)** — основная бизнес-логика, API, логгирование
- **Аналитика (FastAPI)** — Kafka-консьюмер и ClickHouse writer
- **ClickHouse** — высокопроизводительное хранилище логов
- **Kafka** — брокер сообщений между сервисами
- **Redis** — кэш + FSM-хранилище
- **Grafana / Tabix** — визуализация логов
- **PostgreSQL (NeonDB)** — персистентное хранилище бизнес-данных
- **Docker / Docker Compose** — инфраструктура

---

## ⚙️Технологии
```requirements.txt
  aiofiles==24.1.0
  aiogram==3.21.0
  aiohappyeyeballs==2.6.1
  aiohttp==3.12.15
  aiosignal==1.4.0
  annotated-types==0.7.0
  appnope==0.1.4
  asgiref==3.9.1
  asttokens==3.0.0
  async-timeout==5.0.1
  asyncio==4.0.0
  attrs==25.3.0
  certifi==2025.8.3
  click==8.1.8
  comm==0.2.3
  contourpy==1.3.0
  cycler==0.12.1
  debugpy==1.8.16
  decorator==5.2.1
  dj-database-url==3.0.1
  Django==4.2.23
  django-cors-headers==4.7.0
  djangorestframework==3.16.0
  djangorestframework_simplejwt==5.5.1
  drf-spectacular==0.28.0
  drf-spectacular-sidecar==2025.8.1
  dynaconf==3.2.11
  exceptiongroup==1.3.0
  executing==2.2.0
  fonttools==4.59.0
  frozenlist==1.7.0
  gunicorn==23.0.0
  hvac==2.3.0
  idna==3.10
  importlib_metadata==8.7.0
  importlib_resources==6.5.2
  inflection==0.5.1
  ipykernel==6.30.1
  ipython==8.18.1
  jedi==0.19.2
  jsonschema==4.25.0
  jsonschema-specifications==2025.4.1
  jupyter_client==8.6.3
  jupyter_core==5.8.1
  kiwisolver==1.4.7
  knox==0.1.14
  loguru==0.7.3
  magic-filter==1.0.12
  matplotlib==3.9.4
  matplotlib-inline==0.1.7
  multidict==6.6.3
  nest-asyncio==1.6.0
  numpy==2.0.2
  packaging==25.0
  pandas==2.3.1
  parso==0.8.4
  pexpect==4.9.0
  pillow==11.3.0
  platformdirs==4.3.8
  prompt_toolkit==3.0.51
  propcache==0.3.2
  psutil==7.0.0
  psycopg2-binary==2.9.10
  ptyprocess==0.7.0
  pure_eval==0.2.3
  pydantic==2.11.7
  pydantic_core==2.33.2
  Pygments==2.19.2
  PyJWT==2.10.1
  pyparsing==3.2.3
  python-dateutil==2.9.0.post0
  python-dotenv==1.1.1
  pytz==2025.2
  PyYAML==6.0.2
  pyzmq==27.0.1
  referencing==0.36.2
  requests==2.32.4
  rpds-py==0.26.0
  seaborn==0.13.2
  shortuuid==1.0.13
  six==1.17.0
  sqlparse==0.5.3
  stack-data==0.6.3
  tornado==6.5.2
  traitlets==5.14.3
  typing-inspection==0.4.1
  typing_extensions==4.14.1
  tzdata==2025.2
  uritemplate==4.2.0
  urllib3==2.5.0
  validators==0.35.0
  wcwidth==0.2.13
  yarl==1.20.1
  zipp==3.23.0
  aiofiles==24.1.0
  aiogram==3.21.0
  aiohappyeyeballs==2.6.1
  aiohttp==3.12.15
  aiosignal==1.4.0
  annotated-types==0.7.0
  async-timeout==5.0.1
  asyncio==4.0.0
  attrs==25.3.0
  certifi==2025.8.3
  charset-normalizer==3.4.3
  frozenlist==1.7.0
  idna==3.10
  magic-filter==1.0.12
  multidict==6.6.3
  propcache==0.3.2
  pydantic==2.11.7
  pydantic_core==2.33.2
  python-dotenv==1.1.1
  requests==2.32.4
  typing-inspection==0.4.1
  typing_extensions==4.14.1
  urllib3==2.5.0
  yarl==1.20.1
  aiofiles==24.1.0
  aiogram==3.21.0
  aiohappyeyeballs==2.6.1
  aiohttp==3.12.15
  aiosignal==1.4.0
  annotated-types==0.7.0
  anyio==4.10.0
  async-timeout==5.0.1
  asyncio==4.0.0
  attrs==25.3.0
  certifi==2025.8.3
  charset-normalizer==3.4.3
  click==8.1.8
  exceptiongroup==1.3.0
  fastapi==0.116.1
  frozenlist==1.7.0
  h11==0.16.0
  idna==3.10
  magic-filter==1.0.12
  multidict==6.6.3
  propcache==0.3.2
  pydantic==2.11.7
  pydantic_core==2.33.2
  python-dotenv==1.1.1
  requests==2.32.4
  sniffio==1.3.1
  starlette==0.47.2
  typing-inspection==0.4.1
  typing_extensions==4.14.1
  urllib3==2.5.0
  uvicorn==0.35.0
  yarl==1.20.1
```

---

## 📁 Структура проекта

```text
.
├── analytics
│   ├── app
│   │   ├── clickhouse_client.py
│   │   ├── init_clickhouse.py
│   │   ├── kafka_consumer.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── backend
│   ├── analitics
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── handlers
│   │   │   ├── __init__.py
│   │   │   ├── handlers.py
│   │   │   ├── report_handlers.py
│   │   │   ├── set_handlers.py
│   │   │   └── unit_handlers.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_unitmodel_fc.py
│   │   │   ├── 0003_unitmodel_name.py
│   │   │   ├── 0004_unitmodel_agr_unitmodel_rr_alter_unitmodel_model_set_and_more.py
│   │   │   └── 0005_alter_unitmodel_agr_alter_unitmodel_rr.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── backend
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── asgi.py
│   │   ├── authentication.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── dockerfile
│   ├── gunicorn.conf.py
│   ├── kafka_producer
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── events_schema.json
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── manage.py
│   ├── redis_cache
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── requirements.txt
│   ├── signals
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── tests.py
│   │   └── views.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   ├── __init__.py
│       │   ├── 0001_initial.py
│       │   └── 0002_user_test_group.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── bot
│   ├── __init__.py
│   ├── app
│   │   ├── database
│   │   ├── filters
│   │   │   └── IsAdmin.py
│   │   ├── handlers
│   │   │   ├── admin_handlers.py
│   │   │   ├── router.py
│   │   │   ├── templates.py
│   │   │   └── user_handlers.py
│   │   ├── kafka
│   │   │   └── utils.py
│   │   ├── keyboards
│   │   │   ├── answer_admin.py
│   │   │   ├── answer_user.py
│   │   │   ├── inline_admin.py
│   │   │   └── inline_user.py
│   │   ├── middlewares
│   │   │   └── antiflud.py
│   │   ├── requests
│   │   │   ├── delete
│   │   │   ├── files
│   │   │   ├── get
│   │   │   ├── helpers
│   │   │   ├── old requests
│   │   │   ├── post
│   │   │   ├── put
│   │   │   ├── sets
│   │   │   ├── units
│   │   │   └── user
│   │   └── states
│   │       └── states.py
│   ├── Dockerfile
│   ├── main_wh.py
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yaml
├── README.md
└── requirements.txt
```

---

## 🏗 Архитектура микросервисов

```
User → Telegram Bot → Django API → Kafka Topics → FastAPI Consumer → ClickHouse → Grafana/Tabix
```

### Контейнеры:

- **bot** — aiogram-бот, логирует действия через Kafka
- **backend** — Django + DRF, предоставляет REST API
- **analytics** — FastAPI Kafka-консьюмер
- **clickhouse** — база логов
- **tabix** — GUI-интерфейс к ClickHouse
- **grafana** — визуализация логов
- **redis** — FSM и кэш
- **kafka / zookeeper** — брокер и координатор
- **kafdrop** — UI для Kafka

---

## 📦 Переменные окружения

### .env.backend

- `SECRET_KEY` — Django ключ
- `DEBUG` — режим отладки
- `DATABASE_URL` — PostgreSQL (NeonDB)
- `BOOTSTRAP_SERVERS` — Kafka брокер
- `REDIS_HOST`, `REDIS_PORT` — Redis
- `BOT_TOKEN`, `BASE_URL`, `ADMINS` — Telegram-бот

### .env.analytics

- `KAFKA_BOT_TOPIC`, `KAFKA_BACKEND_TOPIC` — топики логов
- `CLICKHOUSE_*` — конфиг подключения к ClickHouse
- `BATCH_SIZE` — размер batch при записи логов

### .env.bot

Аналогично `.env.backend`, но адаптировано под использование внутри контейнера бота.

---

## 🔌 API: основные роуты (DRF)

API разбито на модули:

### 🔹 /api/sets/

- `GET` — список наборов моделей
- `POST` — создать ModelSet
- `/{set_id}/` — получить/изменить/удалить ModelSet
- `/{set_id}/units/` — получить/создать юниты в наборе

### 🔹 /api/sets/{set_id}/units/{unit_id}/

- `GET/PUT/PATCH/DELETE` — CRUD для конкретного юнита

### 🔹 /auth/user/

- `POST` — регистрация пользователя
- `GET` — список
- `/active/` — активные
- `/{telegram_id}/` — CRUD для пользователя по Telegram ID

### 🔹 /analitics/report/

- `/unit/{unit_id}/text|xlsx/` — текстовый/Excel отчёт по юниту
- `/set/{set_id}/text|xlsx|image/` — отчёты по набору

### 🔹 /analitics/evaluate/

- `/unit/{unit_id}/break_even_point/` — точка безубыточности

### 🔹 /analitics/cohort/

- `/unit/{unit_id}/` — когортный анализ юнита
- `/set/{set_id}/` — когортный анализ набора

---

# API Documentation 

## 🟢 Analytics Endpoints

| Method | Path | Описание | Параметры | Пример запроса | Пример ответа |
|--------|------|----------|-----------|----------------|---------------|
| POST | /analitics/cohort/set/{set_id}/ | Создание когорты для Set | set_id (path, int, required) | `POST /analitics/cohort/set/1/` | 200 No content |
| POST | /analitics/cohort/unit/{unit_id}/ | Создание когорты для Unit | unit_id (path, int, required) | `POST /analitics/cohort/unit/5/` | 200 No content |
| POST | /analitics/evaluate/unit/{unit_id}/break_even_point/ | Расчёт точки безубыточности для Unit | unit_id (path, int, required) | `POST /analitics/evaluate/unit/5/break_even_point/` | 200 No content |
| GET | /analitics/file/upload/ | Получить список загруженных файлов | — | `GET /analitics/file/upload/` | 200 No content |
| POST | /analitics/file/upload/ | Загрузка файла | — | `POST /analitics/file/upload/` (multipart/form-data) | 200 No content |
| POST | /analitics/report/set/{set_id}/image/ | Создание графического отчёта Set | set_id | `POST /analitics/report/set/1/image/` | 200 No content |
| POST | /analitics/report/set/{set_id}/text/ | Создание текстового отчёта Set | set_id | `POST /analitics/report/set/1/text/` | 200 No content |
| POST | /analitics/report/set/{set_id}/xlsx/ | Создание Excel отчёта Set | set_id | `POST /analitics/report/set/1/xlsx/` | 200 No content |
| POST | /analitics/report/unit/{unit_id}/text/ | Создание текстового отчёта Unit | unit_id | `POST /analitics/report/unit/5/text/` | 200 No content |
| POST | /analitics/report/unit/{unit_id}/xlsx/ | Создание Excel отчёта Unit | unit_id | `POST /analitics/report/unit/5/xlsx/` | 200 No content |

---

## 🟢 API Endpoints (Sets / Units)

### Sets

| Method | Path | Описание | Параметры | Body | Пример запроса | Пример ответа |
|--------|------|----------|-----------|------|----------------|---------------|
| GET | /api/sets/ | Список всех Set | — | — | `GET /api/sets/` | `[{"id":1,"name":"Set A","description":"Описание набора","created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}]` |
| POST | /api/sets/ | Создание Set | — | JSON `ModelSet` | `POST /api/sets/ {"name":"Set A","description":"Описание набора"}` | `{"id":1,"name":"Set A","description":"Описание набора","created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}` |
| GET | /api/sets/{set_id}/ | Получить Set | set_id | — | `GET /api/sets/1/` | `{"id":1,"name":"Set A","description":"Описание набора","created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z","units":[]}` |
| PUT | /api/sets/{set_id}/ | Полное обновление Set | set_id | JSON `ModelSet` | `PUT /api/sets/1/ {"name":"Set B","description":"Новый набор"}` | `{"id":1,"name":"Set B","description":"Новый набор","created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:00:00Z"}` |
| PATCH | /api/sets/{set_id}/ | Частичное обновление Set | set_id | JSON `PatchedModelSet` | `PATCH /api/sets/1/ {"description":"Обновлённое описание"}` | `{"id":1,"name":"Set B","description":"Обновлённое описание","created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:10:00Z"}` |
| DELETE | /api/sets/{set_id}/ | Удаление Set | set_id | — | `DELETE /api/sets/1/` | 204 No content |

### Units (внутри Set)

| Method | Path | Описание | Параметры | Body | Пример запроса | Пример ответа |
|--------|------|----------|-----------|------|----------------|---------------|
| GET | /api/sets/{set_id}/units/ | Список Unit для Set | set_id | — | `GET /api/sets/1/units/` | `[{"id":5,"name":"Unit 1","users":100,"customers":50,"AVP":200,"APC":150,"TMS":30,"COGS":500,"COGS1s":450,"FC":1000,"RR":1.5,"AGR":0.2,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:00:00Z"}]` |
| POST | /api/sets/{set_id}/units/ | Создание Unit в Set | set_id | JSON `UnitModel` | `POST /api/sets/1/units/ {"name":"Unit 1","users":100,"customers":50,"AVP":200,"APC":150,"TMS":30,"COGS":500,"COGS1s":450,"FC":1000,"RR":1.5,"AGR":0.2}` | `{"id":5,"name":"Unit 1","users":100,"customers":50,"AVP":200,"APC":150,"TMS":30,"COGS":500,"COGS1s":450,"FC":1000,"RR":1.5,"AGR":0.2,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:00:00Z"}` |
| GET | /api/sets/{set_id}/units/{unit_id}/ | Получить Unit | set_id, unit_id | — | `GET /api/sets/1/units/5/` | `{"id":5,"name":"Unit 1","users":100,"customers":50,"AVP":200,"APC":150,"TMS":30,"COGS":500,"COGS1s":450,"FC":1000,"RR":1.5,"AGR":0.2,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:00:00Z"}` |
| PUT | /api/sets/{set_id}/units/{unit_id}/ | Полное обновление Unit | set_id, unit_id | JSON `UnitModel` | `PUT /api/sets/1/units/5/ {"name":"Unit 1 Updated","users":120,"customers":60,"AVP":210,"APC":160,"TMS":35,"COGS":520,"COGS1s":470,"FC":1050,"RR":1.6,"AGR":0.25}` | `{"id":5,"name":"Unit 1 Updated","users":120,"customers":60,"AVP":210,"APC":160,"TMS":35,"COGS":520,"COGS1s":470,"FC":1050,"RR":1.6,"AGR":0.25,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T02:00:00Z"}` |
| PATCH | /api/sets/{set_id}/units/{unit_id}/ | Частичное обновление Unit | set_id, unit_id | JSON `PatchedUnitModel` | `PATCH /api/sets/1/units/5/ {"users":130}` | `{"id":5,"name":"Unit 1 Updated","users":130,"customers":60,"AVP":210,"APC":160,"TMS":35,"COGS":520,"COGS1s":470,"FC":1050,"RR":1.6,"AGR":0.25,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T02:10:00Z"}` |
| DELETE | /api/sets/{set_id}/units/{unit_id}/ | Удаление Unit | set_id, unit_id | — | `DELETE /api/sets/1/units/5/` | 204 No content |

---

## 🟢 Auth Endpoints

| Method | Path | Описание | Параметры | Body | Пример запроса | Пример ответа |
|--------|------|----------|-----------|------|----------------|---------------|
| GET | /auth/user/ | Список всех пользователей | — | — | `GET /auth/user/` | `[{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":true,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}]` |
| POST | /auth/user/ | Создание пользователя | — | JSON `User` | `POST /auth/user/ {"telegram_id":"123456","is_alive":true}` | `{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":true,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}` |
| GET | /auth/user/{telegram_id}/ | Получить пользователя | telegram_id | — | `GET /auth/user/123456/` | `{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":true,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}` |
| PUT | /auth/user/{telegram_id}/ | Полное обновление пользователя | telegram_id | JSON `User` | `PUT /auth/user/123456/ {"is_alive":false}` | `{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":false,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:00:00Z"}` |
| PATCH | /auth/user/{telegram_id}/ | Частичное обновление пользователя | telegram_id | JSON `PatchedUser` | `PATCH /auth/user/123456/ {"is_alive":true}` | `{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":true,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T01:10:00Z"}` |
| DELETE | /auth/user/{telegram_id}/ | Удаление пользователя | telegram_id | — | `DELETE /auth/user/123456/` | 204 No content |
| GET | /auth/user/active/ | Список активных пользователей | — | — | `GET /auth/user/active/` | `[{"id":1,"telegram_id":"123456","is_admin":true,"is_alive":true,"created_at":"2025-08-29T00:00:00Z","updated_at":"2025-08-29T00:00:00Z"}]` |

---

## 🟢 Cache Endpoints

| Method | Path | Описание | Пример запроса | Пример ответа |
|--------|------|----------|----------------|---------------|
| GET | /cache/ | Получить кеш | `GET /cache/` | 200 No content |
| POST | /cache/ | Создать/обновить кеш | `POST /cache/` | 200 No content |


⸻

📘 Пояснения:
	•	set/{set_id} — операции с наборами юнитов.
	•	unit/{unit_id} — расчёты по отдельным юнитам.
	•	cohort/... — когортный анализ.
	•	evaluate/.../break_even_point — расчёт точки безубыточности.
	•	report/... — генерация текстовых, xlsx и графических отчётов.
	•	file/upload/ — загрузка и получение файлов (возможно, загруженных пользователем шаблонов или файлов отчётов).

---
## 🔐 Авторизация

Пользователь создаётся автоматически по Telegram ID при первом взаимодействии с ботом.  
Идентификация производится на бэкенде и логируется через Kafka.

---

## 🧠 Аналитика (Kafka + FastAPI + ClickHouse)

Сервис `analytics` подписан на Kafka-топики (`bot_logs_topic`, `logs_topic`), обрабатывает сообщения и записывает в ClickHouse.  

Используется асинхронный ClickHouse-клиент + парсинг схемы сообщений.

---

## 📊 Визуализация

- **Grafana** подключается к ClickHouse и отображает:
  - кол-во уникальных пользователей
  - распределение по action (start, register, set_value, report и т.д.)
  - временные ряды активности

- **Tabix** — альтернатива Grafana для сырых SQL-запросов

---

## 📈 Пример логов

```json
{
  "telegram_id": 7984483686,
  "action": "register",
  "source": "command",
  "payload": "start"
}
```

Все действия логируются продюсерами (бот / бекенд) и доступны для построения отчётов.

---

## 🐳 Как запустить

```bash
git clone ...
cp .env.template .env.bot / .env.backend / .env.analytics
docker-compose up --build
```

После запуска:

- `localhost:3000` — Grafana
- `localhost:8124` — Tabix
- `localhost:9001` — Kafdrop

---

## 🧪 Тестирование

- Бэкенд покрыт unit-тестами: `python manage.py test`
- Kafka и ClickHouse логика — вручную через pytest / Grafana
- Возможна интеграция с GitHub Actions

---

## 📌 Возможности

- [x] Создание юнитов и наборов
- [x] Расчёт юнит-экономики
- [x] Генерация Excel, текстовых и графических отчётов
- [x] Когортный и BEP-анализ
- [x] Kafka-логирование действий
- [x] Визуализация в Grafana

---

## 📍 TODO

- [ ] CI/CD pipeline
- [ ] Автоматическое масштабирование ClickHouse
- [ ] Поддержка мультиюзерных проектов


---

## 👤 Автор

- Telegram: [@dianabol_metandienon_enjoyer](https://t.me/dianabol_metandienon_enjoyer)
- Email: segunperkele@gmail.com
- GitHub: github.com/Segun228

