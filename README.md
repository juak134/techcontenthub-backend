# TechContent Hub - Backend

Plataforma de gestión de campañas y contenido digital, construida con **Django REST Framework**, **JWT**, **Docker**, **Celery/Redis** y **Elasticsearch**.

---

## 📦 Instalación

### Requisitos previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Linux containers en Windows/WSL2)
- `docker-compose`

### Pasos de instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-org/techcontent-hub-backend.git
cd techcontent-hub-backend

# Copiar variables de entorno
cp .env.example .env
```

---

## ⚙️ Variables de entorno

Ejemplo de `.env`:

```env
# Django
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
DJANGO_DEFAULT_SITE_ID=1

# Base de datos (Postgres)
POSTGRES_DB=techcontent
POSTGRES_USER=techuser
POSTGRES_PASSWORD=techpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Elasticsearch
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=content_metrics

# Email global (cada tenant puede sobreescribirlo)
DEFAULT_FROM_EMAIL=no-reply@techcontent.local
```

---

## ▶️ Levantar el proyecto

```bash
# Construir imágenes y levantar servicios
docker-compose up --build

# Aplicar migraciones iniciales (en otra terminal)
docker-compose exec web python manage.py migrate

# Sembrar datos demo (usuarios, compañías, campañas, contenido)
docker-compose exec web python manage.py seed_demo_data
```

Usuarios demo creados por el seeder:

| Usuario          | Rol     | Contraseña  |
|------------------|---------|-------------|
| admin@test.com   | ADMIN   | password123 |
| brand@test.com   | BRAND   | password123 |
| creator@test.com | CREATOR | password123 |

---

## 🌐 Endpoints principales

- **Auth (JWT)**
  - `POST /api/auth/token/` → obtener `access` y `refresh`
  - `POST /api/auth/token/refresh/`

- **Companies**
  - `GET /api/companies/`
  - `POST /api/companies/`
  - `GET /api/company-configs/`
  - `GET /api/email-configs/`

- **Campaigns**
  - `GET /api/campaigns/`
  - `POST /api/campaigns/` (Brand solo en borrador)
  - `PATCH /api/campaigns/{id}/` (solo Admin cambia estado)
  - `POST /api/campaigns/{id}/add-creators/` (solo Admin, campañas activas)

- **Content**
  - `POST /api/content/` (solo Creator o Admin; campaña activa)
  - `GET /api/content/{id}/`

- **Creators**
  - `GET /api/creators/`

- **Metrics (Elasticsearch)**
  - `POST /api/metrics/content/{content_id}/`
  - `PUT /api/metrics/content/{content_id}/`
  - `GET /api/metrics/content/{content_id}/`

- **Docs**
  - Swagger UI: `http://localhost:8000/api/docs/`
  - Redoc: `http://localhost:8000/api/redoc/`

---

## 📝 Ejemplos de uso

### Obtener token JWT (admin)
```bash
curl -X POST http://localhost:8000/api/auth/token/   -H "Content-Type: application/json"   -d '{"username":"admin@test.com","password":"password123"}'
```

### Crear campaña como Brand (solo borrador permitido)
```bash
curl -X POST http://localhost:8000/api/campaigns/   -H "Authorization: Bearer <ACCESS>"   -H "Content-Type: application/json"   -d '{"company":1,"name":"Campaña Demo","state":1}'
```

### Subir contenido como Creator
```bash
curl -X POST http://localhost:8000/api/content/   -H "Authorization: Bearer <ACCESS>"   -H "Content-Type: application/json"   -d '{"campaign":2,"creator":3,"title":"Video Demo","url":"https://ejemplo.com","type":"video"}'
```

### Agregar métricas (Elasticsearch)
```bash
curl -X POST http://localhost:8000/api/metrics/content/1/   -H "Authorization: Bearer <ACCESS>"   -H "Content-Type: application/json"   -d '{"metrics":{"views":100,"likes":25,"shares":10,"comments":5}}'
```

---

## 📧 Configuración de email por tenant

Cada **Company** puede tener su propia configuración SMTP en `EmailConfig`:

Campos principales:
- `host`, `port`
- `username`, `password`
- `use_tls`, `use_ssl`

Esto permite que cada tenant/envío de campaña use su propio servidor de correo.

Ejemplo (POST):
```json
{
  "company": 1,
  "host": "smtp.miempresa.com",
  "port": 587,
  "username": "noreply@miempresa.com",
  "password": "secreto",
  "use_tls": true,
  "use_ssl": false
}
```

---

## 📊 Estructura de datos en Elasticsearch

Cada documento de métricas (`content_metrics`) tiene la forma:

```json
{
  "content_id": "1",
  "campaign_id": "2",
  "creator_id": "3",
  "company_id": "1",
  "site_id": "1",
  "metrics": {
    "views": 100,
    "likes": 25,
    "shares": 10,
    "comments": 5
  },
  "content_info": {
    "title": "Video campaña verano",
    "type": "video",
    "url": "https://example.com/video"
  },
  "timestamp": "2025-09-10T15:30:00Z",
  "updated_at": "2025-09-10T16:00:00Z"
}
```

Esto permite agregaciones y análisis por campaña, creator o empresa.

---

## 🧪 Tests

```bash
# Ejecutar suite de tests
docker-compose exec web python manage.py test
```

Incluye validación de reglas de negocio y métricas mockeadas en ES.

---
