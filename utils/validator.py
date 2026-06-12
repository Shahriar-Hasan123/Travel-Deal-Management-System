VALID_TRAVEL_TYPES = ["Budget", "Luxury", "Adventure", "Family"]


def validate_deal_input(data):
    errors = []

    destination = data.get("destination", "")
    if not destination.strip() or not isinstance(destination, str):
        errors.append("destination can not be empty")

    price = data.get("price")
    if price is None:
        errors.append("Price is required")
    if not isinstance(price, (int, float)) or price <= 0:
        errors.append("Price must be a positive number")

    platform = data.get("platform")
    if not platform.strip() or not isinstance(platform, str):
        errors.append("plateform can not be empty")

    rating = data.get("rating")
    if rating is None:
        errors.append("Rating is required")
    if not isinstance(rating, (int, float)) or not (rating >= 1 and rating <= 5):
        errors.append("rating must be between 1 and 5")

    travel_type = data.get("travel_type", "")
    if travel_type not in VALID_TRAVEL_TYPES:
        errors.append(f"travel_type must be one of: {', '.join(VALID_TRAVEL_TYPES)}")
    
    return len(errors)==0, errors
