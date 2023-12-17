from io import BytesIO
from django.db import models
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse
from reportlab.lib import colors


class Report(models.Model):
    type = models.CharField(max_length=256, default='', null=True, blank=True),
    title = models.CharField(max_length=256, default="Relatório %d/%m/%Y")
    date_creation = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
    
    def getReportFields(self):
        return Report_field.objects.filter(report=self)
    
    def generatePDF(self):
        response = FileResponse(self.createPDF(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio.pdf"'
        return response
    
    
    def createPDF(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        try:
            elements = []

            # Adicione o título do relatório
            title = self.title if self.title else "Relatório Sem Título"
            elements.append(Paragraph(title, styles['Title']))
            elements.append(Spacer(1, 20))

            # Inicializando a primeira tabela
            data = []

            for report_field in self.getReportFields():
                if report_field.field and not report_field.content:
                    # Adicionando a tabela anterior (se houver dados)
                    if data:
                        self.add_table_to_elements(data, elements, doc.width)
                        data = []  # Resetando os dados para a próxima tabela

                    # Tratando como um título de seção
                    elements.append(Paragraph(report_field.field, styles['Heading2']))
                    elements.append(Spacer(1, 12))

                else:
                    # Adicionando à tabela
                    row = [report_field.field or "", report_field.content or ""]
                    data.append(row)

            # Adicionando a última tabela (se houver dados)
            if data:
                self.add_table_to_elements(data, elements, doc.width)

            # Cria o PDF
            doc.build(elements)
            buffer.seek(0)
            return buffer

        except Exception as e:
            print(f"Ocorreu um erro ao criar o PDF: {e}")
            return None

    def add_table_to_elements(self, data, elements, page_width):
        # Função auxiliar para adicionar uma tabela aos elementos
        table = Table(data, colWidths=[page_width/2.0]*2)  # Largura dividida igualmente
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

    

class Report_field(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    field = models.TextField(default=None, blank=True, null=True)
    content = models.TextField(default=None, blank=True, null=True)
    
    def __str__(self):
        return f"Campo: {self.field}, Conteúdo: {self.content}"
