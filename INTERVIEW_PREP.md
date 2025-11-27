# 🎯 Interview Preparation Guide - Pluggable Rule Engine

## Table of Contents
1. [📁 Project File Structure](#project-file-structure)
2. [Project Overview](#project-overview)
3. [Complete Build Process - Step by Step](#complete-build-process)
4. [Architecture Deep Dive](#architecture-deep-dive)
5. [Key Technical Decisions](#key-technical-decisions)
6. [Interview Questions & Answers](#interview-questions--answers)
7. [Talking Points](#talking-points)

---

## 📁 Project File Structure

**Quick Reference Guide:** Every file, its purpose, and key line numbers

### Core Application Files

| File | Purpose | Key Sections |
|------|---------|--------------|
| **Configuration** | | |
| `config/settings.py` | Django settings | • Lines 38-50: INSTALLED_APPS<br>• Lines 53-61: MIDDLEWARE<br>• Lines 88-93: DATABASE<br>• Lines 139-151: REST_FRAMEWORK<br>• Lines 164-196: LOGGING |
| `config/urls.py` | URL routing + Swagger | • Lines 24-48: Swagger config<br>• Lines 50-58: URL patterns |
| **Orders App** | | |
| `orders/models.py` | Order model | • Lines 6-42: Order class definition<br>• Lines 16-20: total field<br>• Lines 22-25: items_count field |
| `orders/admin.py` | Admin interface | • Lines 5-23: OrderAdmin config |
| `orders/serializers.py` | API serialization | • Lines 4-24: OrderSerializer |
| `orders/apps.py` | **Auto-seeding on startup** | • Lines 8-26: ready() method |
| `orders/management/commands/seed_orders.py` | Seed command | • Lines 9-34: Creates 3 orders |
| **Rules App (THE CORE!)** | | |
| `rules/engine.py` | **⭐ Metaclass magic** | • Lines 16-65: RuleRegistry<br>• Lines 68-84: RuleMeta (auto-register)<br>• Lines 87-128: BaseRule<br>• Lines 131-170: RuleEngine |
| `rules/order_rules.py` | **⭐ Business rules** | • Lines 9-25: MinTotalRule<br>• Lines 28-44: MinItemsRule<br>• Lines 47-76: DivisibleByFiveRule |
| `rules/views.py` | **⭐ API endpoints** | • Lines 23-114: RuleCheckView (POST /rules/check/)<br>• Lines 117-154: RuleListView (GET /rules/) |
| `rules/serializers.py` | Request/response validation | • Lines 7-45: RuleCheckRequestSerializer<br>• Lines 26-43: validate_rules() |
| `rules/exceptions.py` | Error handling | • Lines 11-55: custom_exception_handler |
| `rules/urls.py` | Rules routing | • Lines 8-11: URL patterns |
| `rules/apps.py` | Load rules on startup | • Lines 8-13: ready() imports rules |
| `rules/tests.py` | **⭐ Test suite (18 tests)** | • Lines 14-37: Registry tests<br>• Lines 40-83: Rule logic tests<br>• Lines 86-131: Engine tests<br>• Lines 134-223: API tests |

### Deployment & CI/CD Files

| File | Purpose | Key Content |
|------|---------|-------------|
| `requirements.txt` | Dependencies | Django 5.0, DRF 3.14, drf-yasg, etc. |
| `Dockerfile` | Container setup | Lines 1-28: Multi-stage build |
| `docker-compose.yml` | Local dev | Lines 1-17: Service configuration |
| `render.yaml` | **Render deployment** | • Line 5: `plan: free` (IMPORTANT!)<br>• Line 6: Build command with migrations |
| `build.sh` | Build script | Lines 1-9: Install, migrate, seed |
| `.github/workflows/ci.yml` | CI/CD pipeline | Lines 13-66: Test & build jobs |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `INTERVIEW_PREP.md` | This file! Interview guide |
| `api_examples.md` | cURL, Python, JS examples |
| `LICENSE` | MIT License |
| `CONTRIBUTING.md` | Contribution guidelines |

---

### 🎯 Files to Master for Interview

**Must Know Inside-Out:**
1. **`rules/engine.py`** - The metaclass auto-registration pattern (this is your innovation!)
2. **`rules/order_rules.py`** - How business rules are implemented
3. **`rules/views.py`** - RESTful API design and validation

**Should Be Familiar With:**
4. `config/settings.py` - Production configuration
5. `rules/tests.py` - Test strategy and coverage
6. `orders/models.py` - Data model design
7. `render.yaml` - Deployment configuration

**Quick Lookup Reference:**
8. Everything else - Know they exist and what they do

---

## Project Overview

### What Was Built
A production-ready Django REST API featuring a **pluggable rule engine** that validates orders against configurable business rules. The key innovation is the **auto-registration pattern** using Python metaclasses, allowing new rules to be added without modifying existing code.

### Live Links
- **GitHub:** https://github.com/William9701/Pluggable_Rule_Engine
- **Live Demo:** https://pluggable-rule-engine.onrender.com

### Tech Stack
- **Backend:** Django 5.0, Django REST Framework 3.14
- **Database:** SQLite (dev), PostgreSQL-ready
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Deployment:** Render (free tier)
- **CI/CD:** GitHub Actions
- **Containerization:** Docker + Docker Compose
- **Testing:** Django's built-in test framework (18 tests, 100% passing)

---

## Complete Build Process - Step by Step

### Phase 1: Initial Project Setup

**Step 1: Create Requirements File**
```bash
# Command: Created requirements.txt file
```
**What it does:** Lists all Python dependencies needed for the project
**Why:** Ensures consistent environment across development and production

**Dependencies added:**
- `Django==5.0.1` - Web framework
- `djangorestframework==3.14.0` - REST API toolkit
- `drf-yasg==1.21.7` - Swagger/OpenAPI documentation
- `python-dotenv==1.0.0` - Environment variable management
- `whitenoise==6.6.0` - Static file serving
- `gunicorn==21.2.0` - Production WSGI server
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `dj-database-url==2.1.0` - Database URL parsing

**Step 2: Create Virtual Environment**
```bash
python -m venv venv
```
**What it does:** Creates an isolated Python environment in the `venv` directory
**Why:** Prevents dependency conflicts with system Python

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```
**What it does:** Installs all packages listed in requirements.txt
**Output:** Django, DRF, and all dependencies installed successfully

**Step 4: Create Django Project**
```bash
django-admin startproject config .
```
**What it does:**
- Creates Django project structure
- `config/` directory contains settings, URLs, WSGI
- `.` means create in current directory (not subdirectory)
**Files created:**
- `manage.py` - Command-line utility
- `config/settings.py` - Project configuration
- `config/urls.py` - URL routing
- `config/wsgi.py` - WSGI deployment interface

**Step 5: Create Django Apps**
```bash
python manage.py startapp orders
python manage.py startapp rules
```
**What it does:** Creates two Django apps (modular components)
- `orders/` - Handles Order model and data
- `rules/` - Contains rule engine and API endpoints

---

### Phase 2: Configuration & Settings

**Step 6: Configure settings.py**

📁 **File:** `config/settings.py`

**Added Environment Variable Support (Lines 13-18):**
```python
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```
**Why:** Separates configuration from code, enables different settings for dev/prod

**Added Apps to INSTALLED_APPS (Lines 38-50):**
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",      # REST API framework
    "drf_yasg",           # Swagger documentation
    # Local apps
    "orders",             # Our orders app
    "rules",              # Our rules app
]
```

**Added WhiteNoise Middleware (Lines 53-61):**
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files - ADD THIS
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```
**Why:** Efficiently serves static files in production without needing Nginx/Apache

**Configured Database (Lines 88-93):**
```python
DATABASES = {
    "default": dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}
```
**Why:** Uses DATABASE_URL env var if available, falls back to SQLite

**Added REST Framework Config (Lines 139-151):**
```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'EXCEPTION_HANDLER': 'rules.exceptions.custom_exception_handler',
}
```

**Added Logging Configuration (Lines 164-196):**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'rules': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```
**Why:** Tracks rule registration and evaluation for debugging

---

### Phase 3: Order Model Implementation

**Step 7: Create Order Model**

📁 **File:** `orders/models.py` (Lines 1-42)

```python
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    """
    Order model representing a customer order.

    Attributes:
        total: The total amount of the order (must be non-negative)
        items_count: The number of items in the order (must be positive)
        created_at: Timestamp when the order was created
        updated_at: Timestamp when the order was last updated
    """
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total amount of the order"
    )
    items_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of items in the order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['total']),
        ]

    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total}, Items: {self.items_count}"

    def __repr__(self):
        return f"<Order(id={self.id}, total={self.total}, items_count={self.items_count})>"
```

**Key Decisions:**
- **DecimalField for money:** Avoids floating-point precision errors
- **Validators:** Ensures data integrity at model level
- **Indexes:** Optimizes queries by created_at and total
- **Timestamps:** Audit trail for when orders were created/modified

**Step 8: Create Admin Interface**

📁 **File:** `orders/admin.py` (Lines 1-23)

```python
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ('id', 'total', 'items_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Order Information', {
            'fields': ('total', 'items_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```
**Why:** Provides GUI for managing orders in Django admin

**Step 9: Create Serializers**

📁 **File:** `orders/serializers.py` (Lines 1-24)
```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError("Total must be non-negative.")
        return value
```
**Why:** Converts between JSON and Django model instances, adds validation

**Step 10: Create Seed Command**

**File:** `orders/management/commands/seed_orders.py`
```python
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if Order.objects.exists():
            return  # Don't seed if orders exist

        orders_data = [
            {'total': Decimal('150.00'), 'items_count': 3},
            {'total': Decimal('75.50'), 'items_count': 1},
            {'total': Decimal('200.00'), 'items_count': 5},
        ]
        for data in orders_data:
            Order.objects.create(**data)
```
**Usage:** `python manage.py seed_orders`

**Step 11: Run Migrations**
```bash
python manage.py makemigrations
```
**Output:**
```
Migrations for 'orders':
  orders/migrations/0001_initial.py
    - Create model Order
```
**What it does:** Creates migration file that defines database schema changes

```bash
python manage.py migrate
```
**Output:**
```
Applying orders.0001_initial... OK
```
**What it does:** Applies migration to database, creates `orders_order` table

**Step 12: Seed Database**
```bash
python manage.py seed_orders
```
**Output:**
```
Created order #1: Total=$150.00, Items=3
Created order #2: Total=$75.50, Items=1
Created order #3: Total=$200.00, Items=5
```

---

### Phase 4: Rule Engine Implementation (The Core Innovation)

**Step 13: Create Rule Engine Core**

**File:** `rules/engine.py`

**Part 1: Registry Pattern**
```python
class RuleRegistry:
    _rules: Dict[str, Type['BaseRule']] = {}

    @classmethod
    def register(cls, name: str, rule_class: Type['BaseRule']) -> None:
        cls._rules[name] = rule_class
        logger.info(f"Registered rule: {name}")

    @classmethod
    def get_rule(cls, name: str) -> Type['BaseRule']:
        if name not in cls._rules:
            raise KeyError(f"Rule '{name}' not found")
        return cls._rules[name]
```
**Why:** Central registry to store and retrieve all rule classes

**Part 2: Auto-Registration Metaclass**
```python
class RuleMeta(ABCMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        cls = super().__new__(mcs, name, bases, attrs)

        # Auto-register if it has a name
        if name != 'BaseRule' and 'name' in attrs and attrs['name']:
            RuleRegistry.register(attrs['name'], cls)

        return cls
```
**Why:** This is the magic! When Python creates a class with this metaclass, it automatically registers itself.

**How it works:**
1. When `class MinTotalRule(BaseRule)` is defined, Python calls `RuleMeta.__new__`
2. The metaclass checks if the class has a `name` attribute
3. If yes, it automatically calls `RuleRegistry.register()`
4. No manual registration needed!

**Part 3: Base Rule Class**
```python
class BaseRule(metaclass=RuleMeta):
    name: str = None
    description: str = ""

    @abstractmethod
    def evaluate(self, order) -> bool:
        pass
```
**Why:**
- Defines interface all rules must follow
- Uses metaclass for auto-registration
- Abstract method ensures `evaluate` is implemented

**Part 4: Rule Engine**
```python
class RuleEngine:
    def evaluate_rules(self, order, rule_names: list) -> dict:
        results = {}
        for rule_name in rule_names:
            rule_class = RuleRegistry.get_rule(rule_name)
            rule_instance = rule_class()
            results[rule_name] = rule_instance.evaluate(order)

        return {
            'passed': all(results.values()),
            'details': results
        }
```
**Why:** Orchestrates rule evaluation, returns detailed results

---

**Step 14: Implement Business Rules**

**File:** `rules/order_rules.py`

```python
class MinimumTotalRule(BaseRule):
    name = "min_total_100"
    description = "Validates that order total is greater than 100"

    def evaluate(self, order) -> bool:
        return order.total > Decimal('100.00')

class MinimumItemsRule(BaseRule):
    name = "min_items_2"
    description = "Validates that order has at least 2 items"

    def evaluate(self, order) -> bool:
        return order.items_count >= 2

class DivisibleByFiveRule(BaseRule):
    name = "divisible_by_5"
    description = "Validates that order total is divisible by 5"

    def evaluate(self, order) -> bool:
        return order.total % Decimal('5.00') == Decimal('0.00')
```

**Key Point:** As soon as these classes are defined, they're automatically registered! No need to manually add them to any list.

**Step 15: Enable Auto-Registration on App Startup**

**File:** `rules/apps.py`
```python
class RulesConfig(AppConfig):
    def ready(self):
        from . import order_rules  # Import triggers registration
```
**Why:** Ensures rules are loaded when Django starts

**Step 16: Add Auto-Seeding**

**File:** `orders/apps.py`
```python
class OrdersConfig(AppConfig):
    def ready(self):
        from decimal import Decimal
        from django.db.utils import OperationalError

        try:
            from .models import Order
            if not Order.objects.exists():
                orders_data = [
                    {'total': Decimal('150.00'), 'items_count': 3},
                    {'total': Decimal('75.50'), 'items_count': 1},
                    {'total': Decimal('200.00'), 'items_count': 5},
                ]
                for data in orders_data:
                    Order.objects.create(**data)
        except (OperationalError, Exception):
            pass  # Table doesn't exist yet during migrations
```
**Why:** Automatically seeds database on first startup (important for Render deployment)

---

### Phase 5: REST API Implementation

**Step 17: Create Exception Handler**

**File:** `rules/exceptions.py`
```python
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, KeyError):
            return Response({
                'error': 'Invalid rule name',
                'detail': str(exc),
            }, status=status.HTTP_400_BAD_REQUEST)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response
```
**Why:** Provides consistent error response format

**Step 18: Create Request/Response Serializers**

**File:** `rules/serializers.py`

```python
class RuleCheckRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    rules = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1
    )

    def validate_rules(self, value):
        invalid_rules = []
        for rule_name in value:
            if not RuleRegistry.rule_exists(rule_name):
                invalid_rules.append(rule_name)

        if invalid_rules:
            available = list(RuleRegistry.get_all_rules().keys())
            raise serializers.ValidationError(
                f"Invalid rule(s): {', '.join(invalid_rules)}. "
                f"Available rules: {', '.join(available)}"
            )
        return value
```
**Why:**
- Validates request data before processing
- Provides helpful error messages with available rules
- Checks rules exist in registry

**Step 19: Create API Views**

**File:** `rules/views.py`

```python
class RuleCheckView(APIView):
    @swagger_auto_schema(
        operation_description="Evaluate multiple rules against an order",
        request_body=RuleCheckRequestSerializer,
        responses={200: RuleCheckResponseSerializer}
    )
    def post(self, request):
        # Validate request
        serializer = RuleCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid request',
                'detail': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get order
        order_id = serializer.validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'error': 'Order not found',
                'detail': f'Order with id {order_id} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        # Evaluate rules
        engine = RuleEngine()
        result = engine.evaluate_rules(order, serializer.validated_data['rules'])

        return Response(result, status=status.HTTP_200_OK)

class RuleListView(APIView):
    def get(self, request):
        rules = RuleRegistry.get_all_rules()
        rules_info = [
            {'name': rule_class.name, 'description': rule_class.description}
            for rule_class in rules.values()
        ]
        return Response(rules_info, status=status.HTTP_200_OK)
```

**Step 20: Configure URLs**

**File:** `rules/urls.py`
```python
urlpatterns = [
    path('check/', RuleCheckView.as_view(), name='rule-check'),
    path('', RuleListView.as_view(), name='rule-list'),
]
```

**File:** `config/urls.py`
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Pluggable Rule Engine API",
        default_version='v1',
        description="Auto-registered rules for order validation",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rules/', include('rules.urls')),
    path('', schema_view.with_ui('swagger'), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='redoc'),
]
```

---

### Phase 6: Testing

**Step 21: Create Comprehensive Test Suite**

**File:** `rules/tests.py`

**Tests Created:**
1. **TestRuleRegistry** (4 tests)
   - Rules are auto-registered
   - Get rule by name
   - Non-existent rule raises error
   - Check rule existence

2. **TestOrderRules** (3 tests)
   - min_total_100 rule logic
   - min_items_2 rule logic
   - divisible_by_5 rule logic

3. **TestRuleEngine** (4 tests)
   - Single rule evaluation
   - Multiple rules all pass
   - Multiple rules some fail
   - Non-existent rule raises error

4. **TestRuleCheckAPI** (6 tests)
   - Successful rule check
   - Some rules fail
   - Order not found (404)
   - Invalid rule name (400)
   - Missing required fields (400)
   - Invalid order_id validation (400)

5. **TestRuleListAPI** (1 test)
   - List all available rules

**Total: 18 tests**

**Step 22: Run Tests**
```bash
python manage.py test
```
**Output:**
```
Ran 18 tests in 0.032s
OK
```

**All tests passed!** ✅

---

### Phase 7: Containerization

**Step 23: Create Dockerfile**

**File:** `Dockerfile`
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
```

**Key Points:**
- Multi-stage build for smaller image
- Non-root user for security
- Gunicorn as production server

**Step 24: Create docker-compose.yml**

```yaml
services:
  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py seed_orders &&
             gunicorn --bind 0.0.0.0:8000 config.wsgi:application"
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
```

**Usage:**
```bash
docker-compose up
```

---

### Phase 8: CI/CD Pipeline

**Step 25: Create GitHub Actions Workflow**

**File:** `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python manage.py test
```

**What it does:**
- Runs tests on every push/PR
- Tests against Python 3.10 and 3.11
- Fails if any test fails

---

### Phase 9: Deployment

**Step 26: Create Render Configuration**

**File:** `render.yaml`
```yaml
services:
  - type: web
    name: pluggable-rule-engine
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_orders"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
```

**Key Addition:** `plan: free` - Without this, Render asks for payment!

**Step 27: Deploy to Render**

1. Push to GitHub
2. Go to render.com
3. New → Web Service
4. Connect GitHub repo
5. Use Blueprint (render.yaml)
6. Deploy

**Deployment Process:**
```
Building...
Installing dependencies...
Running migrations...
Seeding database...
Starting Gunicorn...
Service is live! 🎉
```

**URL:** https://pluggable-rule-engine.onrender.com

---

### Phase 10: Git Commit History

**Professional Commit Strategy:**

```bash
# 1. Initial setup
git add .gitignore requirements.txt .env.example
git commit -m "feat: initial project setup with dependencies and configuration"

# 2. Django configuration
git add config/ manage.py
git commit -m "feat: configure Django project with production settings"

# 3. Order model
git add orders/
git commit -m "feat: implement Order model with validation and seeding"

# 4. Rule engine core
git add rules/engine.py rules/order_rules.py rules/apps.py
git commit -m "feat: implement pluggable rule engine with auto-registration"

# 5. API implementation
git add rules/views.py rules/serializers.py rules/urls.py
git commit -m "feat: build RESTful API for rule validation"

# 6. Tests
git add rules/tests.py
git commit -m "test: add comprehensive test suite with 100% coverage"

# 7. Docker
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "build: add Docker configuration for containerization"

# 8. CI/CD
git add .github/
git commit -m "ci: implement CI/CD pipeline with GitHub Actions"

# 9. Deployment
git add render.yaml build.sh
git commit -m "deploy: add Render deployment configuration"

# 10. Documentation
git add README.md LICENSE CONTRIBUTING.md
git commit -m "docs: add comprehensive project documentation"

# 11. Bug fixes (discovered during deployment)
git add orders/apps.py
git commit -m "fix: handle database not ready during migrations"

git add render.yaml
git commit -m "fix: add free plan to render.yaml to avoid payment requirement"

# 12. Final updates
git add README.md
git commit -m "docs: update README with live demo URL"
```

**Total: 13 commits, all with conventional commit messages**

---

## Architecture Deep Dive

### Design Patterns Used

#### 1. **Registry Pattern**
```python
class RuleRegistry:
    _rules: Dict[str, Type['BaseRule']] = {}
```
**Purpose:** Central registry to store all rule classes
**Benefits:**
- Single source of truth
- Easy to query available rules
- Supports dynamic rule discovery

#### 2. **Metaclass Pattern** (Advanced Python)
```python
class RuleMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        # Auto-register when class is created
        RuleRegistry.register(attrs['name'], cls)
```
**Purpose:** Auto-register rules when class is defined
**Benefits:**
- Zero-configuration
- Impossible to forget registration
- Clean, declarative code

**How Metaclasses Work:**
```python
# When Python sees this:
class MinTotalRule(BaseRule):
    name = "min_total_100"
    def evaluate(self, order):
        return order.total > 100

# Python actually does this behind the scenes:
MinTotalRule = RuleMeta('MinTotalRule', (BaseRule,), {
    'name': 'min_total_100',
    'evaluate': lambda self, order: order.total > 100
})

# RuleMeta.__new__ is called, which auto-registers the rule!
```

#### 3. **Strategy Pattern**
```python
class BaseRule(ABC):
    @abstractmethod
    def evaluate(self, order) -> bool:
        pass
```
**Purpose:** Define family of interchangeable algorithms (rules)
**Benefits:**
- Rules are interchangeable
- Easy to add new rules
- Testable in isolation

#### 4. **Template Method Pattern**
```python
class RuleEngine:
    def evaluate_rules(self, order, rule_names):
        for rule_name in rule_names:
            rule = RuleRegistry.get_rule(rule_name)()
            results[rule_name] = rule.evaluate(order)
```
**Purpose:** Define skeleton of algorithm, let subclasses fill in details
**Benefits:**
- Consistent evaluation logic
- Rules only implement their specific logic

#### 5. **Repository Pattern** (Django ORM)
```python
Order.objects.get(id=order_id)
```
**Purpose:** Abstract data access
**Benefits:**
- Database-agnostic code
- Easy to test with mocks
- Clean separation of concerns

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client (Browser/cURL)                │
└─────────────────────────────────────────────────────────┘
                           │ HTTP
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Gunicorn (WSGI Server)                  │
│                    3 Worker Processes                     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Django Framework                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Middleware Stack                      │  │
│  │  • Security  • CORS  • Authentication              │  │
│  └────────────────────────────────────────────────────┘  │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │              URL Routing                           │  │
│  │  • /rules/  →  RuleListView                       │  │
│  │  • /rules/check/  →  RuleCheckView                │  │
│  └────────────────────────────────────────────────────┘  │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │              API Views (DRF)                       │  │
│  │  • Validate request                                │  │
│  │  • Call business logic                             │  │
│  │  • Serialize response                              │  │
│  └────────────────────────────────────────────────────┘  │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Rule Engine                           │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │         RuleRegistry                         │  │  │
│  │  │  {                                           │  │  │
│  │  │    "min_total_100": MinTotalRule,          │  │  │
│  │  │    "min_items_2": MinItemsRule,            │  │  │
│  │  │    "divisible_by_5": DivisibleByFiveRule   │  │  │
│  │  │  }                                           │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  • Lookup rules by name                            │  │
│  │  • Instantiate rule objects                        │  │
│  │  • Call evaluate() method                          │  │
│  │  • Aggregate results                               │  │
│  └────────────────────────────────────────────────────┘  │
│                         │                                │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Django ORM                            │  │
│  │  • Query orders                                    │  │
│  │  • Transaction management                          │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  SQLite Database                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │  orders_order                                      │  │
│  │  ├── id (PK)                                       │  │
│  │  ├── total (DECIMAL)                               │  │
│  │  ├── items_count (INTEGER)                         │  │
│  │  ├── created_at (DATETIME)                         │  │
│  │  └── updated_at (DATETIME)                         │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Request Flow Example

**Request:** `POST /rules/check/`
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2"]
}
```

**Step-by-Step Execution:**

1. **Gunicorn receives HTTP request**
   - Worker process handles request

2. **Django middleware processes request**
   - CSRF check (exempt for API)
   - Authentication (none required)

3. **URL routing**
   - `/rules/check/` matches `RuleCheckView.post()`

4. **View validates request**
   ```python
   serializer = RuleCheckRequestSerializer(data=request.data)
   serializer.is_valid()  # Validates order_id and rules
   ```

5. **Fetch order from database**
   ```python
   order = Order.objects.get(id=1)
   # SQL: SELECT * FROM orders_order WHERE id = 1
   ```

6. **Initialize rule engine**
   ```python
   engine = RuleEngine()
   ```

7. **Evaluate each rule**
   ```python
   # For "min_total_100":
   rule_class = RuleRegistry.get_rule("min_total_100")  # Gets MinTotalRule
   rule = rule_class()  # Instantiate
   result = rule.evaluate(order)  # Returns True (150 > 100)

   # For "min_items_2":
   rule_class = RuleRegistry.get_rule("min_items_2")  # Gets MinItemsRule
   rule = rule_class()
   result = rule.evaluate(order)  # Returns True (3 >= 2)
   ```

8. **Aggregate results**
   ```python
   {
       'passed': True,  # All rules passed
       'details': {
           'min_total_100': True,
           'min_items_2': True
       }
   }
   ```

9. **Serialize and return response**
   ```python
   return Response(result, status=200)
   ```

10. **Client receives JSON response**

### Database Schema

```sql
CREATE TABLE orders_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    items_count INTEGER NOT NULL CHECK (items_count >= 1),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX orders_order_created_at_idx ON orders_order(created_at DESC);
CREATE INDEX orders_order_total_idx ON orders_order(total);
```

**Indexes Explained:**
- `created_at DESC`: Fast sorting/filtering by newest orders
- `total`: Fast filtering by price ranges

---

## Key Technical Decisions

### 1. Why Metaclasses for Auto-Registration?

**Alternatives Considered:**
- Manual registration in a list
- Decorator pattern
- Import-time registration

**Chosen Solution: Metaclass**

**Pros:**
- Truly zero-configuration
- Impossible to forget registration
- Clean, declarative syntax
- Enforces inheritance

**Cons:**
- Advanced Python concept
- Can be confusing for beginners
- Harder to debug

**Why it's better:**
```python
# ❌ Manual registration (error-prone):
class MinTotalRule(BaseRule):
    pass
register_rule(MinTotalRule)  # Easy to forget!

# ✅ Metaclass (automatic):
class MinTotalRule(BaseRule):
    name = "min_total_100"
# That's it! Automatically registered!
```

### 2. Why Decimal for Money?

```python
total = models.DecimalField(max_digits=10, decimal_places=2)
```

**Problem with Float:**
```python
>>> 0.1 + 0.2
0.30000000000000004  # ❌ Precision error!
```

**With Decimal:**
```python
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')  # ✅ Exact!
```

**Why it matters:** Financial calculations must be exact!

### 3. Why SQLite in Production?

**Normally bad practice, but acceptable here because:**
- Demo project, not production
- Low traffic expected
- Render free tier has persistent disk
- Easy to switch to PostgreSQL (just change DATABASE_URL)

**For real production:**
```python
# render.yaml would include:
databases:
  - name: mydb
    plan: free
```

### 4. Why REST Instead of GraphQL?

**REST Chosen Because:**
- Simpler for this use case
- Requirements specified REST
- Better caching with HTTP methods
- Swagger documentation is excellent

**When GraphQL is better:**
- Complex nested data
- Frontend needs flexible queries
- Multiple related resources

### 5. Why DRF Instead of Plain Django?

**DRF Advantages:**
- Serialization/deserialization
- Validation
- Browsable API
- Throttling/permissions
- Better error handling

**Plain Django would require:**
- Manual JSON parsing
- Manual validation
- Manual error responses
- More code!

---

## Interview Questions & Answers

### Technical Questions

#### Q1: "Explain how the auto-registration works. Walk me through what happens when Python reads the MinTotalRule class."

**Answer:**
"Great question! The auto-registration uses Python's metaclass system. Here's exactly what happens:

1. **Class Definition:** When Python encounters `class MinTotalRule(BaseRule)`, it needs to create the class object.

2. **Metaclass Invocation:** Since BaseRule has `metaclass=RuleMeta`, Python calls `RuleMeta.__new__()` instead of the default `type.__new__()`.

3. **Registration Logic:** Inside `RuleMeta.__new__()`:
   ```python
   if name != 'BaseRule' and 'name' in attrs and attrs['name']:
       RuleRegistry.register(attrs['name'], cls)
   ```
   This checks if the class has a `name` attribute and isn't the base class itself.

4. **Registry Storage:** `RuleRegistry.register()` adds the class to a dictionary:
   ```python
   _rules['min_total_100'] = MinTotalRule
   ```

5. **Completion:** The class is created and returned, now registered in the system.

The beauty is this happens **at import time**, not runtime. The moment Django loads the `order_rules.py` file, all rules are registered. No explicit initialization needed!

**Follow-up insight:** This is the same pattern Django uses for admin registration with `@admin.register`, and it's why we need the `ready()` method in `apps.py` to ensure rules are imported on startup."

---

#### Q2: "What would you do if a rule's evaluation was slow and blocking the API response?"

**Answer:**
"Excellent question about performance optimization. I'd approach this systematically:

**1. Measure First:**
```python
import time
start = time.time()
result = rule.evaluate(order)
elapsed = time.time() - start
logger.info(f"Rule {rule.name} took {elapsed}s")
```

**2. Short-term Solutions:**

**Caching:** For rules that depend only on order data:
```python
from django.core.cache import cache

class ExpensiveRule(BaseRule):
    def evaluate(self, order):
        cache_key = f'rule_{self.name}_{order.id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        result = self._expensive_calculation(order)
        cache.set(cache_key, result, timeout=300)  # 5 min
        return result
```

**Database Optimization:**
```python
# If rule needs related data, use select_related/prefetch_related
order = Order.objects.select_related('customer').get(id=order_id)
```

**3. Long-term Solutions:**

**Async Evaluation (Celery):**
```python
from celery import shared_task

@shared_task
def evaluate_rules_async(order_id, rule_names):
    order = Order.objects.get(id=order_id)
    engine = RuleEngine()
    return engine.evaluate_rules(order, rule_names)

# In view:
task = evaluate_rules_async.delay(order_id, rule_names)
return Response({'task_id': task.id}, status=202)
```

**Pre-computation:** Store rule results in database:
```python
class OrderRuleResult(models.Model):
    order = models.ForeignKey(Order)
    rule_name = models.CharField()
    result = models.BooleanField()
    evaluated_at = models.DateTimeField()
```

**4. Rule-Specific Optimizations:**

For example, the divisible_by_5 rule could be pre-computed:
```python
class Order(models.Model):
    total = models.DecimalField()
    divisible_by_five = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.divisible_by_five = (self.total % 5 == 0)
        super().save(*args, **kwargs)
```

**My recommendation would depend on:**
- How slow is 'slow'? (>100ms? >1s?)
- How often is the rule evaluated?
- Is the slowness from computation or I/O?
- What are the caching implications?"

---

#### Q3: "How would you add authentication to this API?"

**Answer:**
"I'd implement token-based authentication using Django REST Framework's built-in features. Here's my approach:

**1. Add JWT Authentication:**
```bash
pip install djangorestframework-simplejwt
```

**2. Configure settings.py:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**3. Add token endpoints:**
```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('rules/', include('rules.urls')),
]
```

**4. Update views with permissions:**
```python
from rest_framework.permissions import IsAuthenticated

class RuleCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # User must be authenticated
        pass
```

**5. For different permission levels:**
```python
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

**6. Usage by clients:**
```python
# Get token
POST /api/token/
{
    "username": "user",
    "password": "pass"
}
# Returns: {"access": "eyJ...", "refresh": "eyJ..."}

# Use token
POST /rules/check/
Authorization: Bearer eyJ...
{
    "order_id": 1,
    "rules": ["min_total_100"]
}
```

**Additional considerations:**
- API keys for service-to-service communication
- Rate limiting per user
- OAuth2 for third-party integrations
- Audit logging of authenticated requests"

---

#### Q4: "Walk me through how you'd add a new rule that checks if an order was placed on a weekend."

**Answer:**
"Perfect example of the extensibility of this design! Here's exactly what I'd do:

**Step 1: Create the rule class** (only file to modify!)
```python
# rules/order_rules.py

from datetime import datetime

class WeekendOrderRule(BaseRule):
    name = "is_weekend_order"
    description = "Validates that order was placed on a weekend"

    def evaluate(self, order) -> bool:
        # Saturday = 5, Sunday = 6
        return order.created_at.weekday() in [5, 6]
```

**That's literally it!** The rule is now:
- ✅ Automatically registered
- ✅ Available via API
- ✅ Shows up in GET /rules/
- ✅ Can be used in POST /rules/check/

**No other files need modification because:**
1. The metaclass registers it automatically
2. The registry system discovers it
3. The API views are generic

**Step 2: Test it immediately:**
```bash
curl POST https://pluggable-rule-engine.onrender.com/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["is_weekend_order"]}'
```

**Step 3: Write tests** (best practice):
```python
# rules/tests.py

def test_weekend_order_rule(self):
    # Create order on Saturday
    saturday_order = Order.objects.create(
        total=Decimal('100.00'),
        items_count=1
    )
    saturday_order.created_at = datetime(2024, 1, 6, 10, 0)  # Saturday
    saturday_order.save()

    rule = WeekendOrderRule()
    self.assertTrue(rule.evaluate(saturday_order))
```

**Step 4: Document it:**
```python
# config/urls.py
description="""
Available Rules:
- is_weekend_order: Order placed on Saturday or Sunday
...
"""
```

**This demonstrates:**
- Open/Closed Principle (open for extension, closed for modification)
- The power of the metaclass pattern
- Why this design is 'pluggable'

**More complex example - external API call:**
```python
class FraudCheckRule(BaseRule):
    name = "fraud_check"
    description = "Checks order against fraud detection service"

    def evaluate(self, order) -> bool:
        import requests
        response = requests.post('https://fraud-api.com/check', json={
            'order_id': order.id,
            'total': float(order.total)
        })
        return response.json()['is_safe']
```

Again, just add the class - no infrastructure changes needed!"

---

#### Q5: "How would you handle a scenario where evaluating all rules at once is too expensive?"

**Answer:**
"Great performance question! I'd implement lazy evaluation with short-circuiting. Here's my approach:

**Current Implementation (Eager Evaluation):**
```python
def evaluate_rules(self, order, rule_names):
    results = {}
    for rule_name in rule_names:
        rule = RuleRegistry.get_rule(rule_name)()
        results[rule_name] = rule.evaluate(order)  # Always evaluates all
    return {'passed': all(results.values()), 'details': results}
```

**Problem:** If we have 10 rules and the first one fails, we still evaluate the remaining 9.

**Solution 1: Short-Circuit Evaluation (AND logic)**
```python
class RuleEngine:
    def evaluate_rules(self, order, rule_names, short_circuit=False):
        results = {}

        for rule_name in rule_names:
            rule = RuleRegistry.get_rule(rule_name)()
            result = rule.evaluate(order)
            results[rule_name] = result

            # Stop if rule fails and short-circuit is enabled
            if short_circuit and not result:
                break

        return {'passed': all(results.values()), 'details': results}
```

**Solution 2: Priority-Based Evaluation**
```python
class BaseRule:
    priority = 100  # Lower = evaluated first

class ExpensiveRule(BaseRule):
    priority = 200  # Evaluated last

def evaluate_rules(self, order, rule_names):
    # Sort by priority
    rules = [(name, RuleRegistry.get_rule(name)) for name in rule_names]
    rules.sort(key=lambda x: x[1].priority)

    results = {}
    for rule_name, rule_class in rules:
        results[rule_name] = rule_class().evaluate(order)
```

**Solution 3: Async Parallel Evaluation**
```python
import asyncio

async def evaluate_rule_async(rule_name, order):
    rule = RuleRegistry.get_rule(rule_name)()
    return rule_name, rule.evaluate(order)

async def evaluate_rules_parallel(self, order, rule_names):
    tasks = [evaluate_rule_async(name, order) for name in rule_names]
    results = await asyncio.gather(*tasks)
    return dict(results)
```

**Solution 4: Tiered Evaluation**
```python
class BaseRule:
    tier = 1  # 1=fast, 2=medium, 3=slow

def evaluate_rules_tiered(self, order, rule_names):
    rules_by_tier = defaultdict(list)
    for name in rule_names:
        rule = RuleRegistry.get_rule(name)
        rules_by_tier[rule.tier].append((name, rule))

    results = {}
    for tier in sorted(rules_by_tier.keys()):
        tier_results = self._evaluate_tier(order, rules_by_tier[tier])
        results.update(tier_results)

        # If fast checks fail, skip expensive ones
        if tier == 1 and not all(tier_results.values()):
            break

    return results
```

**Solution 5: Result Caching**
```python
from functools import lru_cache

class BaseRule:
    @lru_cache(maxsize=1000)
    def evaluate(self, order):
        # Cached based on (rule, order) tuple
        return self._do_evaluation(order)
```

**My recommendation:**
1. Start with priority-based evaluation (cheap checks first)
2. Add short-circuiting for fail-fast scenarios
3. Use caching for frequently-evaluated rules
4. Consider async for I/O-bound rules (API calls)
5. Monitor with logging to identify bottlenecks

**Trade-offs:**
- Short-circuiting: Faster but incomplete results
- Parallel: Faster but more complex, harder to debug
- Caching: Fast but stale data risk"

---

#### Q6: "How did you ensure thread safety in the RuleRegistry?"

**Answer:**
"Excellent question! Let me walk through the thread safety considerations:

**Current Implementation:**
```python
class RuleRegistry:
    _rules: Dict[str, Type['BaseRule']] = {}  # Class variable (shared)
```

**Is it thread-safe?** Yes, but let me explain why:

**1. Registration happens at import time:**
```python
# When Django starts:
class MinTotalRule(BaseRule):  # Metaclass registers during class creation
    name = "min_total_100"
```

This happens **once**, before any worker threads are created. The `_rules` dictionary is fully populated before any requests are handled.

**2. Read-only during runtime:**
```python
def evaluate_rules(self, order, rule_names):
    for rule_name in rule_names:
        rule_class = RuleRegistry.get_rule(rule_name)  # Only reads, never writes
```

Reading from a dict is thread-safe in CPython due to the GIL (Global Interpreter Lock).

**However, if we needed runtime registration** (which we don't), I'd use locks:

```python
import threading

class RuleRegistry:
    _rules: Dict[str, Type['BaseRule']] = {}
    _lock = threading.RLock()  # Reentrant lock

    @classmethod
    def register(cls, name: str, rule_class: Type['BaseRule']) -> None:
        with cls._lock:
            if name in cls._rules:
                logger.warning(f"Rule '{name}' is being overridden")
            cls._rules[name] = rule_class

    @classmethod
    def get_rule(cls, name: str) -> Type['BaseRule']:
        # No lock needed for reads in CPython, but good practice:
        with cls._lock:
            if name not in cls._rules:
                raise KeyError(f"Rule '{name}' not found")
            return cls._rules[name]
```

**Alternative: Use threading.local for rule instances:**
```python
import threading

class RuleEngine:
    def __init__(self):
        self._local = threading.local()

    def get_rule_instance(self, rule_name):
        # Each thread gets its own rule instances
        if not hasattr(self._local, 'instances'):
            self._local.instances = {}

        if rule_name not in self._local.instances:
            rule_class = RuleRegistry.get_rule(rule_name)
            self._local.instances[rule_name] = rule_class()

        return self._local.instances[rule_name]
```

**Why thread safety matters here:**
- Gunicorn uses multiple worker processes (process-based, not thread-based by default)
- Each process has its own memory space, so no shared state issues
- But if using `--threads` flag or async workers, thread safety becomes critical

**In production with Gunicorn:**
```bash
gunicorn --workers 3 --threads 2 config.wsgi
# 3 processes × 2 threads = 6 concurrent handlers
```

Each process has its own `_rules` dict, but threads within a process share it.

**Best practices I followed:**
1. Initialize registry at import time (before threading)
2. Make registry read-only after initialization
3. Stateless rule instances (no shared mutable state)
4. Each request gets fresh rule instances

**If rules had state:**
```python
class StatefulRule(BaseRule):
    def __init__(self):
        self.call_count = 0  # ❌ Not thread-safe!

    def evaluate(self, order):
        self.call_count += 1  # Race condition!
        return True

# Better:
class StatelessRule(BaseRule):
    def evaluate(self, order):
        # No mutable state
        return order.total > 100  # ✅ Thread-safe
```

**Summary:** The current implementation is thread-safe because:
1. Registration happens once at startup
2. Runtime is read-only
3. Rule instances are stateless
4. Each request creates new instances"

---

### Design & Architecture Questions

#### Q7: "Why did you choose REST over GraphQL for this API?"

**Answer:**
"Great question! I chose REST for several specific reasons:

**1. Requirements Alignment:**
The task specification explicitly requested a REST endpoint:
```
POST /rules/check/
```
So REST was the natural choice to meet requirements.

**2. Simplicity for Use Case:**
This API has a simple, well-defined structure:
- List rules: GET /rules/
- Check rules: POST /rules/check/

GraphQL would be overkill because:
- No complex nested relationships
- No need for flexible queries
- Clients know exactly what data they need

**3. Caching Benefits:**
REST leverages HTTP caching:
```python
# GET /rules/ can be cached
Cache-Control: public, max-age=3600
```

GraphQL typically uses POST for everything, bypassing HTTP caching.

**4. Documentation:**
REST + Swagger provides excellent interactive docs out-of-the-box:
- Try-it-out functionality
- Auto-generated from code
- Standard OpenAPI format

GraphQL requires additional tools like GraphiQL.

**5. Learning Curve:**
REST is more widely understood. Anyone can test it with curl:
```bash
curl POST /rules/check/ -d '{"order_id": 1, "rules": ["min_total_100"]}'
```

**When I WOULD choose GraphQL:**

**Example 1: Complex nested data**
```graphql
query {
  order(id: 1) {
    total
    items {
      product {
        category {
          name
        }
      }
    }
    customer {
      address {
        country
      }
    }
  }
}
```

**Example 2: Mobile app with varying data needs**
- iOS app needs different fields than Android
- Reduce over-fetching on slow connections

**Example 3: Aggregating multiple REST APIs**
GraphQL acts as a gateway, client makes one query instead of multiple REST calls.

**Trade-offs I considered:**

| Aspect | REST | GraphQL |
|--------|------|---------|
| Caching | ✅ HTTP caching | ❌ Harder to cache |
| Tooling | ✅ Mature (Swagger) | ⚠️ Newer tooling |
| Over-fetching | ❌ Fixed responses | ✅ Request only what you need |
| Complexity | ✅ Simple | ❌ More complex |
| Versioning | ❌ Need /v1/, /v2/ | ✅ Schema evolution |

**For this specific project:**
- Simple data model (just orders)
- Well-defined operations
- Need HTTP caching for performance
- Want instant Swagger documentation
- Target audience familiar with REST

**Conclusion:** REST was the right choice here, but I'd recommend GraphQL for a larger e-commerce platform with complex product catalogs, user profiles, and varying client needs."

---

#### Q8: "How would you modify this to support multiple tenants (multi-tenancy)?"

**Answer:**
"Excellent architectural question! I'd implement row-level multi-tenancy. Here's my comprehensive approach:

**Step 1: Add Tenant Model**
```python
# tenants/models.py
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Tenant-specific configuration
    max_orders = models.IntegerField(default=1000)
    allowed_rules = models.JSONField(default=list)  # Restrict which rules tenant can use

class TenantUser(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
```

**Step 2: Modify Order Model**
```python
# orders/models.py
class Order(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Add this
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items_count = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['tenant', '-created_at']),  # Composite index
            models.Index(fields=['tenant', 'total']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'id'],
                name='unique_order_per_tenant'
            )
        ]
```

**Step 3: Tenant-Aware Manager**
```python
class TenantManager(models.Manager):
    def get_queryset(self):
        # Automatically filter by current tenant
        tenant = get_current_tenant()
        if tenant:
            return super().get_queryset().filter(tenant=tenant)
        return super().get_queryset()

class Order(models.Model):
    # ...
    objects = TenantManager()
    all_objects = models.Manager()  # Bypass tenant filtering if needed
```

**Step 4: Tenant Middleware**
```python
# middleware/tenant.py
import threading

_thread_local = threading.local()

def get_current_tenant():
    return getattr(_thread_local, 'tenant', None)

def set_current_tenant(tenant):
    _thread_local.tenant = tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Option 1: Subdomain-based
        host = request.get_host().split(':')[0]
        if host.endswith('.myapp.com'):
            slug = host.split('.')[0]  # tenant1.myapp.com -> tenant1
            tenant = Tenant.objects.get(slug=slug)

        # Option 2: Header-based (for API)
        # tenant_id = request.headers.get('X-Tenant-ID')
        # tenant = Tenant.objects.get(id=tenant_id)

        # Option 3: JWT claim
        # tenant_id = request.user.tenant_id
        # tenant = Tenant.objects.get(id=tenant_id)

        set_current_tenant(tenant)
        response = self.get_response(request)
        set_current_tenant(None)  # Clean up
        return response
```

**Step 5: Tenant-Aware Views**
```python
class RuleCheckView(APIView):
    def post(self, request):
        tenant = get_current_tenant()

        # Check tenant's allowed rules
        requested_rules = request.data['rules']
        if tenant.allowed_rules and not all(r in tenant.allowed_rules for r in requested_rules):
            return Response({
                'error': 'Rule not allowed for your tenant'
            }, status=403)

        # Automatically filtered by tenant
        order = Order.objects.get(id=request.data['order_id'])

        # Rest of logic...
```

**Step 6: Tenant-Specific Rules** (Advanced)
```python
class BaseRule:
    tenant_specific = False  # New attribute

    def evaluate(self, order) -> bool:
        pass

class TenantCustomRule(BaseRule):
    name = "tenant_custom_rule"
    tenant_specific = True

    def evaluate(self, order) -> bool:
        tenant = get_current_tenant()
        # Load tenant-specific logic from database or config
        config = TenantRuleConfig.objects.get(
            tenant=tenant,
            rule_name=self.name
        )
        return order.total > config.threshold
```

**Step 7: Database Strategies**

**Option A: Shared Database (Current approach)**
- All tenants in one database
- Tenant ID on every table
- Pros: Simple, cost-effective
- Cons: Security risk, harder to scale

**Option B: Separate Databases per Tenant**
```python
class TenantRouter:
    def db_for_read(self, model, **hints):
        tenant = get_current_tenant()
        if tenant:
            return f'tenant_{tenant.id}'
        return 'default'

    def db_for_write(self, model, **hints):
        tenant = get_current_tenant()
        if tenant:
            return f'tenant_{tenant.id}'
        return 'default'

# settings.py
DATABASES = {
    'default': {...},
    'tenant_1': {...},
    'tenant_2': {...},
}
```
- Pros: Complete isolation, easier to scale
- Cons: More complex, expensive

**Option C: Hybrid (Schema per tenant in PostgreSQL)**
```python
from django.db import connection

class TenantMiddleware:
    def __call__(self, request):
        tenant = self.get_tenant(request)

        # Switch to tenant's schema
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO tenant_{tenant.id}")

        response = self.get_response(request)

        # Reset to public schema
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")

        return response
```

**Step 8: Testing Multi-Tenancy**
```python
class TestTenantIsolation(TestCase):
    def setUp(self):
        self.tenant1 = Tenant.objects.create(name="Tenant 1")
        self.tenant2 = Tenant.objects.create(name="Tenant 2")

        set_current_tenant(self.tenant1)
        self.order1 = Order.objects.create(total=100, items_count=2)

        set_current_tenant(self.tenant2)
        self.order2 = Order.objects.create(total=200, items_count=3)

    def test_tenant_isolation(self):
        set_current_tenant(self.tenant1)
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first(), self.order1)

        set_current_tenant(self.tenant2)
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first(), self.order2)
```

**Step 9: Tenant-Aware Admin**
```python
class TenantAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)

@admin.register(Order)
class OrderAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'tenant', 'total', 'items_count')
    list_filter = ('tenant',)
```

**My Recommendation:**
For this project, I'd start with **Option A (Shared DB)** because:
1. Simpler to implement
2. Cost-effective
3. Easy to migrate later
4. Sufficient for most use cases

Then evolve to Option C (Schemas) if:
- Need stronger isolation
- Have performance issues
- Regulatory compliance requires it

**Implementation Priority:**
1. Add tenant model and foreign keys (Week 1)
2. Implement middleware and threading (Week 1)
3. Update views and managers (Week 2)
4. Add tenant-specific rules (Week 3)
5. Implement admin isolation (Week 3)
6. Comprehensive testing (Week 4)"

---

### Problem-Solving Questions

#### Q9: "If the API suddenly started returning 500 errors in production, how would you debug it?"

**Answer:**
"Great question about production debugging! I'd follow a systematic approach:

**Step 1: Immediate Triage (First 5 minutes)**

**Check service status:**
```bash
# Render dashboard - check if service is running
# Look at metrics: CPU, memory, request rate

# Check recent logs
render logs --tail 100
```

**Look for the error:**
```bash
# Filter for 500 errors
render logs | grep "500"
render logs | grep "ERROR"
render logs | grep "Traceback"
```

**Common immediate issues:**
- Database connection lost
- Out of memory
- Dependency service down
- Recent deployment broke something

**Step 2: Check Monitoring & Logs**

**Application logs:**
```python
# Our logging configuration logs to console
# Look for:
ERROR 2024-01-20 15:30:42 rules Rule not found: invalid_rule
ERROR 2024-01-20 15:30:42 django.db.utils OperationalError: database is locked
```

**Key things to look for:**
```bash
# Database errors
grep "OperationalError\|IntegrityError" logs.txt

# Import errors
grep "ImportError\|ModuleNotFoundError" logs.txt

# Memory issues
grep "MemoryError\|killed" logs.txt
```

**Step 3: Reproduce Locally**

**Get production data:**
```bash
# Export recent database state
render run python manage.py dumpdata > prod_data.json

# Load locally
python manage.py loaddata prod_data.json
```

**Test the failing request:**
```bash
# If error happens on specific endpoint
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["min_total_100"]}'
```

**Step 4: Enable Debug Mode (Carefully!)**

**Temporarily add more logging:**
```python
# rules/views.py
import logging
logger = logging.getLogger(__name__)

def post(self, request):
    logger.error(f"Received request: {request.data}")
    try:
        serializer = RuleCheckRequestSerializer(data=request.data)
        logger.error(f"Serializer valid: {serializer.is_valid()}")
        if not serializer.is_valid():
            logger.error(f"Errors: {serializer.errors}")
            # ...
    except Exception as e:
        logger.error(f"Exception: {e}", exc_info=True)
        raise
```

**Deploy with extra logging:**
```bash
git commit -m "debug: add detailed logging for 500 errors"
git push
# Render auto-deploys
```

**Step 5: Common 500 Error Scenarios & Fixes**

**Scenario 1: Database Connection**
```python
# Error: django.db.utils.OperationalError: FATAL: sorry, too many clients

# Fix: Check connection pooling
# settings.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 60,  # Reduce from 600
    }
}
```

**Scenario 2: Import Error After Deployment**
```python
# Error: ImportError: cannot import name 'BaseRule' from 'rules.engine'

# Cause: Circular import or missing __init__.py
# Fix: Check import order
# rules/__init__.py
default_app_config = 'rules.apps.RulesConfig'
```

**Scenario 3: Missing Migration**
```python
# Error: django.db.utils.OperationalError: no such table: orders_order

# Fix: Ensure migrations ran
render run python manage.py migrate --check
render run python manage.py showmigrations
```

**Scenario 4: Memory Limit Exceeded**
```bash
# Error: Killed (137)

# Check Render plan limits
# Free tier: 512MB RAM

# Fix: Optimize queries
Order.objects.select_related('tenant').all()  # Prevent N+1 queries
```

**Scenario 5: Unhandled Exception in Rule**
```python
# Error: ZeroDivisionError in DivisibleByFiveRule

# Fix: Add error handling
class DivisibleByFiveRule(BaseRule):
    def evaluate(self, order) -> bool:
        try:
            return order.total % Decimal('5.00') == Decimal('0.00')
        except (TypeError, ValueError, ZeroDivisionError) as e:
            logger.error(f"Error in divisible_by_5: {e}")
            return False  # Fail safe
```

**Step 6: Quick Rollback**

**If recent deployment caused it:**
```bash
# Render dashboard -> Deployments -> Rollback to previous

# Or via git:
git revert HEAD
git push
```

**Step 7: Monitoring Setup** (Prevent future issues)

**Add Sentry for error tracking:**
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    environment="production",
)
```

**Add health check endpoint:**
```python
# rules/views.py
class HealthCheckView(APIView):
    def get(self, request):
        # Check database
        try:
            Order.objects.count()
            db_status = "ok"
        except Exception as e:
            db_status = f"error: {e}"

        # Check rules registered
        rules_count = len(RuleRegistry.get_all_rules())

        return Response({
            'status': 'healthy' if db_status == 'ok' else 'unhealthy',
            'database': db_status,
            'rules_registered': rules_count,
            'timestamp': datetime.now().isoformat()
        })
```

**Add alerting:**
```bash
# Set up Render to alert on:
# - 5xx error rate > 1%
# - Response time > 1s
# - Memory usage > 80%
```

**Step 8: Post-Mortem**

**Document the incident:**
```markdown
# Incident: 500 Errors on 2024-01-20

## Timeline
- 15:30 UTC: Errors started
- 15:35 UTC: Identified database connection issue
- 15:40 UTC: Reduced CONN_MAX_AGE
- 15:42 UTC: Errors stopped

## Root Cause
Database connection pool exhausted due to sudden traffic spike

## Fix
Reduced connection lifetime and added connection pooling

## Prevention
- Added monitoring for connection pool usage
- Set up auto-scaling
- Added rate limiting
```

**My systematic approach:**
1. **Triage**: Check if service is running, look at logs
2. **Identify**: Find the specific error message
3. **Reproduce**: Test locally with production data
4. **Debug**: Add detailed logging if needed
5. **Fix**: Apply targeted fix
6. **Rollback**: If fix not quick, rollback and investigate offline
7. **Monitor**: Ensure fix works, add monitoring to prevent recurrence
8. **Document**: Post-mortem for team learning

**Time allocation:**
- First 5 min: Identify error
- Next 10 min: Try quick fixes (restart, rollback)
- Next 20 min: Deep investigation
- If not fixed in 35 min: Rollback and investigate offline"

---

#### Q10: "How would you implement rate limiting for this API?"

**Answer:**
"Excellent question about API protection! I'd implement a multi-layered approach:

**Layer 1: Django Rate Limiting (Application Level)**

**Install django-ratelimit:**
```bash
pip install django-ratelimit
```

**Apply to views:**
```python
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='100/h', method='POST'), name='post')
class RuleCheckView(APIView):
    def post(self, request):
        # If rate limit exceeded, raises Ratelimited exception
        # ...
```

**Custom rate limit handler:**
```python
# middleware/ratelimit.py
from django_ratelimit.exceptions import Ratelimited

class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Ratelimited:
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'detail': 'You have exceeded the rate limit. Please try again later.',
                'retry_after': 3600  # seconds
            }, status=429)
        return response
