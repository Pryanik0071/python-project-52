app-run:
	uv run manage.py runserver

locales-add:
	uv run manage.py makemessages -a

locales-compile:
	uv run manage.py compilemessages

app-migrations:
	uv run manage.py makemigrations

app-migrate:
	uv run manage.py migrate