# Travel Deal Management System

A professional REST API for managing travel deals built with Flask and SQLAlchemy.

## Features

- ✅ List all travel deals
- ✅ Create new travel deals with validation
- ✅ Retrieve individual deals by ID
- ✅ Update existing deals with validation
- ✅ Delete deals by ID
- ✅ Search deals by destination, platform, travel_type
- ✅ Filter deals by price range (min/max)
- ✅ Sort deals by price, rating, or destination
- ✅ Track and retrieve recently viewed deals
- ✅ View most popular (most-viewed) deals
- ✅ Global API statistics tracking (requests, success rate, search destinations)
- ✅ Input validation for all fields
- ✅ RESTful API design
- ✅ SQLite database persistence
- ✅ Automatic request logging and stats recording via middleware

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **API Format:** JSON
- **Testing:** Postman collection included

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Shahriar-Hasan123/Travel-Deal-Management-System-Shahriar_Hasan.git
cd Travel-Deal-Management-System-Shahriar_Hasan
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
| PUT    | `/deals/<id>`        | Update deal by ID                        |
| DELETE | `/deals/<id>`        | Delete deal by ID                        |
| GET    | `/deals/search`      | Search by destination, platform, type    |
| GET    | `/deals/filter`      | Filter by price range (min_price/max)    |
| GET    | `/deals/sort`        | Sort by price/rating/destination (asc/desc) |
| GET    | `/deals/recent`      | Get 10 most recently viewed deals        |
| GET    | `/deals/popular`     | Get most popular (most-viewed) deals     |
| GET    | `/stats`             | Get global API statistics                |

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

### GET /deals/popular
```bash
curl http://localhost:5000/deals/popular
```

### GET /stats
```bash
curl http://localhost:5000/stats
```

### PUT /deals/<id>
```bash
curl -X PUT http://localhost:5000/deals/1 \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "price": 1500,
    "platform": "Agoda",
    "rating": 4.8,
    "travel_type": "Adventure"
  }'
```

### DELETE /deals/<id>
```bash
curl -X DELETE http://localhost:5000/deals/1
```

## Validation Rules

### Deal Creation & Update (PUT)
- **destination** — Required, non-empty string
- **price** — Required, positive number
- **platform** — Required, non-empty string
- **rating** — Required, number between 1 and 5
- **travel_type** — Required, one of: Budget, Luxury, Adventure, Family

> **Note:** PUT `/deals/<id>` accepts partial updates; omitted fields retain their current values

### Query Parameters
- **search** — At least one of destination, platform, travel_type required
- **filter** — At least one of min_price or max_price required; max must be ≥ min
- **sort** — sort_by required (price, rating, destination); order required (asc, desc)

## API Statistics

The `/stats` endpoint returns global API usage metrics:

**Response Example:**
```json
{
  "success": true,
  "data": {
    "stats": {
      "total_requests": 10,
      "successful_requests": 8,
      "failed_requests": 2,
      "most_searched_destination": "Paris",
      "most_viewed_deal": {
        "deal": {
          "id": 1,
          "destination": "Paris",
          "price": 1200.0,
          "platform": "Booking.com",
          "rating": 4.5,
          "travel_type": "Luxury"
        },
        "view_count": 5
      }
    }
  }
}
```

**Stats Fields:**
- `total_requests` — Total HTTP requests made to the API
- `successful_requests` — Requests with status code < 400
- `failed_requests` — Requests with status code ≥ 400
- `most_searched_destination` — Most frequently searched destination (or `null`)
- `most_viewed_deal` — Deal with highest view count, including its `view_count` (or `null`)

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
- Deal views (popularity) are tracked separately via the `DealView` model
- **API Statistics** are recorded globally via middleware (`@after_request` in `app.py`):
  - Total requests and success/failure counts
  - Most-searched destination (tracked for `GET /deals/search` requests)
  - Most-viewed deal (aggregated from `DealView` records)
- All timestamps use UTC timezone
- **Cascading deletes:** When a deal is deleted via `DELETE /deals/<id>`:
  - Related `RecentView` records are automatically deleted
  - Related `DealView` records are automatically deleted
- Logging is configured for all operations (see `utils/logger.py`)
- Stats are persisted in the `api_stats` table (single record)
- Global error handlers in `app.py` manage 404 (not found), 405 (method not allowed), and 500 (server errors)

## Project Structure

```
Travel_Deal_Management_System/
├── app.py                      # Flask application entry point & middleware
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── database/
│   └── models.py              # SQLAlchemy models (Deal, RecentView, DealView, ApiStat)
├── routes/
│   ├── deal_routes.py         # Deal endpoints (CRUD, search, filter, sort, recent, popular)
│   └── stats_routes.py        # Stats endpoint
├── services/
│   ├── deal_service.py        # CRUD operations for deals
│   ├── search_service.py      # Search, filter, sort logic
│   ├── recent_service.py      # Recently viewed deals logic
│   ├── popular_service.py     # Popular deals and view tracking
│   └── stats_service.py       # API statistics aggregation and recording
├── utils/
│   ├── validator.py           # Input validation
│   ├── query_validator.py     # Query parameter validation
│   ├── response.py            # Response utilities
│   └── logger.py              # Logging configuration
├── instance/                   # Flask instance files (travel.db, etc.)
├── logs/                       # Application logs
└── postman_collection.json    # Postman test collection
```

