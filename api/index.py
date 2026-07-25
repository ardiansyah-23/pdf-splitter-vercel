from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import PyPDF2
import io

app = FastAPI()

# Bagian Frontend (Tampilan Web Pengganti Streamlit)
@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF Splitter App</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 40px; max-width: 600px; margin: auto; }
            .container { border: 1px solid #ccc; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
            button { margin-top: 15px; padding: 10px 15px; background-color: #000; color: #fff; border: none; cursor: pointer; border-radius: 5px; }
            button:hover { background-color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Pemotong PDF (Vercel Edition)</h2>
            <p>Upload file PDF Anda di bawah ini.</p>
            <form action="/split" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="application/pdf" required>
                <br>
                <button type="submit">Proses PDF</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Bagian Backend (Logika Pemotong PDF)
@app.post("/split")
async def split_pdf(file: UploadFile = File(...)):
    try:
        # Membaca file PDF yang di-upload
        pdf_reader = PyPDF2.PdfReader(file.file)
        total_pages = len(pdf_reader.pages)
        
        # Contoh logika pemotongan: Mengambil Halaman 1 Saja
        pdf_writer = PyPDF2.PdfWriter()
        if total_pages > 0:
            pdf_writer.add_page(pdf_reader.pages[0])
            
        output = io.BytesIO()
        pdf_writer.write(output)
        
        return {
            "status": "Sukses", 
            "pesan": f"PDF berhasil diproses. Total halaman asli: {total_pages}",
            "nama_file": file.filename
        }
    except Exception as e:
        return {"status": "Gagal", "pesan": str(e)}
