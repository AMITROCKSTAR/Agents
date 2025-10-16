from Ingest_docs import vector_db
import PyPDF2 
from Img_Pdf_Text_extract import extract_text_from_pdf_ocr


def Insert_new_data(path,metadatas=None):
    # with open("pdf_docs/all_queries.pdf", "rb") as f:
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        texts = []
        total_pages = len(reader.pages)

        text_pages = sum([1 for p in reader.pages if p.extract_text() and p.extract_text().strip()])

        ## Writing condtition to check if pdf is image or text based

        if text_pages == total_pages:
            for page in reader.pages:
                text = page.extract_text()
                text= text.strip().replace("\n"," ")
                ## Doing Chunking with 500 chunk size and 50 overlap 
                for i in range(0,len(text),450):
                    chunks = text[i:i+500]
                    texts.append(chunks)
             
                # print("text-------",text)
                # if text:
                #     # Split by line if PDF has multiple queries per page
                #     texts.extend([line.strip() for line in text.split("\n") if line.strip()])
        
        else:
            texts = extract_text_from_pdf_ocr(path)

            
    
    return vector_db(texts)

print(Insert_new_data("pdf_docs/Groq_Policy.pdf"))