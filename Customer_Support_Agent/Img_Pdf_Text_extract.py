
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_pdf_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    texts = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        if text.strip():
            text = text.strip().replace("\n"," ")
            ## Chunking size 500 with 50 overlap
            for i in range(0,len(text),450):
                chunks = text[i:i+500]
                texts.append(chunks)
            # texts.extend([line.strip() for line in text.split("\n") if line.strip()])
    print(f"OCR Extracted {len(texts)} lines of text.")
    return texts

