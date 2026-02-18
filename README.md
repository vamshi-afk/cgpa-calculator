Got you 👍 — here is **ONE clean single README** for your **main (Flask) branch**.
Simple, clear, no extra fluff, ready to paste as `README.md`.

---

````md
# GPA Toolkit

A simple web application to calculate SGPA and estimate required SGPA for a target CGPA.

This project is built using **Python (Flask)** for local usage and also has a static GitHub Pages version for quick access.

---

## Features

- SGPA Calculator using subject credits and grades
- CGPA Estimator (calculate required SGPA to reach target CGPA)
- Custom grade mapping
- Clean minimal dark UI
- Responsive layout
- No database required

---

## Grade Mapping

| Grade | Points |
|-------|--------|
| S     | 10 |
| A+    | 9 |
| A     | 8 |
| B+    | 7 |
| B     | 6 |
| C     | 5 |
| P     | 4 |
| D     | 2 |
| E     | 1 |
| NC    | 0 |

---

## Run Locally

### Clone repository

```bash
git clone https://github.com/vamshi-afk/cgpa-calculator.git
cd cgpa-calculator
git checkout main
````

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Flask

```bash
pip install flask
```

### Run the application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## Project Structure

```
cgpa-calculator/
│
├── app.py
├── templates/
│   └── index.html
├── requirements.txt (optional)
└── README.md
```

---

## Branches

* **main** → Flask backend version
* **pages** → Static HTML version (GitHub Pages)

Live static version:
[https://vamshi-afk.github.io/cgpa-calculator/](https://vamshi-afk.github.io/cgpa-calculator/)

---

## Notes

* This tool is intended for personal academic planning.
* No user data is stored.
* Works fully offline when run locally.

---

## License

MIT License
