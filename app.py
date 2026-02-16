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
    return render_template("index.html", active_tab="sgpa")


# SGPA Calculator
@app.route("/sgpa", methods=["GET", "POST"])
def sgpa():
    sgpa_value = None
    credits = []
    grades = []

    if request.method == "POST":
        credits = request.form.getlist("credits")
        grades = request.form.getlist("grade")
        sgpa_value = calculate_sgpa(credits, grades)

    return render_template(
        "index.html",
        sgpa=sgpa_value,
        old_credits=credits,
        old_grades=grades,
        active_tab="sgpa",
    )


# CGPA Estimator
@app.route("/estimator", methods=["GET", "POST"])
def estimator():
    required_sgpa_value = None
    message = None

    if request.method == "POST":
        try:
            current_cgpa = float(request.form["current_cgpa"])
            current_credits = float(request.form["current_credits"])
            sem_credits = float(request.form["sem_credits"])
            target_cgpa = float(request.form["target_cgpa"])

            required_sgpa_value = required_sgpa(
                current_cgpa, current_credits, sem_credits, target_cgpa
            )

            if required_sgpa_value is None:
                message = "Semester credits cannot be zero"
            elif required_sgpa_value > 10:
                message = "Target not achievable (required SGPA > 10)"
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
        active_tab="estimator",
    )


# SGPA Finder
@app.route("/finder", methods=["GET", "POST"])
def finder():
    found_sgpa = None

    if request.method == "POST":
        try:
            prev_cgpa = float(request.form["prev_cgpa"])
            prev_credits = float(request.form["prev_credits"])
            new_cgpa = float(request.form["new_cgpa"])
            sem_credits = float(request.form["sem_credits"])

            found_sgpa = find_sgpa(prev_cgpa, prev_credits, new_cgpa, sem_credits)

        except Exception:
            found_sgpa = "Invalid input"

    return render_template(
        "index.html",
        found_sgpa=found_sgpa,
        active_tab="finder",
    )


# CALCULATION FUNCTIONS


def calculate_sgpa(credits, grades):
    total_points = 0
    total_credits = 0

    for i in range(len(credits)):
        try:
            c = float(credits[i])
            g = grades[i]

            total_points += c * grade_points[g]
            total_credits += c
        except Exception:
            continue

    if total_credits == 0:
        return None

    return round(total_points / total_credits, 3)


def required_sgpa(current_cgpa, current_credits, sem_credits, target_cgpa):
    if sem_credits == 0:
        return None

    total_after = current_credits + sem_credits
    sgpa = (
        (target_cgpa * total_after) - (current_cgpa * current_credits)
    ) / sem_credits

    return round(sgpa, 3)


def find_sgpa(prev_cgpa, prev_credits, new_cgpa, sem_credits):
    if sem_credits == 0:
        return None

    total_after = prev_credits + sem_credits
    sgpa = ((new_cgpa * total_after) - (prev_cgpa * prev_credits)) / sem_credits

    return round(sgpa, 3)


if __name__ == "__main__":
    app.run(debug=True)
