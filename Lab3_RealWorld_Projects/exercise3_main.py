from telemetry import generate_telemetry_stream, validate_reading, normalize_reading, OPERATING_RANGE
from diagnostic import monitor, trace_abnormal_condition, build_diagnostic_report, EXECUTION_LOG, ABNORMAL_THRESHOLD

# ----------------------------------------------------------------------
# 1. CONFIGURATION (Cell 1 style) - Requirement 1
# ----------------------------------------------------------------------
LAST_NAME = "Cardenas"
STUDENT_ID = "TUPM-26-1258"
FAVORITE_ARTIST = "Maroon 5"
SEED_DIGIT = int(STUDENT_ID[-1])
NUM_READINGS = SEED_DIGIT + 6  # fixed stream length


@monitor
def process_stream(stream):
    raw_log = []
    valid_readings = []
    invalid_entries = []
    abnormal_traces = []

    for raw_value in stream:
        raw_log.append(raw_value)
        is_valid, result = validate_reading(raw_value)

        if not is_valid:
            invalid_entries.append((raw_value, result))
            continue

        valid_readings.append(result)
        normalized = normalize_reading(result)

        if normalized > ABNORMAL_THRESHOLD:
            levels_used, final_deviation = trace_abnormal_condition(
                normalized - ABNORMAL_THRESHOLD
            )
            abnormal_traces.append({
                "reading": result,
                "normalized": normalized,
                "levels": levels_used,
                "final_deviation": final_deviation,
            })

    return raw_log, valid_readings, invalid_entries, abnormal_traces


def determine_status(invalid_count, abnormal_count):
    if abnormal_count > 0:
        return "CRITICAL"
    elif invalid_count > 0:
        return "WARNING"
    else:
        return "OPTIMAL"


def display_report(raw_log, valid_readings, invalid_entries,
                    abnormal_traces, report):
    print("=" * 60)
    print(f"EQUIPMENT MONITORING PIPELINE REPORT")
    print("=" * 60)

    print("\n1. STUDENT-SPECIFIC INPUTS")
    print("-" * 60)
    print(f"  LAST_NAME: {LAST_NAME}")
    print(f"  STUDENT_ID: {STUDENT_ID}")
    print(f"  FAVORITE_ARTIST: {FAVORITE_ARTIST}")
    print(f"  SEED_NUM: {SEED_DIGIT}")

    print("\n2. GENERATED TELEMETRY DATA")
    print("-" * 60)
    for i, raw in enumerate(raw_log, start=1):
        print(f"  Reading {i:2}: {raw}")

    print("\n3. VALID/INVALID RESULTS")
    print("-" * 60)
    print("  Valid readings:")
    for v in valid_readings:
        print(f"    {v}  (range {OPERATING_RANGE})")
    print("  Invalid entries:")
    for raw, reason in invalid_entries:
        print(f"    {raw!r} -> {reason}")

    print("\n4. PROCESSED RESULTS")
    print("-" * 60)
    for v in valid_readings:
        print(f"  {v} -> normalized: {normalize_reading(v)}")

    print("\n5. RECURSIVE ANALYSIS")
    print("-" * 60)
    if abnormal_traces:
        for trace in abnormal_traces:
            print(f"  Reading {trace['reading']} (normalized {trace['normalized']}): "
                  f"{trace['levels']} recursive level(s), "
                  f"final deviation {trace['final_deviation']}")
    else:
        print("  No abnormal conditions detected.")

    print("\n6. FINAL DIAGNOSTIC SUMMARY")
    print("-" * 60)
    for key, value in report.items():
        print(f"  {key}: {value}")

    print("\n7. EXECUTION LOG")
    print("-" * 60)
    for entry in EXECUTION_LOG:
        print(f"  {entry}")

    print("\n8. FINAL OUTPUT")
    print("-" * 60)
    print(f"  Processed {report['processed']} readings "
          f"({report['valid']} valid, {report['invalid']} invalid, "
          f"{report['abnormal']} abnormal) -> "
          f"Overall Equipment Status: {report['status']}")
    print("=" * 60)


def main():
    stream = generate_telemetry_stream(LAST_NAME, SEED_DIGIT, FAVORITE_ARTIST, NUM_READINGS)
    raw_log, valid_readings, invalid_entries, abnormal_traces = process_stream(stream)

    status = determine_status(len(invalid_entries), len(abnormal_traces))
    report = build_diagnostic_report(
        len(raw_log), len(valid_readings), len(invalid_entries),
        len(abnormal_traces), status
    )

    display_report(raw_log, valid_readings, invalid_entries, abnormal_traces, report)


if __name__ == "__main__":
    main()