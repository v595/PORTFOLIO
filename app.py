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
        "Backend Developer",
        "Full-Stack Developer",
        "React Developer",
        "Flask Developer",
        "AI Automation Developer",
    ],
    "headline": "Python & React Full-Stack Developer",
    "tagline": "Building modern web applications with Python, Flask, React, PostgreSQL and AI automation.",
    "hero_desc": (
        "Full-stack developer with hands-on professional experience building and "
        "improving real-world web applications across React frontend development, "
        "Python Flask backend development, PostgreSQL, UI/UX implementation, AI "
        "automation and server-side development."
    ),
    "about_text": (
        "I'm a Python and React Full-Stack Developer with hands-on professional "
        "experience working on real-world web applications. My experience spans "
        "React frontend development, Python Flask backend development, PostgreSQL, "
        "UI/UX implementation, AI automation and server-side tasks."
    ),
    "email": "vishalchauhan4849@gmail.com",
    "phone": "+91 90792 96316",
    "location": "Bhayandar, Mumbai, India",
    "github": "https://github.com/v595",
    "github_handle": "github.com/v595",
    "linkedin": "https://www.linkedin.com/in/vishal-chauhan-854780410",
    "linkedin_handle": "linkedin.com/in/vishal-chauhan",
    "resume": "files/VISHAL_CHAUHAN_Resume.pdf",
}

STATS = [
    {"value": 4, "suffix": "+", "label": "Personal Projects"},
    {"value": 5, "suffix": "", "label": "Professional Platforms"},
    {"value": 10, "suffix": "+", "label": "Technologies"},
    {"value": 105, "suffix": "", "label": "Days Experience"},
]

SKILLS = {
    "Programming Languages": ["Python", "Java", "C++", "JavaScript", "SQL"],
    "Frontend": ["React", "JavaScript", "HTML5", "CSS3", "Responsive Design"],
    "Backend": ["Python", "Flask", "REST APIs", "Backend Development"],
    "Databases": ["PostgreSQL", "MySQL", "SQLite", "SQLAlchemy"],
    "AI & Automation": ["AI Automation", "Automation Workflows", "AI-Powered Applications"],
    "Tools & Platforms": ["Git", "GitHub", "VS Code", "API Integration", "Server-side Dev"],
}

EXPERIENCE = {
    "role": "AI Automation / Full-Stack Developer",
    "company": "MCM BPO",
    "location": "Jogeshwari West, Mohim Nagar, Mumbai",
    "period": "3 June 2026 – 20 September 2026",
    "duration_value": 105,
    "duration_label": "Days",
    "points": [
        "Contributed to AI automation and full-stack web development projects in a professional development environment.",
        "Developed and improved user interfaces for multiple web applications using React.",
        "Built and maintained backend functionality using Python and Flask.",
        "Worked with PostgreSQL and relational databases for data storage and integration.",
        "Implemented and maintained REST API integrations and backend services.",
        "Handled server-side configuration, deployment and maintenance tasks.",
        "Collaborated on real-world client web applications across frontend and backend.",
        "Improved UI/UX, responsive layouts and user flows across projects.",
        "Contributed to AI automation-related functionality and workflows.",
    ],
    "badges": ["React", "Python", "Flask", "PostgreSQL", "AI Automation", "UI/UX", "Backend", "Server"],
}

PROFESSIONAL_PROJECTS = [
    {
        "name": "UCaaS",
        "featured": True,
        "icon": "fa-solid fa-server",
        "role": "Full-Stack Contributor — Frontend, Backend & Server",
        "desc": "Contributed across frontend, backend and server-side development on this application.",
        "stack_breakdown": [
            {"label": "Frontend", "icon": "fa-brands fa-react", "points": ["React development", "UI/UX implementation", "Application functionality"]},
            {"label": "Backend", "icon": "fa-solid fa-code", "points": ["Python & Flask", "API / backend functionality", "Database integration"]},
            {"label": "Server", "icon": "fa-solid fa-server", "points": ["Server-side configuration", "Application deployment", "Maintenance & upkeep"]},
        ],
        "badges": ["React", "Python", "Flask", "PostgreSQL", "Backend", "Server", "UI/UX"],
        "link": "https://app.ucaas.in/",
        "cta": "Visit Application",
    },
    {
        "name": "Kallus",
        "icon": "fa-solid fa-headset",
        "role": "Frontend / UI-UX Contributor",
        "desc": "Contributed to UI/UX and frontend functionality on this platform.",
        "contrib": [
            "Worked on UI/UX design and interface improvements",
            "Contributed to React-based frontend development",
            "Improved application functionality and layouts",
        ],
        "badges": ["React", "JavaScript", "UI/UX"],
        "link": "https://www.kallus.io/",
        "cta": "Visit Website",
    },
    {
        "name": "9278",
        "icon": "fa-solid fa-microphone-lines",
        "role": "Frontend / UI-UX Contributor",
        "desc": "Contributed to UI/UX and frontend functionality on this web application.",
        "contrib": [
            "Worked on UI/UX and interface improvements",
            "Contributed to React frontend development",
            "Improved web application functionality",
        ],
        "badges": ["React", "JavaScript", "UI/UX"],
        "link": "https://www.9278.io/",
        "cta": "Visit Website",
    },
    {
        "name": "9278 AI",
        "icon": "fa-solid fa-robot",
        "role": "Frontend / AI Web App Contributor",
        "desc": "Contributed to UI/UX and frontend functionality on this AI-related web application.",
        "contrib": [
            "Worked on UI/UX and interface improvements",
            "Contributed to React-based frontend development",
            "Worked on AI-related web application functionality",
        ],
        "badges": ["React", "JavaScript", "UI/UX", "AI Automation"],
        "link": "https://www.9278.ai/",
        "cta": "Visit Website",
    },
    {
        "name": "Unified — MyCountryMobile",
        "icon": "fa-solid fa-tower-broadcast",
        "role": "Frontend / UI-UX Contributor",
        "desc": "Contributed to UI/UX and frontend functionality on this platform.",
        "contrib": [
            "Worked on UI/UX design and improvements",
            "Contributed to React-related frontend development",
            "Improved application functionality",
        ],
        "badges": ["React", "JavaScript", "UI/UX"],
        "link": "https://unified.mycountrymobile.com/",
        "cta": "Visit Website",
    },
]

