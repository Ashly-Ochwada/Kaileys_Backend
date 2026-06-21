
````markdown
# Kaileys Backend

Django REST API backend for the Kaileys Consortium mobile app.

## Features

- Manage training organizations
- Manage training courses
- Generate course access codes
- Validate access codes from the mobile app
- Track trainee details
- Access codes expire after 30 days

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL / SQLite
- Render deployment support

## Setup

### 1. Clone the project

```bash
git clone <repository-url>
cd kaileys_backend
````

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database

For local testing, SQLite can be used.

In `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For production, use PostgreSQL through `DATABASE_URL`.

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

### 7. Run server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/admin/
```

## Main Models

### Organization

Stores organization details.

Fields:

* name
* country

### Course

Stores training courses and access codes.

Fields:

* name
* access_code
* access_code_expires_at

Access codes are used by trainees to unlock course notes in the mobile app.

### Trainee

Stores trainee information.

Fields:

* full_name
* phone_number
* organization

## API Endpoints

### API Root

```http
GET /api/
```

### Verify Access

```http
POST /api/verify-access/
```

Request:

```json
{
  "phone_number": "+254712345678",
  "organization": "ABC Company",
  "course": "fire_safety",
  "access_code": "FIRE2026"
}
```

Success response:

```json
{
  "access_granted": true,
  "message": "Access granted successfully"
}
```

Error response:

```json
{
  "access_granted": false,
  "error": "Invalid access code"
}
```

### Register Trainee

```http
POST /api/register-trainee/
```

Request:

```json
{
  "full_name": "John Doe",
  "phone_number": "+254712345678",
  "organization": "ABC Company",
  "course": "fire_safety",
  "access_code": "FIRE2026"
}
```

Success response:

```json
{
  "access_granted": true,
  "message": "Access granted successfully"
}
```

### Organizations

```http
GET /api/organizations/
```

### Courses

```http
GET /api/courses/
```

### Trainees

```http
GET /api/trainees/
```

## Phone Number Format

Accepted phone number formats:

```text
+254XXXXXXXXX
+256XXXXXXXXX
+250XXXXXXXXX
```

Supported countries:

* Kenya
* Uganda
* Rwanda

## Course Values

Use these course values in API requests:

```text
fire_safety
first_aid
safety_committee
chemical_safety
scaffolding_safety
confined_space_safety
```

## Admin Usage

1. Log in to Django Admin.
2. Go to Courses.
3. Create or edit a course.
4. Enter an access code or leave it blank for auto-generation.
5. Set the access code expiry date.
6. Give the code to trainees.
7. Trainees enter the code in the mobile app.
8. If the code is correct and not expired, the app opens the notes.

## Notes

* There is no longer an admin approval workflow.
* Access is granted immediately when the correct access code is entered.
* Notes/PDFs are stored inside the mobile app.
* The backend only validates the access code.

```
```
