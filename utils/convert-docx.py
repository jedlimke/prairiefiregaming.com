"""
Temporary one-shot converter: docx → markdown stubs.
Delete this file after use.
"""
from docx import Document
from docx.oxml.ns import qn
import re, os

IMAGE_PLACEHOLDER = "❌"
BASE = os.path.dirname(__file__) + "/rules/den-of-wolves-2026"


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
        text = run.text
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


CONVERSIONS = [
    (
        f"{BASE}/Background Guide.docx",
        f"{BASE}/background-guide.md",
        "Background Guide",
        "/rules/den-of-wolves-2026/background-guide/",
        2,
    ),
    (
        f"{BASE}/Rules Handbook.docx",
        f"{BASE}/rules-handbook.md",
        "Full Rules Handbook",
        "/rules/den-of-wolves-2026/rules-handbook/",
        3,
    ),
]

for docx_path, md_path, title, permalink, nav_order in CONVERSIONS:
    print(f"Converting {docx_path} ...")
    body = docx_to_body(docx_path)
    frontmatter = (
        f'---\n'
        f'title: "{title}"\n'
        f'link_title: "{title}"\n'
        f'permalink: {permalink}\n'
        f'nav_order: {nav_order}\n'
        f'---\n\n'
    )
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + body + "\n")
    print(f"  → wrote {md_path}")

print("Done.")
