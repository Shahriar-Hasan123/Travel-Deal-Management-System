# Travel Deal Management System

A professional REST API for managing travel deals built with Flask and SQLAlchemy.

## Features

- ✅ List all travel deals
- ✅ Create new travel deals with validation
- ✅ Retrieve individual deals by ID
- ✅ Input validation for all fields
- ✅ RESTful API design
- ✅ SQLite database persistence

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **API Format:** JSON
- **Testing:** Postman collection included

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Shahriar-Hasan123/Travel-Deal-Management-System.git
cd Travel_Deal_Management_System
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
flask --app app.py run --debug
```

Server runs at: `http://localhost:5000`

## API Endpoints

| Method | Endpoint       | Description             |
|--------|----------------|-------------------------|
| GET    | `/deals`       | List all deals          |
| POST   | `/deals`       | Create a new deal       |
| GET    | `/deals/<id>`  | Get deal by ID          |

## Request Examples

### GET /deals
```bash
curl http://localhost:5000/deals
```

### POST /deals
```bash
curl -X POST http://localhost:5000/deals \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "price": 1200,
    "platform": "Booking.com",
    "rating": 4.5,
    "travel_type": "Luxury"
  }'
```

### GET /deals/<id>
```bash
curl http://localhost:5000/deals/1
```

## Validation Rules

- **destination** — Required, non-empty string
- **price** — Required, positive number
- **platform** — Required, non-empty string
- **rating** — Required, number between 1 and 5
- **travel_type** — Required, one of: Budget, Luxury, Adventure, Family

## Response Format

**Success Response:**
```json
{
  "success": true,
  "data": [...]
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error message",
  "error": [...]
}
```

## Testing with Postman

1. Import `postman_collection.json` into Postman
2. Run all test cases (success and error scenarios)
3. Validate API responses

## Project Structure

```
Travel_Deal_Management_System/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── database/
│   └── models.py            # SQLAlchemy models
├── routes/
│   └── deal_routes.py       # API endpoints
├── services/
│   └── deal_service.py      # Business logic
├── utils/
│   ├── validator.py         # Input validation
│   └── response.py          # Response utilities
└── postman_collection.json  # Postman test collection
```

