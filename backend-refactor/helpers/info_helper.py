"""Helper for loading measurement information from CSV files."""
import csv
from typing import List, Dict
import os

def get_date() -> List[Dict]:
    measurements = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "measurements.csv")

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            measurements.append(row)

        
    rows = []
    for row in measurements:
        rows.append({
            "signal_id": row.get("SignalId"),
            "timestamp": row.get("Ts"),
            "value": row.get("MeasurementValue"),
            "unit": row.get("Unit")
        })

    print(measurements[0])
    return rows