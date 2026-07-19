# --- Importação de Bibliotecas Necessárias --- 
import network 
import time 
import urequests 
import machine 
import ssd1306 
import dht 
from machine import ADC, Pin 
# --- Configuração da Conexão Wi-Fi --- 
SSID = '.............' 
PASSWORD = '.............' 
wifi_led = Pin(2, Pin.OUT) 
wifi_led.off() 
sta_if = network.WLAN(network.STA_IF) 
sta_if.active(True) 
print("Conectando ao WiFi...", end="") 
sta_if.connect(SSID, PASSWORD) 
while not sta_if.isconnected(): 
print(".", end="") 
wifi_led.off() 
time.sleep(0.25) 
wifi_led.on() 
time.sleep(0.25) 
print("\nConectado ao WiFi!") 
print("IP:", sta_if.ifconfig()[0]) 
wifi_led.on() 
# --- Configuração do Google Sheets --- 
 
SHEET_URL = 
"https://script.google.com/macros/s/AKfycbzwVuK4ErrfsXcJm9f6GNZuf5V4tuyzutQ16N4VrK8BtL
PO28c_Pe-RXyegatMqiAMcmQ/exec" 
def enviar_para_sheets(temp, umidade, limite, ac_ligado): 
    try: 
        url = f"{SHEET_URL}?temp={temp}&umidade={umidade}&limite={limite}&ac={1 if ac_ligado 
else 0}" 
        print("Enviando para Google Sheets:", url) 
        response = urequests.get(url) 
        print("Resposta:", response.text) 
        response.close() 
    except Exception as e: 
        print("Erro ao enviar para Google Sheets:", e) 
 
# --- Inicialização dos Sensores e Display OLED --- 
i2c = machine.I2C(0, scl=Pin(23), sda=Pin(21)) 
oled = ssd1306.SSD1306_I2C(128, 64, i2c) 
sensor = dht.DHT22(Pin(19)) 
pot = ADC(Pin(32)) 
pot.atten(ADC.ATTN_11DB) 
 
# --- Variáveis de Estado --- 
notificado = False 
ac_ligado = False 
tempo_ligado = 0 
 
# --- Temporização para Google Sheets --- 
 
ultimo_envio_sheets = time.ticks_ms() 
intervalo_envio_ms = 30000  # 120 segundos colocarvalor de 12000 
 
# --- Configuração do ESP Cliente --- 
esp2_ip = '192.168.135.220' 
 
# --- Configuração da Notificação via WhatsApp (CallMeBot) --- 
url_base = ( 
    
"https://api.callmebot.com/whatsapp.php?phone=5521966534578&text=%E2%9A%A0%EF%B8
%8F+Alerta+de+Temperatura%21%0ALimite%3A+{:.1f}%C2%B0C%0AAtual%3A+{:.1f}%C2%B0C%
0AUmidade%3A+{:.1f}%25%0AAC+foi+ligado.&apikey=6213947" 
) 
 
# --- Funções de Controle do Ar Condicionado --- 
def ac_esp2_ligar(): 
    try: 
        r = urequests.get(f'http://{esp2_ip}/ligar') 
        print("Status AC (LIGADO):", r.text) 
        r.close() 
    except Exception as e: 
        print("Erro ao ligar AC:", e) 
 
def ac_esp2_desligar(): 
    try: 
        r = urequests.get(f'http://{esp2_ip}/desligar') 
        print("Status AC (DESLIGADO):", r.text) 
 
        r.close() 
    except Exception as e: 
        print("Erro ao desligar AC:", e) 
 
# --- Loop Principal --- 
while True: 
    try: 
        # Leitura dos sensores 
        sensor.measure() 
        temp = sensor.temperature() 
        umidade = sensor.humidity() 
        pot_value = pot.read() 
 
        # Cálculo do limite ajustável de temperatura 
        limite_temp = 16 + (pot_value / 4095) * (30 - 16) 
        limite_temp = round(limite_temp, 1) 
 
        # Exibição no display OLED 
        oled.fill(0) 
        oled.text(f"Temp: {temp:.1f} C", 0, 0) 
        oled.text(f"Umidade: {umidade:.1f}%", 0, 20) 
        oled.text(f"Limite: {limite_temp:.1f} C", 0, 30) 
        oled.text("Ar: " + ("LIGADO" if ac_ligado else "DESLIGADO"), 0, 40) 
        oled.show() 
 
 
        # Controle do AC 
        tempo_atual = time.ticks_ms() 
 
        if temp >= limite_temp: 
            if not ac_ligado: 
                tempo_ligado = tempo_atual 
                ac_ligado = True 
                ac_esp2_ligar() 
                print(">>> AC LIGADO <<<") 
 
            if not notificado: 
                try: 
                    url_msg = url_base.format(limite_temp, temp, umidade) 
                    response = urequests.get(url_msg) 
                    print("Notificação WhatsApp enviada!") 
                    response.close() 
                    notificado = True 
                except Exception as e: 
                    print("Erro no WhatsApp:", e) 
        else: 
            if ac_ligado and time.ticks_diff(tempo_atual, tempo_ligado) >= 5000: 
                ac_ligado = False 
                ac_esp2_desligar() 
                print(">>> AC DESLIGADO <<<") 
 
 
            if notificado: 
                notificado = False 
 
        # Envio para o Google Sheets a cada 60 segundos 
        if time.ticks_diff(time.ticks_ms(), ultimo_envio_sheets) >= intervalo_envio_ms: 
            enviar_para_sheets(temp, umidade, limite_temp, ac_ligado) 
            ultimo_envio_sheets = time.ticks_ms() 
 
        # Aguarda 5 segundos antes da próxima iteração 
        time.sleep(5) 
 
    except OSError as e: 
        print("Erro no sensor:", e) 
        oled.fill(0) 
        oled.text("Erro na leitura!", 0, 0) 
        oled.show() 
        time.sleep(5)
