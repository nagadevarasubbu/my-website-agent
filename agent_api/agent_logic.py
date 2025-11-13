from typing import Dict, Any, List
import re
import json
from textwrap import dedent
import google.generativeai as genai
from agent_layer import refine_website_inputs

# ---------- CONFIGURE GEMINI ----------
# (Optional Bedrock Claude reference)
# from langchain_aws import ChatBedrock
# bedrock_model = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0", region_name="us-east-1")

# 🔑 Set Gemini key directly here
genai.configure(api_key="AIzaSyDagMyFx-dxUIs4xtdqU4newjP39HsN6nQ") 
gemini_model = genai.GenerativeModel("gemini-2.5-flash") 

# ---------- HELPERS ----------
def slug_hyphen(s: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.strip().lower())
    return re.sub(r'-+', '-', s).strip('-')

def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")

# ---------- THEME ----------
def pick_theme_color(website_type: str) -> str:
    wt = website_type.lower()
    if any(k in wt for k in ["hospital", "health", "clinic", "care"]): return "#4A63FF"
    if any(k in wt for k in ["gym", "fitness", "sports"]): return "#FF6B3D"
    if any(k in wt for k in ["spa", "yoga", "wellness"]): return "#6A8CAF"
    if any(k in wt for k in ["school", "education", "training"]): return "#8A5AFF"
    if any(k in wt for k in ["restaurant", "food", "hotel"]): return "#D96F32"
    if any(k in wt for k in ["tech", "software", "it", "digital"]): return "#0057FF"
    return "#4A63FF"

# ---------- GEMINI CONTENT GENERATOR ----------
def generate_sections_with_gemini(business_name: str, website_type: str, sections: List[str]) -> Dict[str, str]:
    prompt = dedent(f"""
        You are a professional AI website writer for any industry.

        business_name: {business_name}
        website_type: {website_type}
        sections: {sections}

        Write 5–6 paragraphs (350–500 words) per section.
        Make the tone professional yet friendly and domain-appropriate:
        - Hospitals → care, compassion, trust
        - Restaurants → taste, experience, ambiance
        - Tech → innovation, reliability, quality
        - Fitness → motivation, transformation, wellness
        - Education → learning, growth, empowerment

        Each section should be rich, structured, and human-like.

        Return JSON only:
        {{
          "sections": [
            {{ "title": "Section Name", "content": "Detailed text..." }}
          ]
        }}
    """)

    try:
        response = gemini_model.generate_content(prompt)
        data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        result = {}
        for sec in data.get("sections", []):
            if sec.get("title") and sec.get("content"):
                result[sec["title"]] = sec["content"]
        print("🧠 Gemini content generated successfully.")
        return result
    except Exception as e:
        print("⚠️ Gemini parsing failed:", e)
        return {}

# ---------- CHATBOT FAQs ----------
def get_chatbot_faqs(website_type: str):
    wt = website_type.lower()
    if "hospital" in wt:
        return {
            "How do I book an appointment?": "You can schedule an appointment online or contact our helpdesk at any time.",
            "Do you offer 24/7 emergency care?": "Yes, emergency and intensive care units are operational round the clock.",
            "Are health insurance cards accepted?": "We accept major insurance plans for cashless treatment.",
        }
    elif "restaurant" in wt:
        return {
            "Do you offer home delivery?": "Yes, we provide doorstep delivery through our delivery partners.",
            "Are vegan dishes available?": "Absolutely, we offer a variety of vegan and gluten-free dishes.",
            "Can I reserve a table online?": "Yes, online reservations are available directly through our website.",
        }
    elif "tech" in wt:
        return {
            "What services do you provide?": "We offer web, cloud, and AI-driven software solutions for businesses.",
            "How do you ensure project quality?": "Our QA team follows strict testing and agile development practices.",
            "Do you offer maintenance support?": "Yes, post-deployment maintenance and updates are included.",
        }
    else:
        return {
            "How can I contact you?": "You can reach us via the contact form or email for any inquiries.",
            "What services are offered?": "We provide tailored solutions based on your business needs.",
            "Where are you located?": "Our main office is located in the city center for easy accessibility.",
        }

# ---------- STYLES ----------
def build_styles(primary: str) -> str:
    return dedent(f"""
        :root {{
          --primary: {primary};
          --text: #1C1F33;
          --subtext: #545C6B;
          --border: #E6E8F0;
          --bg-light: #F9FAFE;
        }}
        body {{ margin:0; font-family:'Inter',system-ui,Arial; background:white; color:var(--text); line-height:1.7; }}
        .navbar {{ display:flex; justify-content:space-between; padding:22px 60px; border-bottom:1px solid var(--border); background:white; }}
        .navbar .brand {{ font-size:1.4rem; font-weight:600; }}
        .navbar .links a {{ margin-left:22px; text-decoration:none; color:var(--text); opacity:.85; font-weight:500; }}
        .navbar .links a:hover {{ color:var(--primary); opacity:1; }}
        .hero {{ position:relative; height:500px; overflow:hidden; }}
        .hero img {{ width:100%; height:100%; object-fit:cover; filter:brightness(0.6); }}
        .hero-content {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center; color:white; }}
        .hero-content h1 {{ font-size:3rem; margin-bottom:10px; font-weight:700; }}
        .hero-content p {{ font-size:1.2rem; opacity:0.9; margin-bottom:20px; }}
        section {{ padding:70px 80px; max-width:1100px; margin:auto; }}
        .section-body {{ display:flex; flex-direction:column; align-items:center; gap:25px; }}
        .section-body img {{ width:65%; border-radius:14px; object-fit:cover; }}
        .section-body p {{ font-size:1.12rem; color:var(--subtext); text-align:justify; line-height:1.8; }}
        #chatbot {{ position:fixed; bottom:20px; right:20px; background:var(--primary); color:white; border:none; border-radius:50%; width:55px; height:55px; cursor:pointer; font-size:22px; }}
        #chat-window {{ display:none; position:fixed; bottom:90px; right:20px; width:320px; background:white; border:1px solid var(--border); border-radius:10px; box-shadow:0 4px 20px rgba(0,0,0,0.1); }}
    """).strip()

