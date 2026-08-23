from pypdf import PdfWriter
import io
from logic.extract_text import extract_text

# Create a PDF with actual text content using pypdf annotations/canvas or reportlab
from pypdf.generic import NameObject, create_string_object, DictionaryObject, ArrayObject, DecodedStreamObject

writer = PdfWriter()
page = writer.add_blank_page(width=300, height=300)
# Add a content stream with text
stream = DecodedStreamObject()
stream.set_data(b"BT /F1 12 Tf 50 250 Td (Indian Passport Seva Verification Notice) Tj ET")
page[NameObject("/Contents")] = stream

# Add font resource
fonts = DictionaryObject()
font1 = DictionaryObject()
font1[NameObject("/Type")] = NameObject("/Font")
font1[NameObject("/Subtype")] = NameObject("/Type1")
font1[NameObject("/BaseFont")] = NameObject("/Helvetica")
fonts[NameObject("/F1")] = font1

res = DictionaryObject()
res[NameObject("/Font")] = fonts
page[NameObject("/Resources")] = res

pdf_io = io.BytesIO()
writer.write(pdf_io)
pdf_io.seek(0)

extracted = extract_text(pdf_io, filename="passport_notice.pdf")
print("Extracted PDF text:\n", extracted)
assert "Indian Passport Seva" in extracted
print("PDF extraction verified successfully!")
