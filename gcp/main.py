import json
import functions_framework
from flask import Flask, request, jsonify

args = request.args or {}

@functions_framework.http
def medication_dosage_checker(request):
    ...
    """HTTP Cloud Function.
    Expects JSON with 'weight' (in kg) and 'medication' name.
    Returns a recommended dosage classification.
    """
    # Prefer JSON body; fall back to query parameters for convenience
    data = request.get_json(silent=True) or {}
    args = request.args or {}

    weight = data.get("weight", args.get("weight"))
    medication = data.get("medication", args.get("medication"))

    # Presence check
    if weight is None or medication is None:
        return (
            json.dumps({"error": "Both 'weight' and 'medication' are required."}),
            400,
            {"Content-Type": "application/json"},
        )

    # Convert weight to float
    try:
        weight_val = float(weight)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'weight' must be a number."}),
            400,
            {"Content-Type": "application/json"},
        )

    # Simplified medication dosage logic (mg per kg)
    med_dosage_map = {
        "amoxicillin": 20,  # mg per kg
        "ibuprofen": 10,
        "acetaminophen": 15,
    }

    med = medication.lower()
    if med not in med_dosage_map:
        return (
            json.dumps({"error": f"Medication '{med}' not supported."}),
            400,
            {"Content-Type": "application/json"},
        )

    recommended_dosage = weight_val * med_dosage_map[med]

    # Categorize the dosage
    status = "normal" if recommended_dosage <= 1000 else "high"
    category = "Safe dosage" if status == "normal" else "Above recommended limit"

    payload = {
        "weight_kg": weight_val,
        "medication": med,
        "recommended_dosage_mg": recommended_dosage,
        "status": status,
        "category": category,
    }

    return json.dumps(payload), 200, {"Content-Type": "application/json"}
