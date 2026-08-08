# Vishal Chauhan — Portfolio

A personal portfolio site built with **Python, Flask, HTML, CSS and vanilla JavaScript**,
featuring a blue-and-black theme with animated backgrounds, scroll reveals, a typing
hero effect and a working contact form.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Structure

- `app.py` — Flask app: routes, profile/project/skill data, contact endpoint
- `templates/index.html` — single-page layout (Jinja2)
- `static/css/style.css` — theme, layout, animations
- `static/js/script.js` — typing effect, scroll reveals, particle background, contact form
- `static/files/` — downloadable resume
- `data/messages.json` — messages submitted via the contact form (created at runtime)
