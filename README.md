# Modular Entity System

A complete Django REST Framework project implementing a modular entity system with master entities (Vendor, Product, Course, Certification) and their mappings.

## Tech Stack

- Django 4.2+
- Django REST Framework
- drf-yasg (Swagger/ReDoc documentation)
- SQLite (default database)

## Project Structure

```
modular_entity_system/
├── core/                           # Abstract base model and utilities
├── vendor/                         # Vendor master entity
├── product/                        # Product master entity
├── course/                         # Course master entity
├── certification/                  # Certification master entity
├── vendor_product_mapping/         # Vendor-Product mapping
├── product_course_mapping/         # Product-Course mapping
├── course_certification_mapping/   # Course-Certification mapping
└── modular_entity_system/          # Project settings
```

## Requirements

```
Django>=4.2.0,<5.0
djangorestframework>=3.14.0
drf-yasg>=1.21.0
```

## Setup Instructions

### 1. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Seed Sample Data (Optional)

```bash
python manage.py seed_data
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Documentation

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **JSON Schema**: http://127.0.0.1:8000/swagger.json

## API Endpoints

### Master Entities

#### Vendors
- `GET    /api/vendors/` - List all vendors
- `POST   /api/vendors/` - Create a new vendor
- `GET    /api/vendors/<id>/` - Get a specific vendor
- `PUT    /api/vendors/<id>/` - Update a vendor completely
- `PATCH  /api/vendors/<id>/` - Update a vendor partially
- `DELETE /api/vendors/<id>/` - Soft delete a vendor

#### Products
- `GET    /api/products/` - List all products
- `POST   /api/products/` - Create a new product
- `GET    /api/products/<id>/` - Get a specific product
- `PUT    /api/products/<id>/` - Update a product completely
- `PATCH  /api/products/<id>/` - Update a product partially
- `DELETE /api/products/<id>/` - Soft delete a product

**Query Parameters:**
- `?vendor_id=<id>` - Filter products by vendor ID

#### Courses
- `GET    /api/courses/` - List all courses
- `POST   /api/courses/` - Create a new course
- `GET    /api/courses/<id>/` - Get a specific course
- `PUT    /api/courses/<id>/` - Update a course completely
- `PATCH  /api/courses/<id>/` - Update a course partially
- `DELETE /api/courses/<id>/` - Soft delete a course

**Query Parameters:**
- `?product_id=<id>` - Filter courses by product ID

#### Certifications
- `GET    /api/certifications/` - List all certifications
- `POST   /api/certifications/` - Create a new certification
- `GET    /api/certifications/<id>/` - Get a specific certification
- `PUT    /api/certifications/<id>/` - Update a certification completely
- `PATCH  /api/certifications/<id>/` - Update a certification partially
- `DELETE /api/certifications/<id>/` - Soft delete a certification

**Query Parameters:**
- `?course_id=<id>` - Filter certifications by course ID

### Mapping Entities

#### Vendor-Product Mappings
- `GET    /api/vendor-product-mappings/` - List all mappings
- `POST   /api/vendor-product-mappings/` - Create a new mapping
- `GET    /api/vendor-product-mappings/<id>/` - Get a specific mapping
- `PUT    /api/vendor-product-mappings/<id>/` - Update a mapping completely
- `PATCH  /api/vendor-product-mappings/<id>/` - Update a mapping partially
- `DELETE /api/vendor-product-mappings/<id>/` - Soft delete a mapping

**Query Parameters:**
- `?vendor_id=<id>` - Filter mappings by vendor ID

#### Product-Course Mappings
- `GET    /api/product-course-mappings/` - List all mappings
- `POST   /api/product-course-mappings/` - Create a new mapping
- `GET    /api/product-course-mappings/<id>/` - Get a specific mapping
- `PUT    /api/product-course-mappings/<id>/` - Update a mapping completely
- `PATCH  /api/product-course-mappings/<id>/` - Update a mapping partially
- `DELETE /api/product-course-mappings/<id>/` - Soft delete a mapping

**Query Parameters:**
- `?product_id=<id>` - Filter mappings by product ID

#### Course-Certification Mappings
- `GET    /api/course-certification-mappings/` - List all mappings
- `POST   /api/course-certification-mappings/` - Create a new mapping
- `GET    /api/course-certification-mappings/<id>/` - Get a specific mapping
- `PUT    /api/course-certification-mappings/<id>/` - Update a mapping completely
- `PATCH  /api/course-certification-mappings/<id>/` - Update a mapping partially
- `DELETE /api/course-certification-mappings/<id>/` - Soft delete a mapping

**Query Parameters:**
- `?course_id=<id>` - Filter mappings by course ID

## Request/Response Examples

### Create a Vendor

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechCorp Solutions",
    "code": "TECH001",
    "description": "Leading technology provider",
    "is_active": true
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "TechCorp Solutions",
  "code": "TECH001",
  "description": "Leading technology provider",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Create a Product

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Enterprise Suite",
    "code": "PROD001",
    "description": "Complete enterprise solution",
    "is_active": true
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Enterprise Suite",
  "code": "PROD001",
  "description": "Complete enterprise solution",
  "is_active": true,
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

### Create a Vendor-Product Mapping

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true,
    "is_active": true
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "vendor": 1,
  "vendor_name": "TechCorp Solutions",
  "product": 1,
  "product_name": "Enterprise Suite",
  "primary_mapping": true,
  "is_active": true,
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": "2024-01-15T10:40:00Z"
}
```

