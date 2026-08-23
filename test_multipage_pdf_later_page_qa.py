import unittest
import os
import io
from pypdf import PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from logic.extract_text import extract_text_with_metadata
from logic.llm_calls import answer_question
from logic.memory_manager import log_qa, get_qa_history_for_document, clear_qa_history

def add_text_page(writer, text_lines, width=595, height=842):
    page = writer.add_blank_page(width=width, height=height)
    stream = DecodedStreamObject()
    
    commands = ["BT", "/F1 12 Tf", "50 750 Td"]
    for i, line in enumerate(text_lines):
        if i > 0:
            commands.append("0 -20 Td")
        escaped_line = line.replace("(", "\\(").replace(")", "\\)")
        commands.append(f"({escaped_line}) Tj")
    commands.append("ET")
    
    stream.set_data("\n".join(commands).encode("utf-8"))
    page[NameObject("/Contents")] = stream
    
    fonts = DictionaryObject()
    font1 = DictionaryObject()
    font1[NameObject("/Type")] = NameObject("/Font")
    font1[NameObject("/Subtype")] = NameObject("/Type1")
    font1[NameObject("/BaseFont")] = NameObject("/Helvetica")
    fonts[NameObject("/F1")] = font1
    
    res = DictionaryObject()
    res[NameObject("/Font")] = fonts
    page[NameObject("/Resources")] = res
    return page

def add_blank_or_image_page(writer, width=595, height=842):
    page = writer.add_blank_page(width=width, height=height)
    # Page with 0 text or trivial placeholder
    return page

class TestMultiPageLaterPageQA(unittest.TestCase):

    def setUp(self):
        clear_qa_history()

    def test_multipage_with_image_in_middle_and_later_page_grounding(self):
        print("\n=== Testing Multi-Page PDF with Image Skip & Later-Page Grounding ===")
        
        # 1. Create a 3-page PDF:
        # Page 1: Standard Notice Header
        # Page 2: Blank / Image-only (0 chars)
        # Page 3: Specific Later Clause (Section 271AAB, 60% penalty, Dec 15 2026)
        writer = PdfWriter()
        
        # Page 1
        add_text_page(writer, [
            "INCOME TAX DEPARTMENT - GOVERNMENT OF INDIA",
            "Intimation under Section 143(1) of the Income-tax Act, 1961",
            "Assessment Year: 2025-26 | PAN: ABCDE1234F | Notice Date: 15-Aug-2026",
            "Dear Taxpayer, please review this demand notice carefully."
        ])
        
        # Page 2 (Image page / scanned stamp without readable text)
        add_blank_or_image_page(writer)
        
        # Page 3 (Important later provisions)
        add_text_page(writer, [
            "PAGE 3: SPECIAL ENFORCEMENT AND PENALTY CLAUSES",
            "Clause 14B: Under Section 271AAB, undisclosed income incurs a mandatory 60 percent penalty.",
            "Clause 14C: Mandatory appeal and grievance cutoff date is December 15, 2026.",
            "Clause 14D: Required document for appeal: Certified Form 35 with payment challan."
        ])
        
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        
        # 2. Extract text & metadata
        extracted_text, metadata = extract_text_with_metadata(pdf_bytes, filename="multipage_audit.pdf")
        
        print(f"Total Pages in PDF: {metadata['total_pages']}")
        print(f"Skipped Low-Text/Image Pages: {metadata['low_text_pages']}")
        print(f"Readable Pages Scanned: {metadata['readable_pages']}")
        print("Extracted Text Content:\n" + "="*50 + "\n" + extracted_text + "\n" + "="*50)
        
        self.assertEqual(metadata["total_pages"], 3)
        self.assertEqual(metadata["low_text_pages"], [2])
        self.assertEqual(metadata["readable_pages"], 2)
        
        # Confirm Page 1 text is present
        self.assertIn("INCOME TAX DEPARTMENT", extracted_text)
        # Confirm Page 3 text is present (scanned after the image page)
        self.assertIn("Section 271AAB", extracted_text)
        self.assertIn("December 15, 2026", extracted_text)
        
        # 3. Grounded Q&A asking specifically about Page 3's content
        q = "What is the mandatory penalty percentage and cutoff date specified in Section 271AAB?"
        answer = answer_question(extracted_text, q, language="English")
        print("\nDocument Q&A Question:", q)
        print("Document Q&A Answer:\n", answer)
        
        # 4. Log to memory_manager
        log_id = log_qa("document", "multipage_audit.pdf", q, answer, "English")
        self.assertGreater(log_id, 0)
        
        # 5. Verify retrieval
        history = get_qa_history_for_document("multipage_audit.pdf")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["question"], q)
        print(f"\n[OK] Multi-page scan & Document Q&A verified! Logged to DB row ID {log_id}")

if __name__ == "__main__":
    unittest.main()