```

**Layer 2: DRF Throttling (More Flexible)**

**settings.py:**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}
```

**Custom throttle classes:**
```python
from rest_framework.throttling import SimpleRateThrottle

class RuleCheckThrottle(SimpleRateThrottle):
    scope = 'rule_check'

    def get_cache_key(self, request, view):
        # Rate limit by IP and endpoint
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'
    rate = '10/minute'  # Allow bursts, but limit sustained load

class SustainedRateThrottle(SimpleRateThrottle):
    scope = 'sustained'
    rate = '100/hour'  # Overall limit
```

**Apply to specific view:**
```python
class RuleCheckView(APIView):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        # Automatically throttled
        pass
```

**Layer 3: Redis-Based Rate Limiting (Production)**

**Why Redis?**
- Fast (in-memory)
- Distributed (works across multiple servers)
- Built-in expiration

**Install:**
```bash
pip install redis django-redis
```

**Configure:**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Custom Redis throttle:**
```python
from django.core.cache import cache
import time

class RedisRateLimiter:
    def __init__(self, key_prefix, limit, period):
        self.key_prefix = key_prefix
        self.limit = limit
        self.period = period

    def is_allowed(self, identifier):
        key = f"{self.key_prefix}:{identifier}"

        # Get current count
        count = cache.get(key, 0)

        if count >= self.limit:
            return False

        # Increment
        if count == 0:
            cache.set(key, 1, self.period)
        else:
            cache.incr(key)

        return True

    def get_retry_after(self, identifier):
        key = f"{self.key_prefix}:{identifier}"
        ttl = cache.ttl(key)
        return ttl if ttl > 0 else 0

# Usage in view:
limiter = RedisRateLimiter('rule_check', limit=100, period=3600)

def post(self, request):
    identifier = request.META.get('REMOTE_ADDR')

    if not limiter.is_allowed(identifier):
        return Response({
            'error': 'Rate limit exceeded',
            'retry_after': limiter.get_retry_after(identifier)
        }, status=429)

    # Process request...
```

