import fitz  # PyMuPDF
import os
from PIL import Image

def extract_pdf_pages(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(f"Processando {pdf_path}...")
    
    for i in range(len(doc)):
        page = doc.load_page(i)
        # Aumentar a resolução (zoom) para alta resolução
        zoom = 3.0  
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Converter pixmap para imagem PIL
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        output_filename = f"{base_name}-page-{i+1}.webp"
        output_path = os.path.join(output_folder, output_filename)
        
        # Salvar como WebP com otimização e qualidade (80 é um bom equilíbrio)
        img.save(output_path, "WEBP", quality=80, optimize=True)
        print(f"  Salvo: {output_filename}")
    
    doc.close()

if __name__ == "__main__":
    img_dir = "snippet-mycris/img"
    pdfs = [f for f in os.listdir(img_dir) if f.endswith(".pdf")]
    
    output_dir = os.path.join(img_dir, "extracted")
    
    for pdf in pdfs:
        full_path = os.path.join(img_dir, pdf)
        extract_pdf_pages(full_path, output_dir)

    print("\nExtração concluída!")
