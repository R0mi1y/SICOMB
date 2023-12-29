import pdfkit

def criar_pdf_html(html_file, pdf_file):
    options = {
        'page-size': 'A4',
        'encoding': 'utf-8',  # Use a codificação UTF-8 para suportar acentos
    }
    
    pdfkit.from_file(html_file, pdf_file, options=options)

if __name__ == "__main__":
    html_file = "./exemplo.html"
    pdf_file = "exemplo.pdf"
    
    criar_pdf_html(html_file, pdf_file)
    
    print(f"PDF '{pdf_file}' criado com sucesso a partir do HTML.")
