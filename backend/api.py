from fastapi import FastAPI, File, UploadFile

import PyPDF2

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...)):

    # Open the uploaded PDF file in read-binary mode
    with open(file.filename, 'wb') as pdf_file:
        contents = await file.read()
        pdf_file.write(contents)

    # Create a PDF reader object
    with open(file.filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create a text file for writing
        with open('output.txt', 'w') as txt_file:

            # Loop through all the pages in the PDF file
            for page_num in range(pdf_reader.getNumPages()):

                # Extract the text from the page
                page = pdf_reader.getPage(page_num)
                text = page.extractText()

                # Write the text to the text file
                txt_file.write(text)

    # Return the path to the text file
    return {"text_file_path": "output.txt"}
