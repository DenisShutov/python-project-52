### Hexlet tests and linter status:
[![Actions Status](https://github.com/DenisShutov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DenisShutov/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DenisShutov_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DenisShutov_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DenisShutov_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DenisShutov_python-project-52)

# Task Manager
[Project Reference](https://python-project-52-ijix.onrender.com/)

Task Manager is an educational project from Hexlet developed with Django. It allows you to create, edit, delete tasks, and assign statuses, performers, and labels.

## Features

- **Authentication**: registration, login, logout
- **User management**: view, edit, delete profile
- **Status management**: CRUD operations for task statuses
- **Label management**: CRUD operations for labels
- **Task management**: create, edit, delete, view tasks
- **Task filtering**: by status, performer, labels, only my tasks
- **Error handling**: integration with Rollbar

> ⚠️ **Note**: The service is hosted on [Render.com](https://render.com) with a **temporary database**.  
> The data may be reset periodically.

### Local setup
```bash
# 1. Clone the repository
git clone https://github.com/DenisShutov/python-project-52.git
# 2. Move to the repository
cd python-project-52

# 3. Install dependencies
make install

# 4. Create .env and setup SECRET_KEY and DATABASE_URL 
touch .env
# Open .env and add:
#SECRET_KEY=your_secret_key
#DEBUG=True
#DATABASE_URL=sqlite:///db.sqlite3

# 5. Apply migrations
uv run python manage.py migrate

# 6. Run in dev mode
make dev
```