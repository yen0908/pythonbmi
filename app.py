import math

from flask import Flask, render_template, request

app = Flask(__name__)


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


def parse_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def military_guidance(height, weight):
    measured_height = math.floor(height)
    measured_weight = math.floor(weight * 10) / 10
    bmi = round(measured_weight / ((measured_height / 100) ** 2), 1)

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


@app.route("/", methods=["GET", "POST"])
def index():
    name_input = ""
    height_input = ""
    weight_input = ""
    errors = {}
    result = None

    if request.method == "POST":
        name_input = request.form.get("name", "").strip()
        height_input = request.form.get("height", "").strip()
        weight_input = request.form.get("weight", "").strip()
        height = parse_positive_number(height_input)
        weight = parse_positive_number(weight_input)

        if height is None:
            errors["height"] = "請輸入大於 0 的有效身高（公分）。"
        elif math.floor(height) < 1:
            errors["height"] = "身高至少需要 1 公分，才能進行兵役參考試算。"
        if weight is None:
            errors["weight"] = "請輸入大於 0 的有效體重（公斤）。"

        if not errors:
            height_meters = height / 100
            height_squared = height_meters * height_meters
            if not math.isfinite(height_squared) or height_squared == 0:
                errors["height"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
            else:
                bmi = weight / height_squared
                if not math.isfinite(bmi) or bmi == 0:
                    errors["weight"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
                else:
                    displayed_bmi = round(bmi, 1)
                    result = {
                        "name": name_input,
                        "bmi": f"{displayed_bmi:.1f}",
                        "overweight": 24 <= displayed_bmi < 27,
                        "military": military_guidance(height, weight),
                        **bmi_guidance(displayed_bmi),
                    }

    return render_template(
        "index.html",
        name_input=name_input,
        height_input=height_input,
        weight_input=weight_input,
        errors=errors,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
