import os
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(load):
    load_date = load.date_load
    # Obter a data atual no formato de ano, mês e dia
    year = load_date.strftime('%Y')
    month = load_date.strftime('%m')
    day = load_date.strftime('%d')

    # Crie o caminho da pasta com base na data
    folder_path = f"media/cargas/{load.turn_type}/{year}/{month}/{day}" if load.turn_type != "descarga" else f"media/descargas/{year}/{month}/{day}"
    file_name = f"Carga_{load.id}.pdf"

    # Verifique se a pasta já existe, e se não, crie-a
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Crie o caminho do arquivo com base na pasta, número de carga e extensão do arquivo
    pdf_file = os.path.join(folder_path, file_name)

    # Verifique se o arquivo já existe e, se existir, remova-o
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

    # Crie um arquivo PDF vazio
    document = platypus.SimpleDocTemplate(pdf_file, pagesize=letter)

    # Lista para armazenar elementos do PDF
    elements = []

    # Estilos de texto
    styles = getSampleStyleSheet()

    # Título do PDF
    title = platypus.Paragraph("Relatório de Carga", styles['Title'])
    elements.append(title)

    # Informações sobre a carga
    load_info = [
        ["Data de Carga:", load.date_load.strftime('%d/%m/%Y %H:%M')],
        ["Data Prevista de Devolução:", load.expected_load_return_date.strftime('%d/%m/%Y %H:%M') if load.expected_load_return_date else 'N/A'],
        ["Data de Descarregamento:", load.returned_load_date.strftime('%d/%m/%Y %H:%M') if load.returned_load_date else 'N/A'],
        ["Tipo de Turno:", load.turn_type],
        ["Status:", load.status],
        ["Policial:", load.police.name],
        ["Adjunto:", load.adjunct.name],
    ]
    
    # Tabela para informações da carga
    load_table = platypus.Table(load_info, colWidths=[150, 200])
    load_table.setStyle(platypus.TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('GRID', (0, 0), (-1, -1), 1, (0.2, 0.2, 0.2)),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
                                    ('BACKGROUND', (0, 1), (-1, 1), (0.8, 0.8, 0.8))]))

    elements.append(load_table)

    elements.append(platypus.Spacer(3, 20))
    
    # Informações sobre os equipamentos da carga
    equipment_info = [
        ["Equipamento", "Quantidade", "Observação", "Status"],
    ]

    for equipment_load in load.equipment_loads.all():
        equipment_info.append([
            equipment_load.equipment.model.model if equipment_load.equipment else equipment_load.bullet,
            str(equipment_load.amount),
            equipment_load.observation if equipment_load.observation else 'N/A',
            equipment_load.status,
        ])

    # Tabela para informações dos equipamentos
    equipment_table = platypus.Table(equipment_info, colWidths=[100, 100, 80, 180, 80])
    equipment_table.setStyle(platypus.TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                         ('GRID', (0, 0), (-1, -1), 1, (0.2, 0.2, 0.2)),
                                         ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
                                         ('BACKGROUND', (0, 1), (-1, 1), (0.8, 0.8, 0.8))]))

    elements.append(equipment_table)

    # Construa o PDF
    document.build(elements)

    print(f"O PDF foi gerado com sucesso em {pdf_file}")
    return folder_path, file_name


def send_relatory(load):
    pdf_path, pdf_file = generate_pdf(load)
    
    subject = 'Relatório de carga'
    message = f'Relatório da carga feita no dia {load.date_load}' if load.turn_type != "descarga" else f'Relatório da descarga feita no dia {load.date_load}'
    from_email = load.adjunct.email
    
    recipient_list = [load.police.email]
    
    email = EmailMessage(
        subject=subject,
        body=message,
        bcc=recipient_list,
    )
    
    email.attach_file(pdf_path + "\\" + pdf_file)
    
    os.remove(pdf_path + "\\" + pdf_file)
    
    email.send()