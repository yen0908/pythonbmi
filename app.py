import math

from flask import Flask, render_template, request

from domain.bmi import bmi_guidance, calculate_bmi
from domain.military import military_guidance

app = Flask(__name__)

def parse_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


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
            try:
                displayed_bmi = calculate_bmi(height, weight)
                military_result = military_guidance(height, weight)
            except ValueError:
                errors["height"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
            else:
                result = {
                    "name": name_input,
                    "bmi": f"{displayed_bmi:.1f}",
                    "overweight": 24 <= displayed_bmi < 27,
                    "military": military_result,
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
