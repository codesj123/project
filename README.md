# Django Modular Entity & Mapping System

A Django REST Framework backend for managing Vendors, Products, Courses, Certifications and their mappings — built using **APIView only**, with **drf-yasg** for API documentation.

---

## Project Structure

```
django_project/
├── config/                        # Project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                          # Shared utilities
│   ├── base_model.py              # Abstract TimeStampedModel
│   └── utils.py                   # get_object_or_404_custom, error helpers
├── vendor/                        # Master: Vendor
├── product/                       # Master: Product
├── course/                        # Master: Course
├── certification/                 # Master: Certification
├── vendor_product_mapping/        # Mapping: Vendor → Product
├── product_course_mapping/        # Mapping: Product → Course
├── course_certification_mapping/  # Mapping: Course → Certification
├── manage.py
└── requirements.txt
```

Each app contains: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`

---

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd django_project
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations vendor product course certification \
    vendor_product_mapping product_course_mapping course_certification_mapping
python manage.py migrate
```

### 5. (Optional) Seed sample data
```bash
python manage.py seed_data
```

### 6. Create a superuser (for Django admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

---

## Installed Apps

```python
INSTALLED_APPS = [
    # Django built-ins ...
    'rest_framework',
    'drf_yasg',
    # Master apps
    'vendor', 'product', 'course', 'certification',
    # Mapping apps
    'vendor_product_mapping', 'product_course_mapping', 'course_certification_mapping',
]
```

---

## API Documentation

| URL | Description |
|-----|-------------|
| `/swagger/` | Swagger UI (interactive) |
| `/redoc/` | ReDoc UI (readable) |
| `/admin/` | Django Admin |

---

## API Endpoints

### Master Entities

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/vendors/` | List vendors |
| POST | `/api/vendors/` | Create vendor |
| GET | `/api/vendors/<id>/` | Retrieve vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete |

Same pattern applies for `/api/products/`, `/api/courses/`, `/api/certifications/`.

### Mapping APIs

| Method | URL | Action |
|--------|-----|--------|
| GET/POST | `/api/vendor-product-mappings/` | List / Create |
| GET/PUT/PATCH/DELETE | `/api/vendor-product-mappings/<id>/` | Detail / Update / Delete |

Same pattern for `/api/product-course-mappings/` and `/api/course-certification-mappings/`.

---

## Query Parameter Filtering

| Endpoint | Filter Params |
|----------|---------------|
| `/api/products/` | `?vendor_id=1` |
| `/api/courses/` | `?product_id=2` |
| `/api/certifications/` | `?course_id=3` |
| `/api/vendor-product-mappings/` | `?vendor_id=1&product_id=2&is_active=true` |
| `/api/product-course-mappings/` | `?product_id=1&course_id=2` |
| `/api/course-certification-mappings/` | `?course_id=1&certification_id=2` |

---

## Validation Rules

- `code` must be unique per entity; checked on create and update.
- Duplicate mappings (same pair) are rejected via `unique_together` + serializer validation.
- Only **one** `primary_mapping=True` allowed per parent at each mapping level.
- All foreign keys are validated by DRF automatically.
- `DELETE` performs a **soft delete** (sets `is_active=False`).

---

## API Usage Examples

### Create a Vendor
```http
POST /api/vendors/
Content-Type: application/json

{
  "name": "Vendor Alpha",
  "code": "VND001",
  "description": "A top vendor"
}
```

### Create a Vendor-Product Mapping
```http
POST /api/vendor-product-mappings/
Content-Type: application/json

{
  "vendor": 1,
  "product": 2,
  "primary_mapping": true
}
```

### Filter products by vendor
```http
GET /api/products/?vendor_id=1
```

---

## Tech Stack

- Python 3.10+
- Django 4.2
- Django REST Framework 3.14
- drf-yasg 1.21
# project
