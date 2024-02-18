# Описание
Сервис обрабатывает реферальные ссылки. Позволяет создавать / удалять ссылку по одной для каждого пользователя.
Также позволяет отправлять их по почте, указанной пользователем и регистрироваться другим пользователям по 
реферальной ссылке.

При создании реферальной ссылке указывается срок жизни в секундах. Спустя это время ссылка становиться недоступной.

Технологии
- Poetry
- FastAPI
- Uvicorn
- Docker
- Redis
- Postgres
- SQLAlchemy
- Alembic

# Установка

1. Клонируйте репозиторий с помощью SSH:
```bash
git clone git@github.com:pandenic/referral_link_generator.git
```

2. Перейдите в каталог проекта:
```bash
cd referral_link_generator
```

3. Создайте файл .env в корне проекта, используя шаблон /infra/.env.example


4. Запустите docker compose:
```bash
docker compose up -d
```

- Сервер запускается по адресу http://localhost/. 
- Swagger по адресу: http://localhost/docs/.
- Redoc по адресу: http://localhost/redoc/.

# Примеры запросов для тестирования:

### Postman collection at `infra/Referral Generator.postman_collection.json`
- Рекомендуется запускать в порядку перечисления эндпоинтов.

### Получение токена /auth/jwt/login

```bash
curl -X 'POST' \
  'http://localhost/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=q%40q.com&password=qweqwe123!&scope=&client_id=&client_secret='
```

### Деактивация токена `/auth/jwt/logout`

```bash
curl -X 'POST' \
  'http://localhost/auth/jwt/logout' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -d ''
```

### Регистрация нового пользователя `/auth/register`

```bash
curl -X 'POST' \
  'http://localhost/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "[EMAIL]",
  "password": "[PASSWORD]",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "referral_code": "[REFERRAL CODE]"
}'
```

### Создание / обновление реферального кода `/referral`

```bash
curl -X 'POST' \
  'http://localhost/referral/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -H 'Content-Type: application/json' \
  -d '{
  "lifetime": [IN SECONDS]
}'
```

### Удаление реферального кода `/referral`
```bash
curl -X 'DELETE' \
  'http://localhost/referral/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]'
```

### Отправка реферального кода на почту пользователя `/referral/mail-referral-code`
```bash
curl -X 'POST' \
  'http://localhost/referral/mail-referral-code' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -d ''
```

### Получение списка реферало по id реферера `/referral/{referrer_id}`
```bash
curl -X 'GET' \
  'http://localhost/referral/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]'
```

---

# Description
The service processes referral links. Allows you to create / delete a link one by one for each user.
Also allows you to send them to the mail specified by the user and to register other users on the 
referral link.

When creating a referral link, the lifetime of the link is specified in seconds. After this time the link becomes deactivated.

Technologies
- Poetry
- FastAPI
- Uvicorn
- Docker
- Redis
- Postgres
- SQLAlchemy
- Alembic

# Installation

1. Clone the repository using SSH:
```bash
git clone git@github.com:pandenic/referral_link_generator.git
```

2. Navigate to the project directory:
```bash
cd referral_link_generator
```

3. Create an .env file in the project root using the /infra/.env.example template


4. Run docker compose:
```bash
docker compose up -d
```

- The server starts at http://localhost/. 
- Swagger at: http://localhost/docs/.
- Redoc at: http://localhost/redoc/.

### Example queries for testing:

### Postman collection at `infra/Referral Generator.postman_collection.json`.
- It is recommended to run in order of endpoints.

### Receive token /auth/jwt/login

```bash
curl -X 'POST' \.
  'http://localhost/auth/jwt/login' \
  -H 'accept: application/json' \.
  -H "Content-Type: application/x-www-form-urlencoded \
  -d 'grant_type=&username=q%40q.com&password=qweqwe123!&scope=&client_id=&client_secret='
```

### Deactivate token `/auth/jwt/logout`

```bash
curl -X 'POST' \.
  'http://localhost/auth/jwt/logout' \
  -H 'accept: application/json' \.
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -d ''
```

### Register a new user `/auth/register`

```bash
curl -X 'POST' \.
  'http://localhost/auth/register' \
  -H 'accept: application/json' \.
  -H 'Content-Type: application/json'\
  -d '{
  { "email": "[EMAIL]"
  "password": "[PASSWORD]",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "referral_code": "[REFERRAL CODE]"
}'
```

### Create / update referral code `/referral`

```bash
curl -X 'POST' \.
  'http://localhost/referral/' \
  -H 'accept: application/json' \.
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -H 'Content-Type: application/json' \.
  -d '{
  { "lifetime": [IN SECONDS]
}'
```

### Delete referral code `/referral`
```bash
curl -X 'DELETE' \.
  ``http://localhost/referral/'' \
  -H 'accept: application/json' \.
  -H "Authorization: Bearer [TOKEN FROM LOGIN]
```

### Send referral code to user's email `/referral/mail-referral-code`
```bash
curl -X 'POST' \.
  'http://localhost/referral/mail-referral-code' \
  -H 'accept: application/json' \.
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]' \
  -d ''
```

### Get list of referrals by referrer id `/referral/{referrer_id}``
```bash
curl -X 'GET' \.
  'http://localhost/referral/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'accept: application/json' \\.
  -H 'Authorization: Bearer [TOKEN FROM LOGIN]'
```