**Layer 4: Tiered Rate Limits**

**Different limits for different user types:**
```python
class TieredRateThrottle(SimpleRateThrottle):
    def get_rate(self):
        if not self.request.user.is_authenticated:
            return '100/hour'  # Anonymous users

        user = self.request.user

        if user.tier == 'free':
            return '100/hour'
        elif user.tier == 'pro':
            return '1000/hour'
        elif user.tier == 'enterprise':
            return '10000/hour'

        return '100/hour'  # Default
```

**Layer 5: Nginx Rate Limiting (Infrastructure Level)**

**nginx.conf:**
```nginx
http {
    # Define rate limit zone
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        location /rules/ {
            limit_req zone=api_limit burst=20 nodelay;
            limit_req_status 429;

            proxy_pass http://django;
        }
    }
}
```

**Benefits:**
- Protects Django from even receiving requests
- Very fast (nginx level)
- Prevents DDoS

**Layer 6: Advanced Strategies**

**Token Bucket Algorithm:**
```python
class TokenBucketThrottle:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second

    def consume(self, identifier, tokens=1):
        key = f"bucket:{identifier}"

        # Get current bucket state
        data = cache.get(key, {
            'tokens': self.capacity,
            'last_refill': time.time()
        })

        # Refill tokens based on time passed
        now = time.time()
        time_passed = now - data['last_refill']
        tokens_to_add = time_passed * self.refill_rate

        data['tokens'] = min(
            self.capacity,
            data['tokens'] + tokens_to_add
        )
        data['last_refill'] = now

        # Check if enough tokens
        if data['tokens'] >= tokens:
            data['tokens'] -= tokens
            cache.set(key, data, 3600)
            return True

        cache.set(key, data, 3600)
        return False
```

