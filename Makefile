#установка заисимостей
install:
	uv sync

#запуск в режиме отладки
dev:
	uv run python manage.py runserver

# скачиваем uv и запускаем команду установки зависимостей
build:
	./build.sh

# запуск на Render
render-start:
	gunicorn task_manager.wsgi

# миграции БД
migrate:
	uv run python manage.py migrate

# сборка статики
collectstatic:
	uv run python manage.py collectstatic --noinput

shell:
	uv run python manage.py shell_plus

lint:
	uv run ruff check task_manager

lint-fix:
	uv run ruff check --fix task_manager

test:
	uv run manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage xml

check:
	uv run ruff check task_manager
	uv run python manage.py test
