from typing import Dict, Any, List

def build_home_page_html(website_name: str) -> str:
    return f"""
<!doctype html>
<html>
<head>
    <title>{website_name}</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<nav class="navbar">
    <div class="brand">{website_name}</div>
</nav>

<section id="hero" class="hero-section">
    <!-- IMAGE_PLACEHOLDER:hero -->
    <div class="hero-overlay">
        <h1>Your Health, Our Priority.</h1>
        <p>Providing compassionate and advanced healthcare for our community.</p>
        <button class="voice-btn" onclick="document.getElementById('audio_hero').play()">&#128266; Listen</button>
        <audio id="audio_hero" src="assets/audio/audio_hero.mp3"></audio>
    </div>
</section>

<section id="departments">
    <h2>Departments</h2>
    <p>Explore our medical specialties.</p>
    <!-- IMAGE_PLACEHOLDER:departments -->
    <button class="voice-btn" onclick="document.getElementById('audio_departments').play()">&#128266; Listen</button>
    <audio id="audio_departments" src="assets/audio/audio_departments.mp3"></audio>
    <a class="cta" href="departments.html">View Departments →</a>
</section>

<section id="doctors">
    <h2>Our Doctors</h2>
    <p>Meet our experienced medical professionals.</p>
    <!-- IMAGE_PLACEHOLDER:doctors -->
    <button class="voice-btn" onclick="document.getElementById('audio_doctors').play()">&#128266; Listen</button>
    <audio id="audio_doctors" src="assets/audio/audio_doctors.mp3"></audio>
    <a class="cta" href="doctors.html">View Doctors →</a>
</section>

<section id="contact">
    <h2>Contact Us</h2>
    <p>Email: info@citycarehospital.org | Phone: (555) 123-4567</p>
    <!-- IMAGE_PLACEHOLDER:contact -->
    <button class="voice-btn" onclick="document.getElementById('audio_contact').play()">&#128266; Listen</button>
    <audio id="audio_contact" src="assets/audio/audio_contact.mp3"></audio>
</section>

<footer class="footer">
    <p>© {website_name} — Powered by AI Website Agent</p>
</footer>

</body>
</html>
"""


def generate_website_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    website_name = payload.get("business_name", "City Care Hospital")

    # Pages your AI agent will return
    home_html = build_home_page_html(website_name)
    doctors_page = "<h1>Doctors Page (details coming soon)</h1>"
    departments_page = "<h1>Departments Page (details coming soon)</h1>"

    # Asset requirements for image & voice teams
    section_ids = ["hero", "departments", "doctors", "contact"]
    images_needed = [{"id": s, "description": f"Image needed for {s} section"} for s in section_ids]
    voices_needed = [{"id": s, "script": f"Voice narration for {s} section"} for s in section_ids]

    return {
        "pages": [
            {"page_name": "home", "filename": "index.html", "html_file": home_html},
            {"page_name": "doctors", "filename": "doctors.html", "html_file": doctors_page},
            {"page_name": "departments", "filename": "departments.html", "html_file": departments_page},
        ],
        "images_needed": images_needed,
        "voice_scripts_needed": voices_needed,
        "callback_url_for_assets": "https://<your-backend-url>/submit-assets"
    }
