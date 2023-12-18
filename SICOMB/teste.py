import requests
import serial
import time

# Inicializa o dicionário para armazenar os códigos e seus tempos
codigo_armazenado = {}

def enviar_linha_para_url(linha, url):
    
    parametros = {"uid": linha}
    response = requests.get(url, params=parametros)
    
    if response.status_code == 200:
        print(f"Enviado com sucesso: {linha}")
    else:
        print(f"Falha ao enviar: {linha}")

com13 = serial.Serial('COM13', 115200)

try:
    while True:
        linha = com13.readline().decode('utf-8').strip()

        print("printando linha")
        print(linha)
        
        linha = linha.split("::")
        if linha[0] == "TAG_CODE":
            url = "http://localhost:8000/equipamento/set"
            
            code = linha[1]
            # Verifica se o código já foi armazenado
            if code not in codigo_armazenado:
                codigo_armazenado[code] = time.time()  # Armazena o código com o tempo atual
                enviar_linha_para_url(code, url)
        elif linha[0] == "FINGERPRINT":
            url = "http://localhost:8000/police/set_fingerprint"
            
            
                
        # Remove códigos que estão na lista há mais de 5 segundos
        tempo_atual = time.time()
        codigos_a_remover = [codigo for codigo, tempo_adicao in codigo_armazenado.items() if tempo_atual - tempo_adicao >= 5]
        for codigo in codigos_a_remover:
            del codigo_armazenado[codigo]
except KeyboardInterrupt:
    com13.close()
