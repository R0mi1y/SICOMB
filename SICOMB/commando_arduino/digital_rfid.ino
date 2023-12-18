#include <Adafruit_Fingerprint.h>
#include "RFIDLabel.hpp"  // Inclui o código do arquivo RFIDLabel.hpp

unsigned char ReadSingle[7] = {0XAA, 0X00, 0X22, 0X00, 0X00, 0X22, 0XDD};
unsigned char ReadMulti[10] = {0XAA,0X00,0X27,0X00,0X03,0X22,0XFF,0XFF,0X4A,0XDD};

unsigned char epccode[12] = "SUPERAltec12";
unsigned char readepc[12];
unsigned char lastValidReadData[64];
unsigned char readData[64];
bool isReading = false;
bool isValidRead = false; 
bool hasValidRead = false; 
unsigned int validReadLength = 0;
unsigned int currentReadlength = 0;

unsigned long int counter = 0;

RFIDLabel* label;

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial2);

int num = 0;
int parm = -1;

void processCommand(const String& input) {
  num = 0;
  parm = -1;

  int spaceIndex = input.indexOf(' ');

  if (spaceIndex != -1) {
    num = input.substring(0, spaceIndex).toInt();
    parm = input.substring(spaceIndex + 1).toInt();
  } else {
    num = input.toInt();
  }
}

void setup()
{
  Serial.begin(115200);
  Serial1.begin(115200);

  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
  } else {
    while (1) { delay(1); }
  }

  finger.getParameters();
  finger.getTemplateCount();

  label = new RFIDLabel();															//Data that should be sent to RFIDLabel
	Serial.println("Started");
}

void loop()
{
  parm = -1;

  String inputString = "";
  String commandString = "";
  String firstParam = "";

  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n'); // Lê até encontrar uma quebra de linha

    processCommand(inputString);
  }

  if (num == 0){
    handleInput();

    if(hasValidRead) {
      for(int i = 0; i < 64; i++) {
        if(lastValidReadData[i + 1] == 0XDD || lastValidReadData[i] == 0XDD) {  // Se os últimos dados lidos forem 0XDD
          break;  // Interrompe o loop
        }
        if(counter % 300 == 0) {
          Serial.print("TAG_CODE::");
          for(int i = 0; i < 64; i++) {  // Loop até 64 vezes
            if(lastValidReadData[i + 1] == 0XDD || lastValidReadData[i] == 0XDD) {  // Se os últimos dados lidos forem 0XDD
              break;  // Interrompe o loop
            }
            if(i >=6 ) {
              Serial.print(lastValidReadData[i], HEX);
            }  // Imprime lastValidReadData no monitor serial como hexadecimal
          }
          Serial.println();
          counter++;
        }
      }

    }

    if(counter % 3000 == 0) {  // Pausa não bloqueante dos comandos ReadSingle
      // Serial1.write(ReadSingle, 7);  // Envia o comando ReadSingle para o módulo RFID R200
      Serial1.write(ReadMulti, 10);  // Envia o comando ReadSingle para o módulo RFID R200
    }
    counter++;

  } else if (num == 1) {
    int findId = 1;
    Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo");


    while (findId != 0) {
      findId = getFingerprintID();
      delay(50);
    }

    num = 0;
  } else if (num == 2) {
    if (parm >= 0)
      while (!getFingerprintEnroll(parm));
    num = 0;
  }
}

