# 6-Minute Demo Script: Django Pluggable Rule Engine

## **INTRODUCTION (30 seconds)**

"Hi! I built a Django-based rule engine for validating e-commerce orders. The cool part is it uses Python metaclasses to automatically register new rules - meaning you can add features without changing existing code. It's live on Render right now with interactive Swagger documentation."

**Show:** https://pluggable-rule-engine.onrender.com

---

## **1. THE PROBLEM (45 seconds)**

"So imagine you're running an online store. You need to validate orders - maybe check if they meet a minimum total, have enough items, qualify for promotions, that kind of thing.

The traditional approach would be hardcoding if-statements everywhere. But what happens when business wants a new rule next week? You'd have to dig through the codebase, add more if-statements, test everything again.

My solution: a pluggable system where new rules just... appear. You write a class, and it automatically registers itself. No configuration files, no manual setup."

---

## **2. HOW IT WORKS: THE MAGIC BEHIND IT (90 seconds)**

**Open:** `rules/engine.py`

"Let me show you the core innovation. This is a Python metaclass - think of it as code that runs when you CREATE a class, not when you use it."

```python
class RuleMeta(ABCMeta):
    """Metaclass that auto-registers rule classes"""
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'BaseRule' and 'name' in attrs and attrs['name']:
            RuleRegistry.register(attrs['name'], cls)
        return cls
```

**Explain naturally:**
"So what's happening here? When Python creates a new rule class, this `__new__` method intercepts it. We check if it's a real rule - not just the base class - and if it has a name, we automatically add it to our central registry.

You'll notice it inherits from ABCMeta - that's Python's Abstract Base Class metaclass. We need that because we want to enforce that every rule MUST implement an `evaluate` method. If someone forgets, Python won't even let them create an instance. It's like a contract - you implement evaluate, or your code won't run.

Now look how simple creating a rule becomes."

**Open:** `rules/order_rules.py`

```python
class MinimumTotalRule(BaseRule):
    name = "min_total_100"
    description = "Order total must be greater than 100"

    def evaluate(self, order) -> bool:
        return order.total > Decimal('100.00')
```

**Explain:**
"That's it. Literally just this. Inherit from BaseRule, give it a name, implement evaluate. The metaclass takes care of registration.

When the app starts, you'll see in the logs: 'Registered rule: min_total_100'. It just works.

And because we used ABCMeta with the @abstractmethod decorator on BaseRule, if I forgot to write the evaluate method, Python would throw an error immediately saying 'Can't instantiate abstract class'. It catches bugs before they reach production."

**Why this is powerful:**
- **Zero configuration** - no registration boilerplate
- **Type-safe** - your IDE knows what methods exist
- **Fail-fast** - abstractmethod catches missing implementations
- **Thread-safe** - Python's GIL protects the registry
- **Extensible** - add rules without touching existing code

---

## **3. SEEING IT WORK: LIVE API (60 seconds)**

**Open Swagger UI:** https://pluggable-rule-engine.onrender.com

"Okay, so let's actually use this. The API has one main endpoint - you send an order ID and a list of rules to check."

**Demo Request:**
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2", "divisible_by_5"]
}
```

**Click Execute, show response:**
```json
{
  "passed": true,
  "details": {
    "min_total_100": true,
    "min_items_2": true,
    "divisible_by_5": true
  }
}
```

"Order 1 has a total of $150 and 3 items, so it passes all three rules. Notice we get both the overall result - 'passed: true' - and individual results for each rule.

Now watch what happens with order 2:"

**Demo Failure:**
```json
{
  "order_id": 2,
  "rules": ["min_total_100", "min_items_2"]
}
```

**Response:**
```json
{
  "passed": false,
  "details": {
    "min_total_100": false,
    "min_items_2": false
  }
}
```

"Order 2 only has $75.50 and 1 item. Both rules fail, so overall 'passed' is false. The engine evaluates each rule independently - if ANY rule fails, the overall check fails."

---

## **4. PROFESSIONAL TOUCHES: PRODUCTION-READY DESIGN (90 seconds)**

"Let me show you a few things that make this production-ready, not just a toy project."

**Open:** `orders/models.py`

```python
total = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.00'))]
)
```

**Explain:**
"See how I used DecimalField instead of FloatField? This is critical for money. FloatField has rounding errors - you've probably seen 0.1 + 0.2 equals 0.30000000004. DecimalField uses fixed-point arithmetic, so you never lose pennies. Financial calculations should ALWAYS use Decimal."

---

**Open:** `config/settings.py`

```python
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}
```

**Explain:**
"This is how we handle different environments. Locally, it uses SQLite - dead simple, no setup. In production on Render, it reads the DATABASE_URL environment variable and connects to PostgreSQL. Same code, zero changes. That's what dj_database_url does - parses connection strings automatically."

---

## **EXTRA DETAILS (If You Have Time)**

### **How Auto-Seeding Works**

**Open:** `orders/apps.py`

"When Django starts, it calls this ready() method. If the Order table is empty, it creates three demo orders. I wrapped it in try/except because during migrations, the table doesn't exist yet - this prevents crashes."

```python
def ready(self):
    try:
        from .models import Order
        if not Order.objects.exists():
            # Create 3 demo orders
    except (OperationalError, Exception):
        pass  # Table doesn't exist yet
