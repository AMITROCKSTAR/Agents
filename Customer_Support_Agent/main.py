# Run the Agent
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from graph_builder import build_agent_graph
import uvicorn
import PyPDF2
from Img_Pdf_Text_extract import extract_text_from_pdf_ocr
from Vector_Store.Ingest_docs import vector_db
import os
import logging


app = build_agent_graph()


# --- Setup global logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


api = FastAPI(title="Customer Support Agent API")

## Inserting data in vector db

@api.post("/upload_file/")
async def upload_pdf(file:UploadFile = File(...)):
    # with open("pdf_docs/all_queries.pdf", "rb") as f:
    try:
        
        file_path = f"./pdf_docs{file.filename}"
        os.makedirs("./pdf_docs",exist_ok=True)
        
        with open(file_path, "wb") as t:
             t.write(await file.read())
        with open(file_path, "rb") as f:
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
                texts = extract_text_from_pdf_ocr(file_path)

            
        logging.info(f"✅ PDF '{file.filename}' inserted successfully.")
        return vector_db(texts)
    
    except Exception as e:
        print(f"Error :{e}")


@api.post("/query/")
async def user_query(query: str = Form(...)):
    try:
        logging.info(f"🔍 Received query: {query}")
        final_state = app.invoke(
            {"messages":[HumanMessage(content=query)],"query":query,"result":""},
            config={"configurable":{"thread_id":"cust-123"}}
        )
        logging.info(f"💬 Response generated successfully.")
        return JSONResponse({
            "query": query,
            "response": final_state["result"]
        })
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

# if __name__ == "__main__":
    # uvicorn.run("main:api", host="127.0.0.1", port=8080, reload=True)