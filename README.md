# English Trainer
Backend platform for English training

## .env
Create `.env` file
- DB_URL - str, url for db. For example, `sqlite:///db.db`
- POSTGRES_USER - str
- POSTGRES_PASSWORD - str

Create `db/.env` file
- POSTGRES_USER - str
- POSTGRES_PASSWORD - str

## Test
```shell
docker-compose exec -it web python -m pytest --cov="."
```

## Docker-compose
```shell
docker-compose up --build
```
```shell
docker-compose exec web alembic upgrade head
```

## New migration
```shell
docker-compose exec web alembic revision --autogenerate -m "message"
```
