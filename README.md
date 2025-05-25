# About:

**Task Manager – система управления задачами, подобная http://www.redmine.org/. Она позволяет ставить задачи, назначать исполнителей и менять их статусы. Для работы с системой требуется регистрация и аутентификация:**

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pryanik0071/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pryanik0071/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Pryanik0071_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Pryanik0071_python-project-52)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Pryanik0071_python-project-52&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Pryanik0071_python-project-52)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Pryanik0071_python-project-52&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Pryanik0071_python-project-52)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Pryanik0071_python-project-52&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Pryanik0071_python-project-52)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Pryanik0071_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Pryanik0071_python-project-52)

## ENV

**Создайте файл .env в корневой папке и добавьте следующие переменные:**

```dotenv
DEBUG=True
SECRET_KEY="some-secret-key"
DATABASE_URL="postgres://postgres:postgres@postgres:5432/postgres"
ENVIRONMENT="dev"
```

**См. пример в .env.examples**

---

## Dependencies

```
"django-bootstrap5>=24.3",
"django-filter>=25.1",
"django>=5.1.6",
"python-dotenv>=1.1.0",
"dj-database-url>=2.3.0",
"psycopg2-binary>=2.9.10",
"gunicorn>=23.0.0",
"whitenoise[brotli]>=6.9.0",
"pytest>=8.3.5",
"pytest-django>=4.11.1",
```

## Установка и использование UV

<details>
<summary>📦 Способы установки UV</summary>

### 1. Установка через автономные установщики (рекомендуется)

**Для macOS и Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Для Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Установка через PyPI (альтернативный способ)
```bash
pip install uv
```

### Обновление UV
После установки вы можете обновить UV до последней версии:
```bash
uv self update
```

🔗 Подробнее об установке: [Официальная документация](https://docs.astral.sh/uv/getting-started/installation/)
</details>

---

<details>
<summary>🚀 Основные команды UV</summary>

### Управление Python-окружением

**Установка конкретной версии Python:**
```bash
uv python install 3.13  # Установит Python 3.13
```

### Управление зависимостями

**Синхронизация зависимостей проекта:**
```bash
uv sync  # Аналог pip install + pip-compile
```

**Запуск команд в окружении проекта:**
```bash
uv run <COMMAND>  # Например: uv run manage.py migrate
```

**Запуск Django-сервера:**
```bash
uv run manage.py runserver  # Альтернатива python manage.py runserver
```
</details>

---