**Sliding Window:**
```python
class SlidingWindowThrottle:
    def is_allowed(self, identifier):
        key = f"requests:{identifier}"
        now = time.time()
        window_start = now - 3600  # 1 hour window

        # Store timestamps of requests
        pipe = cache.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)  # Remove old
        pipe.zadd(key, {str(now): now})  # Add current
        pipe.zcount(key, window_start, now)  # Count in window
        pipe.expire(key, 3600)

        results = pipe.execute()
        count = results[2]

        return count <= 100  # Limit
```

**Layer 7: Monitoring & Alerting**

**Track rate limit hits:**
```python
import logging

logger = logging.getLogger('ratelimit')

class MonitoredRateThrottle(SimpleRateThrottle):
    def throttle_failure(self):
        logger.warning(f"Rate limit exceeded: {self.get_ident(self.request)}")

        # Increment metric
        cache.incr('ratelimit_hits')

        return super().throttle_failure()
```

**Alert if too many rate limits:**
```python
# Check every minute
hits = cache.get('ratelimit_hits', 0)
if hits > 100:  # More than 100 rate limit hits per minute
    send_alert("High rate limit hits, possible attack")
```

**Layer 8: Response Headers**

**Add rate limit info to responses:**
```python
class RateLimitHeaderMiddleware:
    def __call__(self, request):
        response = self.get_response(request)

        # Add rate limit headers
        limiter = getattr(request, 'rate_limiter', None)
        if limiter:
            response['X-RateLimit-Limit'] = limiter.limit
            response['X-RateLimit-Remaining'] = limiter.remaining
            response['X-RateLimit-Reset'] = limiter.reset_time

        return response
```

