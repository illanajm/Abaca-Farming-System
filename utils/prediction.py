def predict_yield(farm_area, years_farming, soil_quality_score):

    base = farm_area * 2

    experience_boost = years_farming * 0.5

    soil_factor = {
        "Good": 1.5,
        "Average": 1.0,
        "Poor": 0.7
    }.get(soil_quality_score, 1.0)

    return round((base + experience_boost) * soil_factor, 2)

def pest_risk(pest_count, humidity_level):

    score = pest_count * 2 + humidity_level

    if score < 5:
        return "Low"
    elif score < 10:
        return "Medium"
    else:
        return "High"

def productivity_score(yield_value, farm_area):

    if farm_area == 0:
        return 0

    return round(yield_value / farm_area, 2)