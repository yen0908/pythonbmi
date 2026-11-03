import math


def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI rounded to one decimal place."""
    if not math.isfinite(height_cm) or not math.isfinite(weight_kg):
        raise ValueError("身高與體重必須是有限數值")
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("身高與體重必須大於 0")

    height_meters = height_cm / 100
    try:
        bmi = weight_kg / (height_meters**2)
    except OverflowError as error:
        raise ValueError("BMI 計算結果超出可處理範圍") from error
    if not math.isfinite(bmi):
        raise ValueError("BMI 計算結果超出可處理範圍")
    return round(bmi, 1)


def bmi_guidance(bmi):
    if bmi < 18.5:
        return {
            "label": "體重過輕",
            "tone": "low",
            "advice": "留意是否攝取足夠且均衡的營養，規律進食並搭配適度肌力活動；若體重持續下降，建議諮詢醫師或營養師。",
        }
    if bmi < 24:
        return {
            "label": "健康體位",
            "tone": "healthy",
            "advice": "維持均衡飲食與規律運動，並持續留意睡眠及生活習慣，幫助保持健康體位。",
        }
    if bmi < 27:
        return {
            "label": "體重過重",
            "tone": "high",
            "advice": "可從減少含糖飲料、增加蔬菜與日常活動量開始，循序建立適合自己的健康習慣。",
        }
    return {
        "label": "肥胖",
        "tone": "high",
        "advice": "建議與醫師或營養師討論適合自己的飲食及運動計畫，並留意血壓、血糖等健康指標。",
    }