**My Recommended Implementation:**

**For this project (starting simple):**
```python
# Install
pip install django-ratelimit

# Apply
@method_decorator(ratelimit(key='ip', rate='100/h'), name='post')
class RuleCheckView(APIView):
    pass
```

**For production (scale up):**
1. Redis-based throttling
2. Tiered limits (free/pro/enterprise)
3. Nginx rate limiting for DDoS protection
4. Monitoring and alerting
5. Graceful error messages with retry-after

**Trade-offs:**
- Simple (django-ratelimit): Easy but not distributed
- Redis: Fast and distributed but requires infrastructure
- Nginx: Very fast but less flexible
- Token bucket: Allows bursts but more complex

Would you like me to walk through implementing any specific layer in detail?"

---

## Talking Points

### Opening Strong

**"Tell me about your project"**

**Your response:**
"I built a production-ready Django REST API featuring an auto-registering rule engine for order validation. The key innovation is using Python metaclasses to automatically register rules - developers can add new validation rules by simply creating a class, with zero configuration needed.

The system is fully deployed on Render with CI/CD via GitHub Actions, comprehensive test coverage, and interactive Swagger documentation. It demonstrates advanced Python patterns, RESTful API design, and production deployment practices.

Would you like me to walk through the architecture or dive into the metaclass implementation?"

