#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh

uv pip install -r pyproject.toml

# здесь добавьте все необходимые команды для установки вашего проекта
# команду установки зависимостей, сборки статики, применения миграций и другие
.venv/bin/python manage.py migrate --noinput