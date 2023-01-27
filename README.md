# JabreKh

## Deploy for Development

To deploy the server for development, run the following command.

```bash
docker compose up -d --build
```

In this case, the server will be available at <http://localhost:8000> with live delivery of code changes of django and react. Nginx is not used in this case.

## Deploy for Production

```bash
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

## References

- <https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/>

## TODOs

- CSRF Allowed Hosts
