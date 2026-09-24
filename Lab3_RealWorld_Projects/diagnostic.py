EXECUTION_LOG = []

ABNORMAL_THRESHOLD = 0.85


def monitor(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        EXECUTION_LOG.append(f"{func.__name__} executed -> result: {result}")
        return result
    return wrapper


def trace_abnormal_condition(deviation, level=1):
    EXECUTION_LOG.append(f"Abnormal trace level {level}: deviation={round(deviation, 4)}")

    if deviation < 0.01:
        return level, round(deviation, 4)

    return trace_abnormal_condition(deviation / 2, level + 1)


@monitor
def build_diagnostic_report(processed_count, valid_count, invalid_count,
                             abnormal_count, status):
    return {
        "processed": processed_count,
        "valid": valid_count,
        "invalid": invalid_count,
        "abnormal": abnormal_count,
        "status": status,
    }