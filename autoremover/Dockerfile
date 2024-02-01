FROM python:3.11.6-slim-bullseye

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get -y install tk-dev

ENV DJANGO_SECRET_KEY="django-insecure-c1vs35l$w62!rq2dt8g!2&1at9f&hyowg2)7s((r*lyij+zftw"
ENV DATABASE_NAME="postgres"
ENV DATABASE_USER="postgres"
ENV DATABASE_PASSWORD="Pfors111*__"
ENV DATABASE_HOST="db.hjehxvufdkhjofcblfga.supabase.co"
ENV DATABASE_PORT="5432"

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["python3", "manage.py", "makemigrations", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "migrate", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
