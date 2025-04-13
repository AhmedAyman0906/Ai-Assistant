# 🧠 AI Knowledge Assistant (Backend)

An internal AI-powered assistant to help employees search company knowledge.

## 🚀 Features
- CRUD for articles with tags
- Ask natural language questions powered by OpenAI
- Full-text search using PostgreSQL
- Stats dashboard
- JWT Auth + Roles (optional)
- Rate-limited API access
- Background tasks via Celery

## 🔐 Authentication
- Get token: `POST /api/token/`
- Use: `Authorization: Bearer <token>`

## 🧪 Test
```bash
python manage.py test
