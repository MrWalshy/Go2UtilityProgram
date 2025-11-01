def validate_numeric(value: str) -> bool:
    return value.isdigit() or value == ""

def validate_range(value: int, min: int, max: int) -> bool:
    return value >= min and value <= max

def validate_numeric_in_range(value: str, min: int, max: int) -> bool:
    if not validate_numeric(value):
        return false
    num = 0 if value == "" else int(value)
    return validate_range(num, min, max)