PROJECTS = [
    {
        "title": "RailBite — Railway Food Delivery",
        "category": "Full-Stack  ·  Flask  ·  Web",
        "icon": "fa-solid fa-bowl-food",
        "summary": "An IRCTC e-catering style food delivery platform for train passengers.",
        "problem": "Solves the lack of reliable, trackable food ordering for passengers during train journeys.",
        "features": [
            "PNR-based train route and stop resolution",
            "240+ branded dishes to order from",
            "Live delivery status tracking",
            "Group ordering split by PNR with co-passengers",
            "Vendor dashboard for order management",
        ],
        "stack": ["Python", "Flask", "SQLAlchemy", "SQLite", "JavaScript"],
        "github": "https://github.com/v595/railway_fd",
        "demo": "https://railway-fd.onrender.com",
        "featured": True,
        "image": "files/screenshots/railbite.jpg",
        "image_alt": "RailBite train food delivery app home screen showing PNR search and partner restaurant brands",
    },
    {
        "title": "Expense Tracker",
        "category": "Python  ·  Desktop & Web",
        "icon": "fa-solid fa-wallet",
        "summary": "A full-stack expense management application with budgeting and analytics.",
        "problem": "Solves manual, unstructured expense tracking with no visibility into spending patterns.",
        "features": [
            "Expense tracking and category-wise budget monitoring",
            "Analytics dashboard with spending reports",
            "PDF export of expense reports",
            "Interactive CustomTkinter desktop interface",
        ],
        "stack": ["Python", "Flask", "SQLite", "CustomTkinter"],
        "github": "https://github.com/v595/expenses_tracker",
        "demo": "https://expenses-tracker-bysn.onrender.com/",
        "image": "files/screenshots/expense-tracker.jpg",
        "image_alt": "Expense Tracker sign-in screen with email and password fields",
    },
    {
        "title": "Hotel Management System",
        "category": "Full-Stack  ·  Database",
        "icon": "fa-solid fa-hotel",
        "summary": "A hotel operations app for bookings, billing and stay management.",
        "problem": "Solves fragmented, manual handling of room booking, billing and guest records.",
        "features": [
            "Room booking and customer management",
            "Billing and payment processing",
            "Check-in / check-out workflows",
            "Organized relational database structure",
        ],
        "stack": ["Python", "Flask", "HTML", "CSS", "MySQL"],
        "github": "https://github.com/v595/hotel-management-system",
        "demo": "https://hotel-management-system-luc1.onrender.com/",
        "image": "files/screenshots/hotel-management.jpg",
        "image_alt": "Hotel Management System landing page for a luxury hotel booking site",
    },
    {
        "title": "Quiz Competition Web App",
        "category": "Python  ·  Flask  ·  Web",
        "icon": "fa-solid fa-clipboard-question",
        "summary": "An interactive, timer-based online quiz platform with instant scoring.",
        "problem": "Solves the need for a fast, automated way to run and score multi-participant quizzes.",
        "features": [
            "Timer-based quizzes with multiple-choice questions",
            "Automatic score calculation and instant results",
            "Database storage for participants, questions and scores",
        ],
        "stack": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
        "github": "https://github.com/v595/QUIZ-COMPETITION",
        "demo": "https://quiz-competition-f83r.onrender.com/",
        "image": "files/screenshots/quiz-competition.jpg",
        "image_alt": "Quiz Competition web app sign-in screen with quiz category chips",
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
        experience=EXPERIENCE,
        professional_projects=PROFESSIONAL_PROJECTS,
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
