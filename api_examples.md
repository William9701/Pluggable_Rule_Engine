# API Usage Examples

This document provides practical examples for using the Pluggable Rule Engine API.

## Base URL

```
Local: http://localhost:8000
Production: https://your-app.onrender.com
```

## Authentication

Currently, no authentication is required. For production use, consider adding authentication.

## Examples

### 1. List All Available Rules

**Request:**
```bash
curl -X GET http://localhost:8000/rules/
```

**Response:**
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

### 2. Check Single Rule

**Request:**
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "rules": ["min_total_100"]
  }'
```

**Response:**
```json
{
  "passed": true,
  "details": {
    "min_total_100": true
  }
}
```

### 3. Check Multiple Rules

**Request:**
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "rules": ["min_total_100", "min_items_2", "divisible_by_5"]
  }'
```

**Response:**
```json
{
  "passed": false,
  "details": {
    "min_total_100": true,
    "min_items_2": true,
    "divisible_by_5": false
  }
}
```

### 4. Error: Invalid Order ID

**Request:**
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 999,
    "rules": ["min_total_100"]
  }'
```

**Response (404):**
```json
{
  "error": "Order not found",
  "detail": "Order with id 999 does not exist",
  "status_code": 404
}
```

### 5. Error: Invalid Rule Name

**Request:**
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "rules": ["nonexistent_rule"]
  }'
```

**Response (400):**
```json
{
  "error": "Invalid request",
  "detail": {
    "rules": [
      "Invalid rule(s): nonexistent_rule. Available rules: min_total_100, min_items_2, divisible_by_5"
    ]
  },
  "status_code": 400
}
```

### 6. Error: Missing Required Fields

**Request:**
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1
  }'
```

**Response (400):**
```json
{
  "error": "Invalid request",
  "detail": {
    "rules": [
      "This field is required."
    ]
  },
  "status_code": 400
}
```

## Python Examples

### Using Requests Library

```python
import requests

BASE_URL = "http://localhost:8000"

# List all rules
response = requests.get(f"{BASE_URL}/rules/")
rules = response.json()
print(f"Available rules: {rules}")

# Check rules for an order
payload = {
    "order_id": 1,
    "rules": ["min_total_100", "min_items_2"]
}
response = requests.post(
    f"{BASE_URL}/rules/check/",
    json=payload
)
result = response.json()
print(f"Validation result: {result}")

if result['passed']:
    print("✓ All rules passed!")
else:
    failed_rules = [
        rule for rule, passed in result['details'].items()
        if not passed
    ]
    print(f"✗ Failed rules: {failed_rules}")
```

### Async Example with aiohttp

```python
import aiohttp
import asyncio

async def check_order_rules(order_id, rules):
    async with aiohttp.ClientSession() as session:
        payload = {"order_id": order_id, "rules": rules}
        async with session.post(
            "http://localhost:8000/rules/check/",
            json=payload
        ) as response:
            return await response.json()

# Usage
result = asyncio.run(check_order_rules(1, ["min_total_100", "min_items_2"]))
print(result)
```

## JavaScript Examples

### Using Fetch API

```javascript
// List all rules
fetch('http://localhost:8000/rules/')
  .then(response => response.json())
  .then(rules => console.log('Available rules:', rules));

// Check rules for an order
const payload = {
  order_id: 1,
  rules: ['min_total_100', 'min_items_2']
};

fetch('http://localhost:8000/rules/check/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(result => {
    if (result.passed) {
      console.log('✓ All rules passed!');
    } else {
      console.log('✗ Validation failed:', result.details);
    }
  });
```

### Using Axios

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Check rules
async function checkOrderRules(orderId, rules) {
  try {
    const response = await axios.post(`${BASE_URL}/rules/check/`, {
      order_id: orderId,
      rules: rules
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response.data);
    throw error;
  }
}

// Usage
checkOrderRules(1, ['min_total_100', 'min_items_2'])
  .then(result => console.log('Result:', result));
```

## Integration Examples

### Django View Integration

```python
from django.http import JsonResponse
import requests

def validate_order_view(request, order_id):
    # Call the rule engine API
    response = requests.post(
        'http://localhost:8000/rules/check/',
        json={
            'order_id': order_id,
            'rules': ['min_total_100', 'min_items_2']
        }
    )

    result = response.json()

    if result['passed']:
        return JsonResponse({'status': 'approved', 'details': result})
    else:
        return JsonResponse({'status': 'rejected', 'details': result})
```

### Flask Integration

```python
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/validate/<int:order_id>')
def validate_order(order_id):
    response = requests.post(
        'http://localhost:8000/rules/check/',
        json={
            'order_id': order_id,
            'rules': ['min_total_100', 'min_items_2', 'divisible_by_5']
        }
    )
    return jsonify(response.json())
```

## Best Practices

1. **Cache rule list**: The available rules don't change often, so cache the result
2. **Batch validations**: If checking multiple orders, consider implementing a batch endpoint
3. **Handle errors gracefully**: Always check status codes and handle error responses
4. **Use async for high volume**: For high-throughput applications, use async clients
5. **Monitor performance**: Track API response times and rule evaluation speeds

## Rate Limiting Considerations

Currently, there are no rate limits. For production:
- Consider implementing rate limiting (Django Ratelimit)
- Use caching (Redis) for frequently accessed data
- Implement pagination for large result sets