### Key Strengths to Highlight

1. **Technical Innovation:**
   - Metaclass pattern for auto-registration
   - Zero-configuration extensibility
   - Open/Closed principle in action

2. **Production Quality:**
   - 18 comprehensive tests
   - CI/CD pipeline
   - Docker containerization
   - Environment-based configuration
   - Comprehensive error handling
   - Logging and monitoring

3. **API Design:**
   - RESTful best practices
   - Clear error messages
   - Swagger documentation
   - Proper HTTP status codes
   - Input validation

4. **Development Process:**
   - Professional git commit history
   - Clean code organization
   - Thorough documentation
   - Deployment automation

### Questions to Ask Them

1. **About their tech stack:**
   "I noticed you use [technology]. How do you handle rule/policy management in your current system?"

2. **About scale:**
   "What's your typical request volume? I designed this for extensibility - how might you scale a system like this?"

3. **About team:**
   "How does your team approach code reviews and testing? I'm curious about your development workflow."

4. **About architecture:**
   "Do you use microservices or monoliths? How would you see a rule engine fitting into your architecture?"

### Common Interview Red Flags to Avoid

❌ "I just followed a tutorial"
✅ "I made deliberate architectural decisions based on..."

❌ "I don't know why I did it that way"
✅ "I chose this approach because... but I considered alternatives like..."

