# Sistema IoT de Automação de Climatização com ESP32

Este projeto consiste em um sistema de automação residencial para controle inteligente de climatização, utilizando dois módulos ESP32 que se comunicam via rede Wi-Fi.

## Arquitetura do Sistema

O sistema é dividido em duas funções principais:

1. **ESP32 Controlador (Monitoramento):**
   - Realiza a leitura de temperatura e umidade através do sensor DHT22.
   - Gerencia o limite de temperatura definido manualmente via potenciômetro.
   - Exibe as informações em tempo real no display OLED (SSD1306).
   - Envia os dados coletados para uma planilha do Google Sheets via API.
   - Envia alertas via WhatsApp (CallMeBot) quando a temperatura ultrapassa o limite.
   - Envia comandos HTTP para o segundo ESP32 para controlar o estado do ar-condicionado.

2. **ESP32 Atuador (Simulador de Ar-Condicionado):**
   - Atua como um servidor HTTP local.
   - Simula o próprio ar-condicionado: recebe os comandos "ligar" ou "desligar" enviados pelo controlador e altera o estado físico de um pino (GPIO 4), simulando a operação do equipamento.

## Estrutura dos Arquivos

- `esp32_controlador_ambiente.py`: Lógica principal de monitoramento e controle.
- `esp32_atuador_ac.py`: Código que simula o funcionamento do ar-condicionado.
- `ssd1306.py`: Biblioteca de driver para o display OLED.

## Requisitos
- MicroPython instalado nos módulos ESP32.
- Rede Wi-Fi configurada.
- Google Sheets (Google Apps Script) para o registro de dados.
