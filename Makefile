app-run:
	uv run manage.py runserver

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
	gunicorn task_manager.wsgi

install:
	uv sync
