VALID_TRAVEL_TYPES = ["Budget", "Luxury", "Adventure", "Family"]


def validate_search_params(destination: str | None, platform: str | None, travel_type: str | None):
    errors = []
    if not any([destination, platform, travel_type]):
        errors.append("At least one search parameter is required: destination, platform, or travel_type")

    if travel_type and travel_type.capitalize() not in VALID_TRAVEL_TYPES:
        errors.append(f"Unknown travel type '{travel_type}'. Must be one of: {', '.join(VALID_TRAVEL_TYPES)}")

    return len(errors) == 0, errors
