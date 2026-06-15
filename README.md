# Travel Deal Management System

A professional REST API for managing travel deals built with Flask and SQLAlchemy.

## Features

- ✅ List all travel deals
- ✅ Create new travel deals with validation
- ✅ Retrieve individual deals by ID
- ✅ Search deals by destination, platform, travel_type
- ✅ Filter deals by price range (min/max)
- ✅ Sort deals by price, rating, or destination
- ✅ Track and retrieve recently viewed deals
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
python app.py
```

Or with Flask CLI:
```bash
flask --app app.py run --debug
```

Server runs at: `http://localhost:5000`

## API Endpoints

| Method | Endpoint              | Description                              |
|--------|----------------------|------------------------------------------|
| GET    | `/deals`             | List all deals                           |
| POST   | `/deals`             | Create a new deal                        |
| GET    | `/deals/<id>`        | Get deal by ID (records as viewed)       |
| GET    | `/deals/search`      | Search by destination, platform, type    |
| GET    | `/deals/filter`      | Filter by price range (min_price/max)    |
| GET    | `/deals/sort`        | Sort by price/rating/destination (asc/desc) |
| GET    | `/deals/recent`      | Get 10 most recently viewed deals        |

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

### GET /deals/search
```bash
curl "http://localhost:5000/deals/search?destination=Paris&platform=Expedia&travel_type=Luxury"
```

### GET /deals/filter
```bash
curl "http://localhost:5000/deals/filter?min_price=100&max_price=1000"
```

### GET /deals/sort
```bash
curl "http://localhost:5000/deals/sort?sort_by=price&order=asc"
```

### GET /deals/recent
```bash
curl http://localhost:5000/deals/recent
```

## Validation Rules

### Deal Creation
- **destination** — Required, non-empty string
- **price** — Required, positive number
- **platform** — Required, non-empty string
- **rating** — Required, number between 1 and 5
- **travel_type** — Required, one of: Budget, Luxury, Adventure, Family

### Query Parameters
- **search** — At least one of destination, platform, travel_type required
- **filter** — At least one of min_price or max_price required; max must be ≥ min
- **sort** — sort_by required (price, rating, destination); order required (asc, desc)

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

## Development Notes

- Recently viewed deals are tracked automatically when a deal is fetched via `GET /deals/<id>`
- All timestamps use UTC timezone
- RecentView records have cascading delete on deal removal
- Logging is configured for all operations (see `utils/logger.py`)

## Project Structure

```
Travel_Deal_Management_System/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── database/
│   └── models.py              # SQLAlchemy models (Deal, RecentView)
├── routes/
│   └── deal_routes.py         # All API endpoints
├── services/
│   ├── deal_service.py        # CRUD operations for deals
│   ├── search_service.py      # Search, filter, sort logic
│   └── recent_service.py      # Recently viewed deals logic
├── utils/
│   ├── validator.py           # Input validation
│   ├── query_validator.py     # Query parameter validation
│   ├── response.py            # Response utilities
│   └── logger.py              # Logging configuration
├── instance/                   # Flask instance files (db, etc.)
├── logs/                       # Application logs
└── postman_collection.json    # Postman test collection
```

