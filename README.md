## Запустить проект

Сначала вам нужно скопировать файл .env-local в .env 

```bash
cp .env-local .env
```

заполнить .env нужными данными

```
POSTGRES_USER=loremipsum
POSTGRES_PASSWORD=loremipsum
POSTGRES_DB=loremipsum
SECRET=loremipsum
```

Запустите проект 

```
docker-compose up -d --build
```