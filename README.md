## Варианты запуска
- `bash run.sh`
- `docker compose up --build`

## Посмотреть результат
- `http://0.0.0.0:8000/top` (результат будет после того, как запустится etl контейнер, и спустя 10 сек отработает крона)

## Переменные окружения [.env](.env) 
(Для того, чтобы запустить контейнеры, все переменные уже прописаны)
- `POSTS_URL_API` - url api для постов
- `CRON_FREQ_IN_SEC` - периодичность cron
- `POSTGRES_HOST` - название хоста db
- `POSTGRES_PORT` - порт db
- `POSTGRES_DB` - название db
- `POSTGRES_USER` - логин юзера
- `POSTGRES_PASSWORD` - пароль
- `SQLALCHEMY_ECHO_FLAG` - нужны ли расширенные логи SQLALCHEMY

## Дополнительные задания
1. Легкий дашборд
    - [api/main.py](api/main.py)
    - [api/routers/get_top_users.py](api/routers/get_top_users.py)
2. Docker Compose: `db` + `etl` + `api`
    - [docker-compose.yml](docker-compose.yml)
3. Юнит-тест