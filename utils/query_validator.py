VALID_TRAVEL_TYPES = ["Budget", "Luxury", "Adventure", "Family"]
VALID_SORT_FIELDS = ["price", "rating", "destination"]
VALID_SORT_ORDERS = ["asc", "desc"]


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


def validate_sort_params(sort_by, order):
    errors = []

    if not sort_by:
        errors.append(
            f"sort_by is required. Valid fields: {', '.join(VALID_SORT_FIELDS)}"
        )
    elif sort_by not in VALID_SORT_FIELDS:
        errors.append(
            f"Invalid sort_by '{sort_by}'. Must be one of:  {', '.join(VALID_SORT_FIELDS)}"
        )

    if not order:
        errors.append(f"order is required. Valid value: {', '.join(VALID_SORT_ORDERS)}")
    elif order not in VALID_SORT_ORDERS:
        errors.append(
            f"Invalid order '{order}'. Must be one of: {', '.join(VALID_SORT_ORDERS)}"
        )

    return len(errors) == 0, errors
