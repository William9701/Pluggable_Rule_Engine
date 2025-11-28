# 6-Minute Demo Script: Django Pluggable Rule Engine

## **INTRODUCTION (30 seconds)**

"Hi! I was given a task to build a Django pluggable rule engine with specific requirements:

**The Task:**
1. Create an Order model with `total` and `items_count` fields, seed 3 example orders
2. Build a rule engine where rules auto-register - new rules shouldn't require modifying existing code
3. Implement three rules: total > 100, items ≥ 2, total divisible by 5
4. Expose a REST API at POST /rules/check/ with a specific request/response format

The challenge was the auto-registration requirement. I solved it using Python metaclasses, and it's live on Render with Swagger documentation."

**Show:** https://pluggable-rule-engine.onrender.com

---

## **REQUIREMENT 1: ORDER MODEL + SEEDED DATA (45 seconds)**

"Let me show you how I addressed the first requirement."

**Open:** `orders/models.py`

```python
class Order(models.Model):
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    items_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Explain:**
"So here's the Order model with the two required fields - `total` and `items_count`. I used DecimalField for total instead of FloatField because financial calculations need precision. FloatField gives you 0.1 + 0.2 = 0.30000000004, but DecimalField uses fixed-point arithmetic - no rounding errors.

For the seeding requirement, I created three test orders:"

**Open:** `orders/apps.py` or show the data:

```python
Order 1: total=$150.00, items_count=3  # Passes all rules
Order 2: total=$75.50,  items_count=1  # Fails all rules
Order 3: total=$200.00, items_count=5  # Passes all rules
```

**Explain:**
"These seed automatically when the app starts through the ready() method in apps.py. Order 1 and 3 pass all validation rules, Order 2 fails them - perfect for testing."

---

## **REQUIREMENT 2: AUTO-REGISTERING RULE ENGINE (90 seconds)**

"Now the interesting part - the auto-registration requirement. Rules needed to register themselves without modifying existing code."

**Open:** `rules/engine.py`

"Here's how I solved it with a Python metaclass:"

```python
class RuleMeta(ABCMeta):
    """Metaclass that auto-registers rule classes"""
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'BaseRule' and 'name' in attrs and attrs['name']:
            RuleRegistry.register(attrs['name'], cls)
        return cls

class BaseRule(metaclass=RuleMeta):
    name: str = None

    @abstractmethod
    def evaluate(self, order) -> bool:
        """Returns True/False based on order validation"""
        pass
```

**Explain naturally:**
"So what's happening? A metaclass is code that runs when you CREATE a class, not when you use it. When Python sees a new rule class, this `__new__` method intercepts it and automatically adds it to the RuleRegistry.

I inherited from ABCMeta - Python's Abstract Base Class metaclass - because I wanted enforcement. The @abstractmethod decorator means every rule MUST implement `evaluate(order) -> bool`. If someone forgets, Python won't even let them instantiate the class. It's fail-fast validation.

Now watch how clean adding a rule becomes."

---

## **REQUIREMENT 3: THE THREE REQUIRED RULES (60 seconds)**

**Open:** `rules/order_rules.py`

"The task required three specific rules. Here they are:"

### **Rule 1: Total > 100**
```python
class MinimumTotalRule(BaseRule):
    name = "min_total_100"
    description = "Validates that order total is greater than 100"

    def evaluate(self, order) -> bool:
        return order.total > Decimal('100.00')
```

### **Rule 2: Items Count ≥ 2**
```python
class MinimumItemsRule(BaseRule):
    name = "min_items_2"
    description = "Validates that order has at least 2 items"

    def evaluate(self, order) -> bool:
        return order.items_count >= 2
```

### **Rule 3: Total Divisible by 5**
```python
class DivisibleByFiveRule(BaseRule):
    name = "divisible_by_5"
    description = "Validates that order total is divisible by 5"

    def evaluate(self, order) -> bool:
        return order.total % Decimal('5.00') == Decimal('0.00')
```

**Explain:**
"That's it. Just inherit from BaseRule, give it a name, implement evaluate. The metaclass handles registration automatically.

When the app starts, you'll see in the logs:
```
INFO: Registered rule: min_total_100
INFO: Registered rule: min_items_2
INFO: Registered rule: divisible_by_5
```

No configuration files. No manual registration. Zero extra code."

---

## **REQUIREMENT 4: THE API ENDPOINT (60 seconds)**

"The final requirement was a specific API endpoint format."

**Open Swagger UI:** https://pluggable-rule-engine.onrender.com

"The task specified POST /rules/check/ with this exact format:"

**Demo the EXACT format from the task:**
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2"]
}
```

**Click Execute, show response:**
```json
{
  "passed": true,
  "details": {
    "min_total_100": true,
    "min_items_2": true
  }
}
```

**Explain:**
"So Order 1 has $150 and 3 items. Total > 100? Yes. Items ≥ 2? Yes. Both pass, so overall 'passed' is true.

Notice the response structure matches the task requirements exactly - a 'passed' boolean and a 'details' object with individual rule results.

Let me test with Order 2 which should fail:"

```json
{
  "order_id": 2,
  "rules": ["min_total_100", "min_items_2", "divisible_by_5"]
}
```

**Response:**
```json
{
  "passed": false,
  "details": {
    "min_total_100": false,
    "min_items_2": false,
    "divisible_by_5": false
  }
}
```

