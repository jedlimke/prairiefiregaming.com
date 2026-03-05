"""
Converts all .docx files in rules/den-of-wolves-2026/temp-assets to markdown.
Smart/curly quotes are normalized to straight ASCII quotes.
"""
from docx import Document
from docx.oxml.ns import qn
import re, os, glob

IMAGE_PLACEHOLDER = "❌"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_ASSETS = os.path.join(SCRIPT_DIR, "..", "rules", "den-of-wolves-2026", "temp-assets")


QUOTE_MAP = {
    "\u2018": "'",   # left single quotation mark
    "\u2019": "'",   # right single quotation mark  (apostrophe too)
    "\u201a": "'",   # single low-9 quotation mark
    "\u201b": "'",   # single high-reversed-9 quotation mark
    "\u201c": '"',   # left double quotation mark
    "\u201d": '"',   # right double quotation mark
    "\u201e": '"',   # double low-9 quotation mark
    "\u201f": '"',   # double high-reversed-9 quotation mark
    "\u2032": "'",   # prime
    "\u2033": '"',   # double prime
    "\u02bc": "'",   # modifier letter apostrophe
}


def normalize_quotes(text):
    for src, dst in QUOTE_MAP.items():
        text = text.replace(src, dst)
    return text


def has_image(para):
    return bool(para._p.findall(".//" + qn("a:blip")))


def run_has_image(run):
    return bool(run._r.findall(".//" + qn("a:blip")))


def heading_level(para):
    m = re.match(r"Heading (\d+)", para.style.name)
    return int(m.group(1)) if m else 0


def para_to_md(para):
    level = heading_level(para)

    if has_image(para):
        return IMAGE_PLACEHOLDER

    parts = []
    for run in para.runs:
        text = normalize_quotes(run.text)
        if not text:
            if run_has_image(run):
                parts.append(IMAGE_PLACEHOLDER)
            continue
        if run.bold and run.italic:
            text = f"***{text}***"
        elif run.bold:
            text = f"**{text}**"
        elif run.italic:
            text = f"*{text}*"
        parts.append(text)

    line = "".join(parts)

    if level:
        return "#" * level + " " + line

    style = para.style.name
    if "List Bullet" in style:
        return f"- {line}"
    if "List Number" in style:
        return f"1. {line}"

    return line


def docx_to_body(path):
    doc = Document(path)
    lines = []
    prev_blank = False

    for para in doc.paragraphs:
        md = para_to_md(para)
        if md.strip() == "":
            if not prev_blank and lines:
                lines.append("")
            prev_blank = True
        else:
            lines.append(md)
            prev_blank = False

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


docx_files = sorted(glob.glob(os.path.join(TEMP_ASSETS, "*.docx")))

if not docx_files:
    print(f"No .docx files found in {TEMP_ASSETS}")
else:
    for docx_path in docx_files:
        stem = os.path.splitext(os.path.basename(docx_path))[0]
        md_filename = stem.lower().replace(" ", "-") + ".md"
        md_path = os.path.join(TEMP_ASSETS, md_filename)
        print(f"Converting {os.path.basename(docx_path)} ...")
        body = docx_to_body(docx_path)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(body + "\n")
        print(f"  -> wrote {md_filename}")

print("Done.")
