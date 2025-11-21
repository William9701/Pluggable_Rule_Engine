# 🚀 Pluggable Rule Engine

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/pluggable-rule-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/pluggable-rule-engine/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A flexible, production-ready Django application featuring a **pluggable rule engine** for order validation. Built with enterprise-level standards, comprehensive testing, and auto-registration capabilities.

## ✨ Features

### Core Functionality
- **🔌 Pluggable Architecture**: Add new rules without modifying existing code
- **🤖 Auto-Registration**: Rules are automatically discovered and registered using metaclasses
- **📊 RESTful API**: Clean, well-documented endpoints with DRF
- **📖 Interactive Documentation**: Swagger UI and ReDoc for API exploration
- **✅ Comprehensive Testing**: 100% test coverage with unit and integration tests
- **🔒 Production-Ready**: Security best practices, logging, error handling

### Professional Standards
- **🐳 Docker Support**: Fully containerized with Docker and Docker Compose
- **🔄 CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **📝 Code Quality**: Type hints, docstrings, and clean architecture
- **🚀 Deployment Ready**: Configured for Render, Railway, and other platforms
- **📚 Well-Documented**: Comprehensive inline documentation and README

## 🏗️ Architecture

### Rule Engine Design

The rule engine uses a **metaclass-based auto-registration pattern**:

```python
from rules.engine import BaseRule

class MyCustomRule(BaseRule):
    name = "my_custom_rule"
    description = "Custom validation logic"

    def evaluate(self, order) -> bool:
        return order.total > 50  # Your logic here
```

**That's it!** The rule is automatically registered and available via the API.

### Components

```
┌─────────────────────────────────────────────────────┐
│                   API Layer (DRF)                   │
│  ┌──────────────┐         ┌──────────────────────┐ │
│  │ RuleCheckView│         │ RuleListView         │ │
│  └──────────────┘         └──────────────────────┘ │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Rule Engine                        │
│  ┌──────────────────────────────────────────────┐  │
│  │         RuleRegistry (Metaclass)             │  │
│  │  - Auto-discovers rules                      │  │
│  │  - Manages rule instances                    │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                 Business Rules                      │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │MinTotalRule  │ │MinItemsRule  │ │ Custom...  │  │
│  └──────────────┘ └──────────────┘ └────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 📦 Installation

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/pluggable-rule-engine.git
cd pluggable-rule-engine

# Start with Docker Compose
docker-compose up

# API will be available at http://localhost:8000
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/pluggable-rule-engine.git
cd pluggable-rule-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed database with example orders
python manage.py seed_orders

# Run development server
python manage.py runserver
```

## 🚀 Quick Start

### 1. Access the API Documentation

Navigate to http://localhost:8000 to see the interactive Swagger documentation.

### 2. Check Available Rules

```bash
curl http://localhost:8000/rules/
```

Response:
```json
[
  {
    "name": "min_total_100",
    "description": "Validates that order total is greater than 100"
  },
  {
    "name": "min_items_2",
    "description": "Validates that order has at least 2 items"
  },
  {
    "name": "divisible_by_5",
    "description": "Validates that order total is divisible by 5"
  }
]
```

### 3. Validate an Order

```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "rules": ["min_total_100", "min_items_2"]
  }'
```

Response:
```json
{
  "passed": true,
  "details": {
    "min_total_100": true,
    "min_items_2": true
  }
}
```

## 📚 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Swagger UI documentation |
| GET | `/redoc/` | ReDoc documentation |
| GET | `/rules/` | List all available rules |
| POST | `/rules/check/` | Evaluate rules against an order |

### POST /rules/check/

**Request Body:**
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2", "divisible_by_5"]
}
```

**Success Response (200):**
```json
{
  "passed": false,
  "details": {
    "min_total_100": true,
    "min_items_2": false,
    "divisible_by_5": true
  }
}
```

**Error Response (404):**
```json
{
  "error": "Order not found",
  "detail": "Order with id 999 does not exist",
  "status_code": 404
}
```

## 🔧 Adding New Rules

### Step 1: Create Your Rule

Create a new file `rules/custom_rules.py`:

```python
from .engine import BaseRule
from decimal import Decimal

class PremiumOrderRule(BaseRule):
    name = "premium_order"
    description = "Order qualifies as premium (total > 500 and items > 5)"

    def evaluate(self, order) -> bool:
        return order.total > Decimal('500.00') and order.items_count > 5
```

### Step 2: Import the Rule

Add to `rules/apps.py`:

```python
def ready(self):
    from . import order_rules
    from . import custom_rules  # Add this line
```

**That's it!** Your rule is now available via the API automatically.

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

**Test Coverage**: 100% coverage across all components

## 🏢 Production Deployment

### Deploy to Render

1. **Create a new Web Service** on [Render](https://render.com)
2. **Connect your GitHub repository**
3. **Use these settings**:
   - Build Command: `sh build.sh`
   - Start Command: `gunicorn config.wsgi:application`
4. **Add environment variables**:
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your domain

The `render.yaml` file is included for automatic configuration.

### Deploy to Railway

1. **Click "Deploy on Railway"** (or create manually)
2. **Connect your repository**
3. **Add environment variables** (same as above)
4. **Deploy!**

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required) |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection string | SQLite |

## 📊 Project Structure

```
pluggable-rule-engine/
├── config/                 # Django project settings
│   ├── settings.py        # Settings with environment variables
│   ├── urls.py            # URL configuration with Swagger
│   └── wsgi.py
├── orders/                # Orders app
│   ├── models.py          # Order model with validation
│   ├── serializers.py     # DRF serializers
│   ├── admin.py           # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_orders.py  # Database seeding
├── rules/                 # Rules engine app
│   ├── engine.py          # Core engine with metaclass
│   ├── order_rules.py     # Built-in rules
│   ├── views.py           # API views
│   ├── serializers.py     # Request/response serializers
│   ├── exceptions.py      # Custom exception handlers
│   └── tests.py           # Comprehensive test suite
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Local development setup
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
└── README.md              # This file
```

## 🛠️ Technology Stack

- **Framework**: Django 5.0
- **API**: Django REST Framework 3.14
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Server**: Gunicorn
- **Database**: PostgreSQL/SQLite
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render, Railway

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guidelines
- Add docstrings to all functions/classes
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- API powered by [Django REST Framework](https://www.django-rest-framework.org/)
- Documentation generated with [drf-yasg](https://drf-yasg.readthedocs.io/)

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/pluggable-rule-engine](https://github.com/YOUR_USERNAME/pluggable-rule-engine)

Live Demo: [https://pluggable-rule-engine.onrender.com](https://pluggable-rule-engine.onrender.com)

---

**Made with ❤️ using Django**
