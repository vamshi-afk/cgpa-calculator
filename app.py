from flask import Flask, render_template, request

app = Flask(__name__)

grade_points = {
    "S": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "D": 4,
    "E": 3,
    "NC": 2,
}


# Home
@app.route("/")
def home():
    tab = request.args.get("tab", "sgpa")  # default sgpa
    return render_template("index.html", active_tab=tab)


# SGPA
@app.route("/sgpa", methods=["GET", "POST"])
def sgpa():
    sgpa_value = None
    credits = None
    grades = None

    est_current_cgpa = request.form.get("current_cgpa")
    est_current_credits = request.form.get("current_credits")
    est_sem_credits = request.form.get("sem_credits")
    est_target_cgpa = request.form.get("target_cgpa")

    if request.method == "POST":
        credits = request.form.getlist("credits")
        grades = request.form.getlist("grade")
        sgpa_value = calculate_sgpa(credits, grades)

    return render_template(
        "index.html",
        sgpa=sgpa_value if request.method == "POST" else None,
        old_credits=credits if request.method == "POST" else None,
        old_grades=grades if request.method == "POST" else None,
        est_current_cgpa=est_current_cgpa,
        est_current_credits=est_current_credits,
        est_sem_credits=est_sem_credits,
        est_target_cgpa=est_target_cgpa,
        active_tab=request.args.get("tab", "sgpa"),
    )


# Estimator
@app.route("/estimator", methods=["GET", "POST"])
def estimator():
    required_sgpa_value = None
    message = None

    est_current_cgpa = request.form.get("current_cgpa")
    est_current_credits = request.form.get("current_credits")
    est_sem_credits = request.form.get("sem_credits")
    est_target_cgpa = request.form.get("target_cgpa")

    if request.method == "POST":
        try:
            required_sgpa_value = required_sgpa(
                float(est_current_cgpa),
                float(est_current_credits),
                float(est_sem_credits),
                float(est_target_cgpa),
            )

            if required_sgpa_value is None:
                message = "Semester credits cannot be zero"
            elif required_sgpa_value > 10:
                message = "Target not achievable"
            elif required_sgpa_value < 0:
                message = "Target already achieved"
            else:
                message = "Target achievable"

        except Exception:
            message = "Invalid input"

    return render_template(
        "index.html",
        required_sgpa=required_sgpa_value,
        message=message,
        est_current_cgpa=est_current_cgpa,
        est_current_credits=est_current_credits,
        est_sem_credits=est_sem_credits,
        est_target_cgpa=est_target_cgpa,
        old_credits=None,
        old_grades=None,
        active_tab=request.args.get("tab", "estimator"),
    )


# Calculations


def calculate_sgpa(credits, grades):
    total_points = 0
    total_credits = 0

    for i in range(len(credits)):
        try:
            c = float(credits[i])
            g = grades[i]
            total_points += c * grade_points[g]
            total_credits += c
        except:
            continue

    if total_credits == 0:
        return None

    return round(total_points / total_credits, 3)


def required_sgpa(current_cgpa, current_credits, sem_credits, target_cgpa):
    if sem_credits == 0:
        return None

    total_after = current_credits + sem_credits
    sgpa = (target_cgpa * total_after - current_cgpa * current_credits) / sem_credits
    return round(sgpa, 3)


if __name__ == "__main__":
    app.run(debug=True)