# ---------- HOME ----------
def build_home_html(site_name: str, sections: List[str], theme: str, website_type: str) -> str:
    faqs = get_chatbot_faqs(website_type)
    faq_html = "".join([f"<p><b>{q}</b><br>{a}</p>" for q, a in faqs.items()])
    nav_links = " ".join(f"<a href='{slug_hyphen(s)}.html'>{html_escape(s)}</a>" for s in sections)
    cards = "\n".join(f"<div class='card'><h3>{html_escape(s)}</h3><p>Explore {html_escape(s)} to learn more.</p><a class='btn' href='{slug_hyphen(s)}.html'>View</a></div>" for s in sections)

    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>{html_escape(site_name)}</title><style>{build_styles(theme)}</style></head>
<body>
<nav class="navbar"><div class="brand">{html_escape(site_name)}</div><div class="links">{nav_links}</div></nav>
<section class="hero">
  <!-- IMAGE_PLACEHOLDER:home_hero -->
  <div class="hero-content"><h1>Welcome to {html_escape(site_name)}</h1><p>Discover excellence, innovation, and care with us.</p></div>
</section>
<section><h2 style="text-align:center;">Explore Our Sections</h2><div class="grid">{cards}</div></section>
<button id="chatbot">💬</button>
<div id="chat-window"><h4>Ask Us Anything</h4><div id="chat-content">{faq_html}</div></div>
<script>const chatBtn=document.getElementById('chatbot');const chatWin=document.getElementById('chat-window');chatBtn.addEventListener('click',()=>{{chatWin.style.display=chatWin.style.display==='none'?'block':'none';}});</script>
<footer>© {html_escape(site_name)}</footer></body></html>"""

# ---------- SECTION PAGE ----------
def build_section_html(site_name: str, section_name: str, summary_text: str, theme: str) -> str:
    sid = slug_hyphen(section_name)
    parts = [p.strip() for p in summary_text.split("\n\n") if p.strip()]
    while len(parts) < 5:
        parts.append(parts[-1])
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html_escape(section_name)} — {html_escape(site_name)}</title><style>{build_styles(theme)}</style></head>
<body><nav class="navbar"><a class="btn" href="index.html">← Back</a><div class="brand">{html_escape(section_name)}</div></nav>
<section class="section-body">
<p>{html_escape(parts[0])}</p><!-- IMAGE_PLACEHOLDER:{sid}_img1 -->
<p>{html_escape(parts[1])}</p><!-- IMAGE_PLACEHOLDER:{sid}_img2 -->
<p>{html_escape(parts[2])}</p><p>{html_escape(parts[3])}</p><p>{html_escape(parts[4])}</p>
</section><footer>© {html_escape(site_name)}</footer></body></html>"""

# ---------- IMAGES + AUDIO ----------
def make_image_prompts(website_type: str, site_name: str, sections_4: List[str]):
    prompts = [{"id": "home_hero", "description": f"Wide, cinematic hero image for '{site_name}' ({website_type}). Vibrant, realistic, natural lighting, professional look."}]
    for sec in sections_4:
        sid = slug_hyphen(sec)
        prompts.append({"id": f"{sid}_img1", "description": f"Primary image for '{sec}' showing authentic visuals of {website_type}. High clarity, modern style, human context."})
        prompts.append({"id": f"{sid}_img2", "description": f"Supporting image for '{sec}' focusing on trust, connection, and professionalism."})
    return prompts

def make_site_narration(site_name: str, website_type: str, sections_4: List[str]):
    listed = ", ".join(sections_4[:-1]) + ", and " + sections_4[-1]
    return f"Welcome to {site_name}, your trusted destination for {website_type}. Explore {listed}, and experience our commitment to quality and excellence."

# ---------- MAIN ----------
def generate_website_package(payload: Dict[str, Any]):
    website_type = (payload.get("website_type") or "business").strip()
    business_name = payload.get("business_name") or "My Website"
    sections_all = payload.get("sections_required") or []
    refined = refine_website_inputs(business_name, website_type, sections_all)
    business_name, website_type, sections_all = refined["business_name"], refined["website_type"], refined["sections"]
    sections_4 = sections_all[:4] or ["About", "Services", "Team", "Contact"]
    theme = pick_theme_color(website_type)
    sections_content = generate_sections_with_gemini(business_name, website_type, sections_4)
    pages = [{"filename": "index.html", "html_file": build_home_html(business_name, sections_4, theme, website_type)}]
    for sec in sections_4:
        text = sections_content.get(sec) or "Content unavailable."
        pages.append({"filename": f"{slug_hyphen(sec)}.html", "html_file": build_section_html(business_name, sec, text, theme)})
    return {"pages": pages, "images_needed": make_image_prompts(website_type, business_name, sections_4), "voice_scripts_needed": [{"id": "site_intro", "script": make_site_narration(business_name, website_type, sections_4)}], "callback_url_for_assets": payload.get("callback_url_for_assets") or "http://54.167.58.174:9000/submit-assets"}