```

### **Custom Exception Handler**

**Open:** `rules/exceptions.py`

"This intercepts all errors and formats them consistently. Without it, different exception types return different JSON structures. Now every error looks the same - predictable for frontend developers."

```python
def custom_exception_handler(exc, context):
    if isinstance(exc, Order.DoesNotExist):
        return Response({
            'error': 'Order not found',
            'detail': str(exc)
        }, status=404)
```


**Open:** `config/settings.py` (REST_FRAMEWORK section)

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'EXCEPTION_HANDLER': 'rules.exceptions.custom_exception_handler',
    'PAGE_SIZE': 100,
}
```

**Explain:**
"The REST Framework config does a few things:
- JSONRenderer ensures all responses are JSON
- BrowsableAPIRenderer adds that nice HTML interface you saw in Swagger
- Custom exception handler means all errors follow the same format - consistent API responses
- Pagination is set to 100 items per page, so when this scales to thousands of orders, it won't crash browsers"

---

## **5. DEPLOYMENT: ONE-CLICK TO PRODUCTION (60 seconds)**

**Open:** `render.yaml`

```yaml
services:
  - type: web
    name: pluggable-rule-engine
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_orders"
    startCommand: "gunicorn config.wsgi:application"
```

**Explain:**
"This is infrastructure as code. You push this to Render, and it knows exactly how to deploy.

The build command does everything in sequence:
1. Install dependencies
2. Collect static files - that's the CSS and JavaScript for the admin panel
3. Run migrations - create database tables
4. Seed demo orders - so the API has data to work with immediately

Then it starts Gunicorn, which is a production WSGI server. Way more robust than Django's development server.

The 'plan: free' line is critical - without it, Render asks for payment info. I learned that the hard way."

---

**Mention CI/CD:**
"I also set up GitHub Actions for continuous integration. Every push runs 18 automated tests - covering the registry, rule evaluation, and API endpoints. All passing."

---

## **6. DESIGN DECISIONS EXPLAINED (45 seconds)**

**Why Metaclass Instead of Decorators?**

"I could've used decorators, like:
```python
@register_rule('min_total_100')
class MinimumTotalRule:
    pass
```

But metaclasses are cleaner because:
- Registration happens automatically when Python imports the file
- You can't forget to add the decorator - inheritance enforces it
- Less visual clutter in your code"

---

**Why REST Instead of GraphQL?**

"For this use case, REST made more sense:
- Simple operations - just checking rules
- Standard HTTP methods - easy to test with curl or Postman
- Better HTTP caching
- Swagger generates documentation automatically
- Simpler for the team to understand"

---

## **7. LIVE PROOF: HITTING THE REAL API (30 seconds)**

**Open terminal:**

```bash
curl -X POST https://pluggable-rule-engine.onrender.com/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["min_total_100", "min_items_2", "divisible_by_5"]}'
```

**Show response:**
```json
{"passed": true, "details": {"min_total_100": true, "min_items_2": true, "divisible_by_5": true}}
```

"That's the live API in production. Fully functional, handling real requests right now."

---



## **CLOSING (30 seconds)**

**Quick recap:**

1. **Metaclass auto-registration** - write a class, it registers itself
2. **ABCMeta enforcement** - forget to implement evaluate, Python catches it
3. **DecimalField** - no rounding errors with money
4. **Multi-environment database** - SQLite local, PostgreSQL production, same code
5. **One-click deployment** - render.yaml handles everything
6. **Comprehensive tests** - 18 tests, all green

**What's next if I expand this:**
- Add JWT authentication
- Implement AND/OR rule composition
- Build an audit trail
- Set up webhook notifications

"The beauty of this architecture is scalability. Want to add a new rule? Write one class. Want to change how rules are evaluated? Edit the engine. Everything's decoupled and extensible."

**Links:**
- **Live Demo:** https://pluggable-rule-engine.onrender.com
- **GitHub:** [your-repo-url]

---

## **TIMING GUIDE**

- Introduction: 30s
- Problem Statement: 45s
- **How It Works (Metaclass + ABCMeta)**: 90s ← Your highlight moment
- API Demo: 60s
- Production Design: 90s
- Deployment: 60s
- Design Decisions: 45s
- Live Test: 30s
- Closing: 30s

**Total: 6 minutes 30 seconds**

---

## **CONVERSATION TIPS**

**If they ask: "Why not just use Django signals?"**
→ "Signals are for reacting to events - like 'when an order is saved, send an email'. Rules are structural - they're part of the business logic itself, not side effects."

**If they ask: "How would you handle rule dependencies?"**
→ "Great question. Right now rules are independent. But you could add a 'depends_on' attribute to BaseRule and use topological sorting to evaluate them in the right order."

**If they ask: "How does this scale?"**
→ "For high volume, I'd add Redis caching for rule results, use Celery for async evaluation, or even compile common rule combinations into optimized SQL WHERE clauses."

**If they ask: "What happens if someone requests a rule that doesn't exist?"**
→ "The serializer validates rules before they reach the engine. If someone requests 'fake_rule', they get a 400 error listing all available rules. No surprises."

**If they ask: "Why Decimal instead of storing cents as integers?"**
→ "I considered that, but Decimal is more readable in code and handles mixed currencies better. Plus, Django's ORM plays nicely with Decimal for database precision."

---

## **PRE-DEMO CHECKLIST**

✅ Wake up Render (visit the URL so it's not cold-starting during demo)
✅ Have Swagger UI open in one tab, code editor in another
✅ Test curl command beforehand
✅ Know your line numbers (rules/engine.py around line 38, orders/models.py around line 8)
✅ Practice explaining metaclasses out loud - this is your "wow" moment

---

