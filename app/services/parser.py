import io
import re
import pdfplumber
from docx import Document


SECTION_HEADERS = {
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "work experience", "professional experience", "employment"],
    "skills": ["skills", "technical skills", "core competencies", "technologies"],
    "projects": ["projects", "personal projects", "academic projects"],
    "certifications": ["certifications", "certificates", "achievements"],
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = Document(io.BytesIO(file_bytes))
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text


def clean_text(text: str) -> str:
    # Turn various bullet symbols into a simple dash
    text = re.sub(r"[•▪◦‣·]", "-", text)
    cleaned_lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def _match_header(line: str):
    lowered = line.lower().strip()
    if len(lowered) > 40:          # real headers are short
        return None
    for section, aliases in SECTION_HEADERS.items():
        for alias in aliases:
            if lowered == alias or lowered.startswith(alias):
                return section
    return None


def split_into_sections(text: str) -> dict:
    cleaned = clean_text(text)
    sections = {key: "" for key in SECTION_HEADERS}
    sections["other"] = ""        # name, contact info, anything unmatched

    current = "other"
    for line in cleaned.splitlines():
        header = _match_header(line)
        if header:
            current = header
        else:
            sections[current] += line + "\n"

    return {key: value.strip() for key, value in sections.items()}