"Order 2 has $75.50 and 1 item. Total > 100? No. Items ≥ 2? No. Divisible by 5? No. All fail, so 'passed' is false. The engine evaluates each rule independently, and if ANY rule fails, the overall check fails."

---

## **BONUS: PRODUCTION-READY EXTRAS (90 seconds)**

"The task didn't require these, but I added professional touches to make it production-ready:"

### **1. Request Validation with Serializers**

**Open:** `rules/serializers.py`

```python
class RuleCheckRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    rules = serializers.ListField(
        child=serializers.CharField(),
        min_length=1
    )

    def validate_rules(self, value):
        # Check if all requested rules exist in registry
        for rule_name in value:
            if not RuleRegistry.rule_exists(rule_name):
                raise ValidationError(f"Invalid rule: {rule_name}")
        return value
```

**Explain:**
"This validates requests before they reach the engine. If someone sends a rule that doesn't exist, they get a helpful error listing all available rules."

---

### **2. Multi-Environment Database Config**

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
"Locally it uses SQLite - zero setup. In production on Render, it reads DATABASE_URL and connects to PostgreSQL. Same codebase, different environments."

---

### **3. One-Click Deployment**

**Open:** `render.yaml`

```yaml
buildCommand: "pip install -r requirements.txt && python manage.py migrate && python manage.py seed_orders"
startCommand: "gunicorn config.wsgi:application"
```

**Explain:**
"Infrastructure as code. Push to Render, it installs dependencies, runs migrations, seeds data, and starts the production server automatically."

---

## **LIVE PROOF (30 seconds)**

**Open terminal:**

```bash
curl -X POST https://pluggable-rule-engine.onrender.com/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["min_total_100", "min_items_2", "divisible_by_5"]}'
```

**Response:**
```json
{"passed": true, "details": {"min_total_100": true, "min_items_2": true, "divisible_by_5": true}}
```

"That's the live API - fully functional in production right now."

---

## **CLOSING (30 seconds)**

**How I Addressed Each Requirement:**

1. ✅ **Order model** - DecimalField for precision, auto-seeded with 3 orders
2. ✅ **Auto-registration** - Metaclass pattern, zero configuration needed
3. ✅ **Three rules** - min_total_100, min_items_2, divisible_by_5
4. ✅ **API endpoint** - POST /rules/check/ with exact format specified

**Key Technical Decisions:**
- Metaclass + ABCMeta for auto-registration with enforcement
- DecimalField to avoid floating-point errors
- Serializers for request validation
- One-click deployment with render.yaml
- 18 automated tests covering all functionality

"The beauty of this solution is extensibility. Want a fourth rule? Just write one class. The metaclass handles the rest."

**Links:**
- **Live Demo:** https://pluggable-rule-engine.onrender.com
- **GitHub:** [your-repo-url]

---

## **TIMING GUIDE**

- Introduction: 30s
- Requirement 1 (Model + Seed): 45s
- **Requirement 2 (Auto-Registration)**: 90s ← Your highlight
- Requirement 3 (Three Rules): 60s
- Requirement 4 (API): 60s
- Production Extras: 90s
- Live Test: 30s
- Closing: 30s

**Total: 6 minutes 45 seconds**

---

## **CONVERSATION TIPS**

**If they ask: "Why metaclass instead of decorators?"**
→ "Decorators require remembering to add `@register_rule()` every time. With metaclasses, inheritance enforces it - you can't forget. Plus registration happens at import time, not runtime."

**If they ask: "Why ABCMeta?"**
→ "Because I wanted compile-time enforcement. If someone creates a rule class but forgets to implement `evaluate()`, Python won't let them instantiate it. It catches bugs before they reach production."

**If they ask: "How does this scale?"**
→ "Current implementation evaluates rules sequentially. For high volume, I'd add Redis caching for rule results, use Celery for async evaluation, or compile frequent rule combinations into SQL WHERE clauses."

**If they ask: "What if someone requests a non-existent rule?"**
→ "The serializer validates before it reaches the engine. Request `'fake_rule'` and you get a 400 error: 'Invalid rule: fake_rule. Available rules: min_total_100, min_items_2, divisible_by_5'."

**If they ask: "Why seed in apps.py instead of a fixture?"**
→ "Convenience. The app works immediately without running extra commands. For production, you'd use fixtures or migrations, but for a demo this makes it plug-and-play."

---

## **PRE-DEMO CHECKLIST**

✅ Wake up Render (visit URL to avoid cold start during demo)
✅ Have Swagger UI open in one tab, code in another
✅ Test curl command beforehand
✅ Know line numbers: rules/engine.py (38), rules/order_rules.py (9, 28, 47)
✅ Practice explaining metaclasses - this is your "wow" moment

---

## **WHAT THE TASK REQUIRED vs WHAT I DELIVERED**

| Requirement | Asked For | What I Delivered |
|-------------|-----------|------------------|
| Order model | total, items_count | ✅ Plus timestamps, validation |
| Seed data | 3 orders | ✅ Auto-seeds on startup |
| Auto-registration | "without modifying existing code" | ✅ Metaclass pattern |
| 3 Rules | min_total_100, min_items_2, divisible_by_5 | ✅ All implemented |
| API endpoint | POST /rules/check/ | ✅ Plus Swagger docs |
| Response format | passed + details | ✅ Exact format |
| **Extras** | *(not required)* | Request validation, error handling, tests, deployment |
