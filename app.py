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


@app.route("/")
def home():
    return render_template("index.html")


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
        "index.html", sgpa=sgpa_value, old_credits=credits, old_grades=grades
    )


@app.route("/estimator", methods=["GET", "POST"])
def estimator():
    required_sgpa = None
    message = None

    if request.method == "POST":
        try:
            current_cgpa = float(request.form["current_cgpa"])
            current_credits = float(request.form["current_credits"])
            sem_credits = float(request.form["sem_credits"])
            target_cgpa = float(request.form["target_cgpa"])

            required_sgpa = required_sgpa(
                current_cgpa, current_credits, sem_credits, target_cgpa
            )

            if required_sgpa > 10:
                message = "Target not Achievable,  required sgpa >10"
            elif required_sgpa < 0:
                message = (
                    "Target already Achieved, if wrong please check your target cgpa"
                )
            else:
                message = "Target Achievable"
        except Exception:
            message = "Invalid Input"

    return render_template(
        "estimator.html", required_sgpa=required_sgpa, message=message
    )


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
            found_sgpa = "Invalid Input"

    return render_template("finder.html", sgpa=found_sgpa)


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

    tc_after = current_credits + sem_credits
    sgpa = (target_cgpa * tc_after - current_cgpa * current_credits) / sem_credits

    return round(sgpa, 3)


def find_sgpa(prev_cgpa, prev_credits, new_cgpa, sem_credits):
    if sem_credits == 0:
        return None

    tc_after = sem_credits + prev_credits
    sgpa = (new_cgpa * tc_after - prev_cgpa * prev_credits) / sem_credits

    return round(sgpa, 3)


if __name__ == "__main__":
    app.run(debug=True)
