from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")

PROFILE = {
    "name": "Vishal Chauhan",
    "initials": "VC",
    "roles": [
        "Python Developer",
        "Flask Developer",
        "Full-Stack Enthusiast",
        "CS Undergraduate",
    ],
    "email": "vishalchauhan4849@gmail.com",
    "phone": "+91 90792 96316",
    "location": "Bhayandar, Mumbai, India",
    "github": "https://github.com/v595",
    "github_handle": "github.com/v595",
    "linkedin": "https://www.linkedin.com/in/vishal-chauhan-854780410",
    "linkedin_handle": "linkedin.com/in/vishal-chauhan",
    "resume": "files/VISHAL_CHAUHAN_Resume.pdf",
    "summary": (
        "Highly motivated and detail-oriented Computer Science student with a strong "
        "foundation in programming, web development, and database management. I build "
        "efficient, user-friendly applications with Python, Flask, HTML, CSS and "
        "JavaScript, and I'm always excited to learn new technologies and turn ideas "
        "into working software."
    ),
}

STATS = [
    {"value": 3, "suffix": "+", "label": "Projects Built"},
    {"value": 3, "suffix": "", "label": "Certifications"},
    {"value": 8, "suffix": "+", "label": "Technologies"},
    {"value": 2026, "suffix": "", "label": "Graduating Year"},
]

SKILLS = {
    "Languages": ["Python", "Java", "C++", "JavaScript"],
    "Web Development": ["HTML5", "CSS3", "Flask", "JavaScript"],
    "Database": ["MySQL", "SQLite"],
    "Tools & Platforms": ["Git", "GitHub", "VS Code"],
}

PROJECTS = [
    {
        "title": "Expense Tracker",
        "category": "Python  ·  Desktop & Web",
        "icon": "fa-solid fa-wallet",
        "description": (
            "A full-stack expense management application with expense tracking, "
            "budget monitoring, an analytics dashboard, category-wise reports and "
            "PDF export, wrapped in an interactive CustomTkinter interface."
        ),
        "stack": ["Python", "Flask", "SQLite", "CustomTkinter"],
        "github": "https://github.com/v595/expenses_tracker",
        "demo": "https://expenses-tracker-bysn.onrender.com/",
    },
    {
        "title": "Quiz Competition Web App",
        "category": "Python  ·  Flask  ·  Web",
        "icon": "fa-solid fa-clipboard-question",
        "description": (
            "An interactive online quiz platform with timer-based quizzes, automatic "
            "score calculation, multiple-choice questions and instant results, backed "
            "by a database that stores participants, questions and scores."
        ),
        "stack": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
        "github": "https://github.com/v595/QUIZ-COMPETITION",
        "demo": "https://quiz-competition-f83r.onrender.com/",
    },
    {
        "title": "Hotel Management System",
        "category": "Full-Stack  ·  Database",
        "icon": "fa-solid fa-hotel",
        "description": (
            "A hotel operations app streamlining room booking, customer management, "
            "billing, check-in/check-out and payment processing on top of an "
            "organized relational database."
        ),
        "stack": ["Python", "Flask", "HTML", "CSS", "MySQL"],
        "github": "https://github.com/v595/hotel-management-system",
        "demo": "https://hotel-management-system-luc1.onrender.com/",
    },
]

EDUCATION = {
    "degree": "Bachelor of Science (BSc) in Computer Science",
    "school": "Abhinav College",
    "school_url": "https://www.abhinavcollege.org/",
    "period": "2023 – 2026",
    "location": "Bhayandar, India",
}

CERTIFICATES = [
    {"title": "Python for Beginners", "issuer": "SimpliLearn", "icon": "fa-brands fa-python"},
    {"title": "Git and GitHub", "issuer": "SimpliLearn", "icon": "fa-brands fa-git-alt"},
    {"title": "Introduction to SQL", "issuer": "SimpliLearn", "icon": "fa-solid fa-database"},
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=PROFILE,
        stats=STATS,
        skills=SKILLS,
        projects=PROJECTS,
        education=EDUCATION,
        certificates=CERTIFICATES,
        year=datetime.now().year,
    )


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "error": "Please fill in every field."}), 400
    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"ok": False, "error": "Please enter a valid email address."}), 400

    os.makedirs(DATA_DIR, exist_ok=True)
    entry = {
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        except (json.JSONDecodeError, OSError):
            messages = []

    messages.append(entry)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    return jsonify({"ok": True, "message": "Thanks for reaching out! I'll get back to you soon."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, port=port)
