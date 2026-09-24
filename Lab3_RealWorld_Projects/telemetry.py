OPERATING_RANGE = (15.0, 90.0)


def generate_telemetry_stream(last_name, seed_digit, favorite_artist, count):
    ascii_name = sum(ord(c) for c in last_name.upper())
    ascii_artist = sum(ord(c) for c in favorite_artist.upper() if c.isalpha())

    for i in range(1, count + 1):
        if i % 4 == 0:
            yield "ERR"
        else:
            value = (ascii_name + ascii_artist + (i * seed_digit)) % 100
            yield value


def validate_reading(value):
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        return False, f"Invalid non-numeric reading ('{value}')"

    low, high = OPERATING_RANGE
    if not (low <= numeric_value <= high):
        return False, f"Out of range ({numeric_value})"

    return True, numeric_value

normalize_reading = lambda v, low=OPERATING_RANGE[0], high=OPERATING_RANGE[1]: round((v - low) / (high - low), 3)