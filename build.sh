#!/usr/bin/env bash
# Установка UV и создание окружения
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.cargo/env"
source ~/.local/bin/env
uv venv .venv

# Установка зависимостей через UV (аналог `uv sync`)
uv pip install -r pyproject.toml

# Применение миграций и сбор статики
.venv/bin/python manage.py migrate --noinput

# Сделать gunicorn исполняемым
find /opt/render/project/src/.venv/bin -type f -executable -exec chmod +x {} \;