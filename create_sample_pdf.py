
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


# Kaynak TXT dosyasını oku
with open("sample_document.txt", "r", encoding="utf-8") as file:
    content = file.read()


# PDF dosyasını oluştur
pdf = SimpleDocTemplate(
    "sample_document.pdf",
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm
)


# PDF metin stilleri
styles = getSampleStyleSheet()

story = []

# Metni satırlara ayır
for line in content.split("\n"):

    line = line.strip()

    if not line:
        story.append(Spacer(1, 8))
        continue

    # Başlıkları ayırt et
    if line.startswith("# "):
        paragraph = Paragraph(line[2:], styles["Title"])

    elif line.startswith("## "):
        paragraph = Paragraph(line[3:], styles["Heading2"])

    elif line.startswith("- "):
        paragraph = Paragraph("• " + line[2:], styles["BodyText"])

    else:
        paragraph = Paragraph(line, styles["BodyText"])

    story.append(paragraph)
    story.append(Spacer(1, 6))


# PDF oluştur
pdf.build(story)

print("PDF successfully created!")
print("File: sample_document.pdf")
