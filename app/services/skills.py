import json
import spacy
from spacy.matcher import PhraseMatcher

# Load the English model once when the app starts
nlp = spacy.load("en_core_web_sm")

# Load the skills list from data/skills.json
with open("data/skills.json", "r", encoding="utf-8") as f:
    SKILLS = json.load(f)

# Map lowercase -> original spelling, so output is clean ("Python", not "python")
SKILL_LOOKUP = {skill.lower(): skill for skill in SKILLS}

# Build the matcher once (case-insensitive via attr="LOWER")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS]
matcher.add("SKILLS", patterns)


def extract_skills(text: str) -> list:
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        span_text = doc[start:end].text.lower()
        canonical = SKILL_LOOKUP.get(span_text, span_text)
        found.add(canonical)
    return sorted(found)
