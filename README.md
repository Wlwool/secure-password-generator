# Secure Password Generator

[![Tests](https://github.com/Wlwool/secure-password-generator/actions/workflows/tests.yml/badge.svg)](https://github.com/Wlwool/secure-password-generator/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Веб-приложение для генерации надёжных паролей на Flask. Пароли создаются модулем `secrets` из стандартной библиотеки Python, который предназначен для криптографических задач. Приложение упаковано в Docker и работает на Render.

**Демо:** https://flask-docker-app-nhwy.onrender.com/

> Демо размещено на бесплатном тарифе Render: после 15 минут без запросов сервис засыпает, поэтому первое открытие может занять заметное время.

---

## Возможности

- Длина пароля от 4 до 32 символов.
- Выбор наборов символов: заглавные и строчные буквы, цифры, спецсимволы.
- Каждый выбранный тип символов гарантированно встречается в пароле хотя бы один раз.
- Оценка надёжности пароля. Это эвристика по длине и разнообразию символов, а не расчёт энтропии.
- Кнопка "Сгенерировать ещё" создаёт новый пароль с теми же параметрами.
- Понятные сообщения об ошибках при неверной длине.


---

## Технологии

- **Python 3.13**, **Flask**, **gunicorn**
- **uv** для управления зависимостями
- **pytest** для тестов, **ruff** для линтинга и форматирования, **mypy** для проверки типов
- **Docker**, **GitHub Actions**, **Render**(а качестве демо)

---

## Запуск в Docker

Нужны Docker и Git.

```bash
git clone https://github.com/Wlwool/secure-password-generator.git
cd secure-password-generator
docker build -t secure-password-generator .
docker run --rm -p 8000:8000 secure-password-generator
```

Приложение откроется по адресу http://localhost:8000.

Порт внутри контейнера задаётся переменной `PORT` (по умолчанию 8000):

```bash
docker run --rm -e PORT=10000 -p 10000:10000 secure-password-generator
```

### Docker Compose

```bash
docker compose up --build
```

Остановка: `Ctrl+C`, затем `docker compose down`.

---

## Локальная разработка

Нужны Python 3.12+ и [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run flask --app flask_app.app run --port 5001
```

Приложение откроется по адресу http://127.0.0.1:5001.

### Проверки

Те же команды выполняет CI при каждом пуше и pull request:

```bash
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest -q
```

---

## Структура проекта

```text
flask_app/
  app.py              логика генерации и маршруты
  templates/          base.html, home.html, password.html
  static/styles.css   стили
tests/
  test_app.py         тесты эндпоинтов и генератора
Dockerfile            образ на python:3.13-slim, запуск через gunicorn
docker-compose.yml
pyproject.toml        зависимости и настройки ruff, mypy, pytest
uv.lock               зафиксированные версии зависимостей
.github/workflows/    CI
```

---

## Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).