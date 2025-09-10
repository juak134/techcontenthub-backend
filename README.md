# TechContent Hub - Backend (Django + DRF) — FULL

Incluye:
- JWT + roles (`CREATOR`, `BRAND`, `ADMIN`)
- Multitenancy (Django Sites) + filtro por sitio en ViewSets
- Reglas estrictas de negocio (campañas/contenido)
- Elasticsearch (métricas por contenido)
- Celery/Redis
- Docker Compose
- Seeder con datos demo

## Start
```bash
cp .env.example .env
docker-compose up --build
# En otra terminal:
docker-compose exec web python manage.py createsuperuser   # opcional
docker-compose exec web python manage.py seed_demo_data
```
- Admin: http://localhost:8000/admin
- API:  http://localhost:8000/api/
- JWT:  POST /api/auth/token/  | POST /api/auth/token/refresh/

## Métricas (Elasticsearch)
- POST /api/metrics/content/{content_id}/
- PUT  /api/metrics/content/{content_id}/
- GET  /api/metrics/content/{content_id}/


## 📘 Documentación (OpenAPI)
- Esquema: `GET /api/schema/`
- Swagger UI: `GET /api/docs/`
- ReDoc: `GET /api/redoc/`

## ✅ Tests
```bash
docker-compose exec web python manage.py test
```


## 🔎 Filtros y Ordenamiento
- **Campaigns**: `?company=1&state=2&ordering=-budget`
- **Content**: `?creator=5&type=video&is_approved=true&ordering=-created_at`
- Soportado por **django-filter** + `OrderingFilter`.

## ⚡ Cache (Redis)
Listados cacheados por **60s** por usuario y querystring. Se configura en `core/cache/mixins.py` y en `CACHES` de `settings.py`.
