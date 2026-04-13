#!/usr/bin/env python
import sys
import os

# Try to extract PDF text
try:
    from PyPDF2 import PdfReader
    print("PyPDF2 available, extracting...")
    
    pdf1_path = r'c:\Users\pipsou\Desktop\projets_perso\sncf\sncf data analysis\litterature\21.03.17_communique_aqst-causes_ter.pdf'
    pdf2_path = r'c:\Users\pipsou\Desktop\projets_perso\sncf\sncf data analysis\litterature\bilan_ferroviaire_2023_essentiel-1.pdf'
    
    # Extract from first PDF
    print("\n" + "="*60)
    print("PDF 1: Causes de retard (Delay causes)")
    print("="*60)
    try:
        reader1 = PdfReader(pdf1_path)
        print(f"Total pages: {len(reader1.pages)}")
        for page_num, page in enumerate(reader1.pages):
            text = page.extract_text()
            print(f"\n--- Page {page_num + 1} ---")
            print(text)
    except Exception as e:
        print(f"Error reading first PDF: {e}")
    
    # Extract from second PDF
    print("\n" + "="*60)
    print("PDF 2: Bilan ferroviaire 2023")
    print("="*60)
    try:
        reader2 = PdfReader(pdf2_path)
        print(f"Total pages: {len(reader2.pages)}")
        for page_num, page in enumerate(reader2.pages):
            text = page.extract_text()
            print(f"\n--- Page {page_num + 1} ---")
            print(text)
    except Exception as e:
        print(f"Error reading second PDF: {e}")
        
except ImportError:
    print("PyPDF2 not available, trying alternative...")
    sys.exit(1)