void handleInput() {  // Inicia o loop de manipulação de entrada

	while(Serial1.available()) {  // Verifica se há entrada serial disponível
		unsigned char rc = Serial1.read();  // Lê os dados de entrada e os armazena em 'rc'

		if(rc == 0XAA) { // Iniciar leitura // Verifica se os dados de entrada marcam o início de uma leitura pelo cabeçalho (AA)
			isReading = true;  // Define o estado de leitura como verdadeiro
			currentReadlength = 0;  // Comprimento atual do sinal RFID de entrada salvo

			for(int i = 0; i < 64; i++) {  // Loop 64 vezes para 'readData'
				readData[i] = 0X00;  // Preenche 'readData' com 0X00 para limpar todas as posições antes de salvar novos dados (apenas para fins visuais e de inspeção)
			}
		}

		if(isReading) {  // Verifica se 'isReading' é verdadeiro
			readData[currentReadlength] = rc;  // Coloca os dados de entrada de 'readData' na posição correta (determinada por 'currentReadLength') em 'rc'
			
			if(currentReadlength == 1 && rc == 0X02) { // Tipo de resposta válido // Verifica se o primeiro caractere após o cabeçalho (AA) é 0X02. Isso garante que os dados de entrada sejam uma resposta
				validReadLength = 0;  // Altera a posição em que os primeiros dados de entrada devem ser colocados
				isValidRead = true;  // Os dados de leitura de entrada são válidos
				for(int i = 0; i < 64; i++) {  // Loop 64 vezes para 'lastValidReadData'
					lastValidReadData[i] = 0X00;  // Limpa todos os caracteres
				}
				lastValidReadData[0] = 0XAA;  // Escreve o cabeçalho em 'lastValidReadData' como 0XAA
			}

			if(isValidRead) {  // Se os dados de entrada forem válidos
				lastValidReadData[currentReadlength] = rc;  // Pega os dados de 'lastValidReadData' e os coloca em 'rc' na posição determinada por 'currentReadLength'
				validReadLength++;  // Salva o comprimento da string salva

				if(currentReadlength > 7 && currentReadlength < 20) {  // Extrair o código EPC da sequência completa de dados de entrada após a leitura
					readepc[currentReadlength - 8] = rc;  // Remove os primeiros 8 caracteres dos dados de entrada e os salva em 'readepc'
				}
			}
		}

		if(rc == 0XDD) {  // Verifica se o valor de leitura é 0XDD (IMPORTANTE, se o valor de leitura tiver 0XDD em algum lugar antes do esperado como um rodapé, o código ainda acha que é um rodapé)
			if(isValidRead) {  // Verdadeiro quando os dados de entrada começam com 0XAA, 0X02, indicando que é o cabeçalho e é uma resposta
				hasValidRead = true;  // Salva o estado de uma leitura válida de entrada
			}

			isValidRead = false;  // Como os dados de leitura são 0XDD, eles agem como rodapé da string. Portanto, os dados de entrada possíveis não devem ser considerados como dados válidos
			isReading = false;  // Como os dados de leitura são 0XDD, eles agem como rodapé da string. Portanto, os dados de entrada não devem ser considerados como dados que devem ser lidos
		}

		currentReadlength++;  // Altera a posição em que os dados de leitura devem ser colocados
	}
}

// FUNCAO PARA LER A DIGITAL E RETORNAR O ID COM NIVEL CONFIANCA //
uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      // Serial.println("Image too messy");
      Serial.println("FINGERPRINT::ERROR::Não foi encontrado nenhuma digital que pareie!");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      // Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      // Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
    default:
      Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    // Serial.println("Found a print match!");
    Serial.print("FINGERPRINT::"); 
    Serial.print(finger.fingerID);
    Serial.print("::"); 
    // Serial.print("NIVEL DE CONFIANCA: "); 
    Serial.println(finger.confidence);
    return p;
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("FINGERPRINT::ERROR::Não foi encontrado nenhuma digital que pareie!");
    return 0;
  } else {
    Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
    return p;
  }
}

// FUNCAO PARA CADASTRAR UMA NOVA DIGITAL //
uint8_t getFingerprintEnroll(int value)
{

  int p = -1;
  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo");
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(1);
  switch (p)
  {
  case FINGERPRINT_OK:
    // Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }

  Serial.println("FINGERPRINT::USERMESSAGE::Remova o dedo!");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER)
  {
    p = finger.getImage();
  }
  // Serial.print("ID ");
  // Serial.println(value);
  p = -1;
  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo novamente");
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      // Serial.print(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p)
  {
  case FINGERPRINT_OK:
    // Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }

  // OK converted!
  // Serial.print("Creating model for #");
  // Serial.println(value);

  p = finger.createModel();
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Prints matched!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_ENROLLMISMATCH)
  {
    Serial.println("FINGERPRINT::ERROR::Dedo incorreto! Você deve colocar o mesmo dedo!");
    return p;
  }
  else
  {
    Serial.println("Unknown error");
    return p;
  }

  Serial.print("ID ");
  Serial.println(value);
  p = finger.storeModel(value);
  if (p == FINGERPRINT_OK)
  {
    Serial.println("FINGERPRINT::SUCCESS");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
    return p;
  }
  else if (p == FINGERPRINT_BADLOCATION)
  {
    Serial.println("Could not store in that location");
    // Serial.println("FINGERPRINT::ERROR::Erro!");
    return p;
  }
  else if (p == FINGERPRINT_FLASHERR)
  {
    Serial.println("Error writing to flash");
    // Serial.println("FINGERPRINT::ERROR::Erro!");
    return p;
  }
  else
  {
    Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
    return p;
  }

  return true;
}