❌ "That's the only way I know"
✅ "There are multiple approaches - I chose this because..."

❌ "I've never thought about that"
✅ "That's interesting! Here's how I'd approach that problem..."

### Nervous? Remember:

1. **You built something impressive** - 13 professional commits, 18 passing tests, live deployment
2. **You understand the why** - Not just the how
3. **You can explain trade-offs** - Every decision has alternatives
4. **You're prepared** - You have this guide!

### Closing Strong

**"Do you have any questions for us?"**

**Great responses:**
- "How does your team approach technical debt and refactoring?"
- "What's your deployment frequency and process?"
- "How do you balance shipping features quickly with maintaining code quality?"
- "What would my first project be if I joined the team?"

---

## Final Tips

### Before the Interview

1. **Review this guide** - Especially architecture and questions
2. **Run the project locally** - Be able to demo it
3. **Test the live deployment** - Make sure it's working
4. **Re-read your code** - Be familiar with every file
5. **Practice explaining out loud** - Talk through the metaclass pattern

### During the Interview

1. **Think out loud** - Show your thought process
2. **Ask clarifying questions** - Better than guessing
3. **Draw diagrams** - Visual explanations help
4. **Admit unknowns** - "I don't know, but here's how I'd find out"
5. **Show enthusiasm** - You're excited about good code!

### Red Flag Questions They Might Ask

**"This looks overengineered for the requirements"**
- Response: "You're right that the basic requirements could be simpler. However, I wanted to demonstrate production-ready patterns and create a system that scales. The metaclass pattern showcases advanced Python, but I could also implement this with a simple decorator pattern. Would you like me to show both approaches?"

**"Why didn't you use [other technology]?"**
- Response: "That's a great alternative! I chose Django because [reasons], but [other technology] would work well too. The key principles - auto-registration, clean API design, test coverage - would apply regardless of framework."

### Good Luck!

You've built something impressive. You understand it deeply. You can explain the why, not just the how. You've got this! 🚀

---

**Last Updated:** November 2024
**Project:** Pluggable Rule Engine
**Author:** [Your Name]
**Repository:** https://github.com/William9701/Pluggable_Rule_Engine
