from typing import Dict, Any, List

# Library of auto templates for any business category
TEMPLATES = {
    "hospital": [
        {"id": "hero", "title": "Your Health, Our Priority.", "content": "Providing compassionate and advanced healthcare for our community."},
        {"id": "departments", "title": "Departments", "content": "Explore our medical specialties → click for details."},
        {"id": "doctors", "title": "Our Doctors", "content": "Meet our expert medical professionals."},
        {"id": "contact", "title": "Contact Us", "content": "Email: info@citycarehospital.org | Phone: (555) 123-4567"}
    ],
    "gym": [
        {"id": "hero", "title": "Transform Your Body.", "content": "Professional fitness training tailored to your goals."},
        {"id": "programs", "title": "Training Programs", "content": "Strength, Cardio, HIIT, Yoga & more."},
        {"id": "trainers", "title": "Our Trainers", "content": "Certified and experienced coaches to guide you."},
        {"id": "contact", "title": "Join Us", "content": "Email: info@fitclub.com | Phone: (555) 555-2020"}
    ],
    "restaurant": [
        {"id": "hero", "title": "Welcome to Our Kitchen.", "content": "Serving fresh, delicious meals with love."},
        {"id": "menu", "title": "Menu", "content": "Explore our signature dishes and seasonal specials."},
        {"id": "chefs", "title": "Our Chefs", "content": "Meet the culinary artists behind your favorite meals."},
        {"id": "contact", "title": "Reservations", "content": "Call or reserve your table online."}
    ],
    "school": [
        {"id": "hero", "title": "Shaping Tomorrow.", "content": "Quality education for inspiring young minds."},
        {"id": "academics", "title": "Academics", "content": "Comprehensive curriculum designed for growth."},
        {"id": "faculty", "title": "Our Teachers", "content": "Experienced educators dedicated to student success."},
        {"id": "contact", "title": "Admissions", "content": "Apply now for the new academic year."}
    ]
}

# fallback if unknown type
DEFAULT_TEMPLATE = [
    {"id": "hero", "title": "Welcome!", "content": "Discover what we offer."},
    {"id": "about", "title": "About Us", "content": "We are committed to excellence."},
    {"id": "services", "title": "Our Services", "content": "Here is what we provide."},
    {"id": "contact", "title": "Contact Us", "content": "Get in touch with us anytime."}
]


def build_page_html(website_name: str, sections: List[Dict[str, str]]) -> str:
    html_sections = ""
    for section in sections:
        sec_id = section["id"]
        title = section["title"]
        content = section["content"]

        image_placeholder = f"<!-- IMAGE_PLACEHOLDER:{sec_id} -->"

        voice_block = f"""
        <button class="voice-btn" onclick="document.getElementById('audio_{sec_id}').play()">🔊 Listen</button>
        <audio id="audio_{sec_id}" src="assets/audio/audio_{sec_id}.mp3"></audio>
        """

        html_sections += f"""
        <section id="{sec_id}">
            <h2>{title}</h2>
            <p>{content}</p>
            {image_placeholder}
            {voice_block}
        </section>
        """

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

{html_sections}

<footer class="footer">
    <p>© {website_name} — Powered by AI Website Agent</p>
</footer>

</body>
</html>
"""


def generate_website_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    website_name = payload.get("business_name", "My Website")
    use_case = payload.get("website_type", "").lower()

    sections = TEMPLATES.get(use_case, DEFAULT_TEMPLATE)

    html = build_page_html(website_name, sections)

    images_needed = [{"id": sec["id"], "description": f"Image for {sec['title']}"} for sec in sections]
    voices_needed = [{"id": sec["id"], "script": sec["content"]} for sec in sections]

    return {
        "pages": [
            {"page_name": "home", "filename": "index.html", "html_file": html}
        ],
        "images_needed": images_needed,
        "voice_scripts_needed": voices_needed,
        "callback_url_for_assets": "https://explanation-cigarette-worldwide-supreme.trycloudflare.com "
    }
