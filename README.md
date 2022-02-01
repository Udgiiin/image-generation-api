## Запустить проект

Сначала вам нужно скопировать файл .example-env в .env 

```bash
cp .example-env .env
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