### Filter Products by Vendor

**Request:**
```bash
curl "http://127.0.0.1:8000/api/products/?vendor_id=1"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Enterprise Suite",
    "code": "PROD001",
    "description": "Complete enterprise solution",
    "is_active": true,
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
]
```

### Update a Vendor (Partial)

**Request:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "TechCorp Solutions",
  "code": "TECH001",
  "description": "Updated description",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:45:00Z"
}
```

### Soft Delete a Vendor

**Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/vendors/1/
```

**Response (204 No Content)**

### Error Response (Validation Error)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "code": "TECH001"
  }'
```

**Response (400 Bad Request):**
```json
{
  "name": ["Name is required."]
}
```

### Error Response (Not Found)

**Request:**
```bash
curl http://127.0.0.1:8000/api/vendors/999/
```

**Response (404 Not Found):**
```json
{
  "error": "Vendor not found",
  "detail": "Vendor with id=999 does not exist."
}
```

## Validations

### Master Entity Validations
1. **Required fields**: `name` and `code` are required
2. **Unique code**: Each entity must have a unique code (case-insensitive)
3. **Active check**: Entities must be active to be referenced in mappings

### Mapping Validations
1. **Duplicate mappings**: Same vendor-product/product-course/course-certification pair cannot be created twice
2. **Primary mapping constraint**: Only one primary mapping allowed per parent entity
   - Only one primary product per vendor
   - Only one primary course per product
   - Only one primary certification per course
3. **Foreign key validation**: Referenced entities must exist and be active

## Features

- **Soft Delete**: DELETE endpoints set `is_active=False` instead of actually deleting records
- **Abstract Base Model**: All models inherit from `BaseModel` with `created_at` and `updated_at` timestamps
- **Custom Utility**: `get_object_or_404_custom()` function for consistent 404 handling
- **Swagger Documentation**: Full API documentation with request/response schemas
- **Query Parameter Filtering**: Filter related entities via query parameters

## Admin Interface

Access the Django admin at: http://127.0.0.1:8000/admin/

All entities are registered with appropriate list displays, filters, and search fields.

## Database Schema

### Master Tables
- `vendors` - Vendor master data
- `products` - Product master data
- `courses` - Course master data
- `certifications` - Certification master data

### Mapping Tables
- `vendor_product_mappings` - Vendor-Product relationships
- `product_course_mappings` - Product-Course relationships
- `course_certification_mappings` - Course-Certification relationships

All tables include:
- `id` (Primary Key)
- `created_at` (Auto timestamp)
- `updated_at` (Auto timestamp)
- `is_active` (Boolean for soft delete)
