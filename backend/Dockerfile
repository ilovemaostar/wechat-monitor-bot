version: "3.9"

services:
  db:
    image: postgres:16-alpine
    container_name: wechat-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: wechat
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: wechat-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
    container_name: wechat-backend
    restart: unless-stopped
    depends_on:
      - db
      - redis
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/wechat
      REDIS_URL: redis://redis:6379/0
    ports:
      - "8000:8000"
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
    container_name: wechat-frontend
    restart: unless-stopped
    ports:
      - "5173:5173"
    depends_on:
      - backend
    environment:
      VITE_API_BASE_URL: http://localhost:8000

volumes:
  postgres_data:
