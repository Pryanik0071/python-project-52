app-run:
	uv run manage.py runserver 127.0.0.1:8000

locales-add:
	uv run manage.py makemessages -a

locales-compile:
	uv run manage.py compilemessages

migrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

build:
	./build.sh

render-start:
	.venv/bin/gunicorn task_manager.wsgi:application --workers=3 --timeout 120

install:
	uv sync
