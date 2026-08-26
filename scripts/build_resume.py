import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Table, TableStyle

TEAL = HexColor('#1F8A8A')
NAVY = HexColor('#20354F')
GRAY = HexColor('#555555')

src = Path(sys.argv[1] if len(sys.argv) > 1 else 'resume.json')
out = Path(
    sys.argv[2]
    if len(sys.argv) > 2
    else 'Constantine_Yachnytskyi_Go_Rust_Backend_Distributed_Systems_Engineer.pdf'
)
data = json.loads(src.read_text(encoding='utf-8'))

margin = 14 * mm
doc = SimpleDocTemplate(
    str(out),
    pagesize=A4,
    leftMargin=margin,
    rightMargin=margin,
    topMargin=12 * mm,
    bottomMargin=10 * mm,
)

styles = {
    'name': ParagraphStyle(
        'name', fontName='Helvetica-Bold', fontSize=17.5, leading=20,
        textColor=NAVY, alignment=1, spaceAfter=3,
    ),
    'title': ParagraphStyle(
        'title', fontName='Helvetica-Bold', fontSize=10.5, leading=12,
        textColor=TEAL, alignment=1, spaceAfter=6,
    ),
    'contact': ParagraphStyle(
        'contact', fontName='Helvetica', fontSize=7.6, leading=9,
        textColor=GRAY, alignment=1, spaceAfter=10,
    ),
    'section': ParagraphStyle(
        'section', fontName='Helvetica-Bold', fontSize=9.5, leading=10,
        textColor=NAVY, spaceBefore=3, spaceAfter=1,
    ),
    'body': ParagraphStyle(
        'body', fontName='Helvetica', fontSize=7.7, leading=9.1,
        textColor=black, spaceAfter=2,
    ),
    'label': ParagraphStyle(
        'label', fontName='Helvetica-Bold', fontSize=7.6, leading=8.8,
        textColor=NAVY,
    ),
    'exp': ParagraphStyle(
        'exp', fontName='Helvetica-Bold', fontSize=8.0, leading=9.2,
        textColor=NAVY,
    ),
    'dates': ParagraphStyle(
        'dates', fontName='Helvetica-Bold', fontSize=7.5, leading=9,
        textColor=GRAY, alignment=2,
    ),
    'bullet': ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=7.45, leading=8.7,
        leftIndent=4 * mm, firstLineIndent=-2.5 * mm, bulletIndent=1 * mm,
        spaceAfter=1,
    ),
}

story = [
    Paragraph(data['name'], styles['name']),
    Paragraph(data['title'], styles['title']),
]

contact = [
    data['location'],
    f"<link href='tel:{data['phone'].replace(' ', '')}' color='#555555'>{data['phone']}</link>",
    f"<link href='mailto:{data['email']}' color='#555555'>{data['email']}</link>",
]
for label, url in data['links'].items():
    contact.append(f"<link href='{url}' color='#555555'>{label}</link>")
story.append(Paragraph(' &nbsp;|&nbsp; '.join(contact), styles['contact']))


def section(title: str) -> None:
    story.append(Paragraph(title, styles['section']))
    story.append(
        HRFlowable(
            width='100%', thickness=0.7, color=NAVY,
            spaceBefore=0, spaceAfter=2,
        )
    )


section('PROFESSIONAL SUMMARY')
story.append(Paragraph(data['summary'], styles['body']))

section('TECHNICAL SKILLS')
rows = [
    [Paragraph(label, styles['label']), Paragraph(value, styles['body'])]
    for label, value in data['skills']
]
skills = Table(rows, colWidths=[41 * mm, 126 * mm], hAlign='LEFT')
skills.setStyle(
    TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.4),
    ])
)
story.append(skills)

section('PROFESSIONAL EXPERIENCE')
for item in data['experience']:
    role = item['role'] + (f" | {item['company']}" if item['company'] else '')
    heading = Table(
        [[Paragraph(role, styles['exp']), Paragraph(item['dates'], styles['dates'])]],
        colWidths=[130 * mm, 37 * mm],
    )
    heading.setStyle(
        TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ])
    )
    story.append(heading)
    for bullet in item['bullets']:
        story.append(Paragraph('• ' + bullet, styles['bullet']))

section('LANGUAGES')
story.append(Paragraph(data['languages'], styles['body']))

doc.build(story)
print(out)
