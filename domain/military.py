import math

from .bmi import calculate_bmi


def military_guidance(height_cm, weight_kg):
    """Return a military status reference based on official height/BMI rules."""
    if not math.isfinite(height_cm) or not math.isfinite(weight_kg):
        raise ValueError("身高與體重必須是有限數值")
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("身高與體重必須大於 0")

    measured_height = math.floor(height_cm)
    try:
        measured_weight = math.floor(weight_kg * 10) / 10
    except OverflowError as error:
        raise ValueError("體重超出可處理範圍") from error
    bmi = calculate_bmi(measured_height, measured_weight)

    if measured_height <= 154 or measured_height >= 196:
        category = "免役體位"
        reason = "身高 154 公分以下或 196 公分以上。"
    elif 155 <= measured_height <= 157:
        if 15 <= bmi <= 35:
            category = "替代役體位"
            reason = "身高 155 至 157 公分，且 BMI 落在 15 至 35。"
        else:
            category = "免役體位"
            reason = "身高 155 至 157 公分，且 BMI 不在 15 至 35。"
    elif 16.5 <= bmi <= 32:
        category = "常備役體位"
        reason = "BMI 落在 16.5 至 32。"
    elif 15 <= bmi < 16.5 or 32 < bmi <= 35:
        category = "替代役體位"
        reason = "BMI 落在替代役體位區間。"
    else:
        category = "免役體位"
        reason = "BMI 低於 15 或高於 35。"

    return {
        "category": category,
        "reason": reason,
        "height": f"{measured_height:d}",
        "weight": f"{measured_weight:.1f}",
        "bmi": f"{bmi:.1f}",
    }
