VALID_TRAVEL_TYPES = ["Budget", "Luxury", "Adventure", "Family"]


def validate_search_params(
    destination: str | None, platform: str | None, travel_type: str | None
):
    errors = []
    if not any([destination, platform, travel_type]):
        errors.append(
            "At least one search parameter is required: destination, platform, or travel_type"
        )

    if travel_type and travel_type.capitalize() not in VALID_TRAVEL_TYPES:
        errors.append(
            f"Unknown travel type '{travel_type}'. Must be one of: {', '.join(VALID_TRAVEL_TYPES)}"
        )

    return len(errors) == 0, errors


def validate_filter_params(min_price, max_price):
    errors = []
    parsed = {}

    if min_price is not None:
        try:
            min_val = float(min_price)
            if min_val < 0:
                errors.append("min_price can not be negative")
            else:
                parsed["min_price"] = min_val
        except ValueError:
            errors.append("min_price must be a valid number")

    if max_price is not None:
        try:
            max_val = float(max_price)
            if max_val < 0:
                errors.append("max_price can not be negative")
            else:
                parsed["max_price"] = max_val
        except ValueError:
            errors.append("max_price must be valid number")

    if "min_price" in parsed and "max_price" in parsed:
        if parsed["max_price"] < parsed["min_price"]:
            errors.append("max_price can not be smaller than min price")

    return (len(errors) == 0), parsed, errors
