from PyPDF2 import PdfReader
import json

pdf1_path = r'c:\Users\pipsou\Desktop\projets_perso\sncf\sncf data analysis\litterature\21.03.17_communique_aqst-causes_ter.pdf'
pdf2_path = r'c:\Users\pipsou\Desktop\projets_perso\sncf\sncf data analysis\litterature\bilan_ferroviaire_2023_essentiel-1.pdf'

output = []

# Extract from first PDF
output.append("=" * 80)
output.append("PDF 1: Causes de retard TER - 21.03.17_communique_aqst-causes_ter.pdf")
output.append("=" * 80)

try:
    reader1 = PdfReader(pdf1_path)
    output.append(f"Total pages: {len(reader1.pages)}\n")
    for page_num, page in enumerate(reader1.pages):
        text = page.extract_text()
        output.append(f"--- Page {page_num + 1} ---")
        output.append(text)
        output.append("")
except Exception as e:
    output.append(f"Error reading first PDF: {e}")

# Extract from second PDF
output.append("\n" + "=" * 80)
output.append("PDF 2: Bilan ferroviaire 2023 - bilan_ferroviaire_2023_essentiel-1.pdf")
output.append("=" * 80)

try:
    reader2 = PdfReader(pdf2_path)
    output.append(f"Total pages: {len(reader2.pages)}\n")
    for page_num, page in enumerate(reader2.pages):
        text = page.extract_text()
        output.append(f"--- Page {page_num + 1} ---")
        output.append(text)
        output.append("")
except Exception as e:
    output.append(f"Error reading second PDF: {e}")

# Write to file
with open(r'c:\Users\pipsou\Desktop\projets_perso\sncf\sncf data analysis\pdf_extraction_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("PDF extraction complete. Results saved to pdf_extraction_output.txt")
