#!/usr/bin/env python3
"""Build files/cv.pdf from the same records that power the website.

Usage: python scripts/build_cv.py
Dependencies: pip install -r requirements-cv.txt
"""
import json
from datetime import datetime
from html import escape
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether,
    HRFlowable, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
CV = json.loads((ROOT / "_data/cv.json").read_text())
PAPERS = yaml.safe_load((ROOT / "_data/research.yml").read_text())["published"]
OUT = ROOT / "files/cv.pdf"
INK, MUTED, ACCENT = "#242724", "#626963", "#315f7e"


def setup_fonts():
    # ReportLab includes Bitstream Vera: embed fonts for portable Unicode text.
    import reportlab
    fonts = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("CV", str(fonts / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("CV-Bold", str(fonts / "VeraBd.ttf")))
    pdfmetrics.registerFontFamily("CV", normal="CV", bold="CV-Bold")


def text(value):
    return escape(str(value).replace("—", "-").replace("–", "-").replace("‑", "-"))


def month(value):
    return datetime.strptime(value, "%Y-%m").strftime("%b %Y") if value != "Present" else value


setup_fonts()
STYLES = {
    "body": ParagraphStyle("body", fontName="CV", fontSize=8.5, leading=12.7, textColor=colors.HexColor(INK), spaceAfter=5),
    "small": ParagraphStyle("small", fontName="CV", fontSize=7.4, leading=11, textColor=colors.HexColor(MUTED), spaceAfter=5),
    "heading": ParagraphStyle("heading", fontName="CV-Bold", fontSize=13, leading=17, textColor=colors.HexColor(INK), spaceBefore=13, spaceAfter=9, keepWithNext=True),
    "title": ParagraphStyle("title", fontName="CV-Bold", fontSize=28, leading=34, textColor=colors.HexColor(INK), spaceAfter=8),
    "label": ParagraphStyle("label", fontName="CV-Bold", fontSize=9, leading=13, textColor=colors.HexColor(INK), spaceAfter=4),
    "date": ParagraphStyle("date", fontName="CV", fontSize=7.3, leading=11, textColor=colors.HexColor(MUTED), alignment=TA_RIGHT),
}


def p(value, style="body"):
    return Paragraph(value, STYLES[style])


def section(title):
    return [p(text(title), "heading"), HRFlowable(width="100%", thickness=.45, color=colors.HexColor("#d5d8cf")), Spacer(1, 7)]


def dated(title, date, description):
    row = Table([[p(title, "label"), p(text(date), "date")]], colWidths=[365, 118])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([row, p(description), Spacer(1, 5)])


def footer(canvas, doc):
    canvas.setTitle("Vaibhav Rathore - Curriculum Vitae")
    canvas.setAuthor("Vaibhav Rathore")
    canvas.setStrokeColor(colors.HexColor("#d5d8cf"))
    canvas.line(56, 43, A4[0] - 56, 43)
    canvas.setFillColor(colors.HexColor(MUTED))
    canvas.setFont("CV", 7)
    canvas.drawString(56, 29, "Vaibhav Rathore  /  Curriculum vitae  /  Updated " + CV["updated"])
    canvas.drawRightString(A4[0] - 56, 29, str(doc.page))


story = [p(text(CV["basics"]["name"]), "title"), p(text(CV["basics"]["summary"]))]
story.append(p("Mumbai, India  ·  " + text(CV["basics"]["email"]), "small"))
links = [(profile["network"], profile["url"]) for profile in CV["basics"]["profiles"]]
links.insert(0, ("Website", CV["basics"]["website"]))
story.append(p("  ·  ".join('<a href="' + text(url) + '" color="' + ACCENT + '">' + text(label) + "</a>" for label, url in links), "small"))
story += section("Experience")
for job in CV["work"]:
    story.append(dated(text(job["position"]), month(job["startDate"]) + " - " + month(job["endDate"]), "<b>" + text(job["company"]) + "</b><br/>" + text(job["summary"])))
story += section("Education")
for item in CV["education"][:3]:
    story.append(dated(text(item["studyType"] + " · " + item["institution"]), item["startDate"] + " - " + item["endDate"], text(item["area"]) + " · CPI " + text(item["gpa"])))

story.append(PageBreak())
story += section("Recognition")
for award in CV["awards"]:
    story.append(dated(text(award["title"]), datetime.strptime(award["date"], "%Y-%m-%d").strftime("%d %b %Y"), text(award["awarder"] + ". " + award["summary"])))
for item in CV["achievements"]:
    story.append(dated(text(item["title"]), item["year"], text(item["summary"])))
story += section("Teaching & mentoring")
for item in CV["teaching"]:
    story.append(dated(text(item["course"]), item["date"], text(item["role"] + ", " + item["institution"])))
for item in CV["mentoring"]:
    story.append(dated(text(item["role"] + " · " + item["institution"]), item["date"], text(item["summary"])))
story += section("Academic service")
for item in CV["service"]:
    story.append(p("<b>" + text(item["name"]) + "</b> · " + text(item["role"] + " · " + item["year"])))
story += section("Skills & research interests")
for group in CV["skills"] + CV["interests"]:
    story.append(p(text(" · ".join(group["keywords"]))))
story += section("Selected coursework")
for item in CV["education"][:2]:
    story.append(p("<b>" + text(item["studyType"] + " · " + item["institution"]) + "</b><br/>" + text(" · ".join(item["courses"]))))
story += section("Earlier education")
for item in CV["education"][3:]:
    story.append(p(text(item["studyType"] + " · " + item["institution"] + " · " + item["startDate"] + "-" + item["endDate"] + " · " + item["gpa"])))

for group, title in [("main", "Conferences & journals"), ("workshop", "Workshops & posters")]:
    story.append(PageBreak())
    story += section(title)
    story.append(p("Published and accepted work. Acceptance is not a claim of completed presentation or archival publication.", "small"))
    for paper in [item for item in PAPERS if item["group"] == group]:
        venue = paper["venue"] + " · " + paper["status"]
        if paper.get("note"):
            venue += " · " + paper["note"]
        author_line = text(paper["authors"]).replace("Vaibhav Rathore", "<b>Vaibhav Rathore</b>")
        entry = [p(text(paper["title"]), "label"), p(text(venue), "small"), p(author_line, "small")]
        if paper.get("affiliation"):
            entry.append(p(text(paper["affiliation"]), "small"))
        entry.append(p(text(paper["summary"])))
        if paper.get("links"):
            entry.append(p("  ·  ".join('<a color="' + ACCENT + '" href="' + text(link["url"]) + '">' + text(link["label"]) + "</a>" for link in paper["links"]), "small"))
        entry += [Spacer(1, 8), HRFlowable(width="100%", thickness=.35, color=colors.HexColor("#d5d8cf")), Spacer(1, 11)]
        story.append(KeepTogether(entry))
    if group == "workshop":
        story.append(p('Ongoing research is listed separately on <a color="' + ACCENT + '" href="' + text(CV["basics"]["website"]) + '/projects/">the website</a>; submission and review details are not disclosed.', "small"))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=56, leftMargin=56, topMargin=45, bottomMargin=58, title="Vaibhav Rathore - Curriculum Vitae", author="Vaibhav Rathore", pageCompression=1)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
