# MedBook - Медицинская информационная система

**Docker-приложение на Django + React с Celery, Redis и PostgreSQL**

## Содержание

- [Возможности](#возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Сервисы](#сервисы)
- [Celery](#celery)
- [Решение проблем](#решение-проблем)
- [Лицензия](#лицензия)

## Возможности

 **Фронтенд**: React (Vite) приложение на `http://localhost:3000`  
 **Бэкенд**: Django REST API на `http://localhost:8000`  
 **База данных**: PostgreSQL с сохранением данных  
 **Асинхронные задачи**: Celery + Redis  
 **Мониторинг**: Flower на `http://localhost:5555`

## Требования

- Docker и Docker Compose
- Python 3.9+
- Node.js (для разработки фронтенда)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/medbook.git
   cd medbook
   cp .env.example .env

# Сборка и запуск
    make build

# Остановка

    make down

## Services & Ports

| Service    | URL                                            | Port | Description            |
|------------|------------------------------------------------|------|------------------------|
| Frontend   | [http://localhost:3000](http://localhost:3000) | 3000 | React application      |
| Backend    | [http://localhost:8000](http://localhost:8000) | 8000 | Django REST API        |
| PostgreSQL | `host: localhost`                              | 5432 | Database               |
| Redis      | -                                              | 6379 | Celery task broker     |
| Flower     | [http://localhost:5555](http://localhost:5555) | 5555 | Celery task monitoring |
| Swagger     | [http://localhost:8000](http://localhost:8000/swagger) | 8000 | Swagger task api |

