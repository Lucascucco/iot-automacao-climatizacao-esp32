import network 
import socket 
import machine 
import time 
# --- Configuração Wi-Fi --- 
SSID = '...............' 
PASSWORD = '...............' 
# Configuração do LED de status Wi-Fi 
wifi_led = machine.Pin(2, machine.Pin.OUT)  # LED no pino D2 (GPIO 2) 
wifi_led.off()  # Inicia desligado 
sta_if = network.WLAN(network.STA_IF) 
sta_if.active(True) 
print("Conectando ao WiFi...", end="") 
sta_if.connect(SSID, PASSWORD) 
# Tenta conectar e pisca o LED enquanto espera 
while not sta_if.isconnected(): 
print(".", end="") 
wifi_led.off()  # Pisca LED 
time.sleep(0.25) 
wifi_led.on() 
time.sleep(0.25) 
# Conexão estabelecida 
print("\nConectado ao WiFi!") 
print("IP:", sta_if.ifconfig()[0]) 
wifi_led.on()  # Mantém LED aceso indicando conexão 
# --- Inicializa atuador, simular o controle do AC --- 
led = machine.Pin(4, machine.Pin.OUT) 
led.off()  # Começa desligado 
# --- Configuração do Servidor HTTP --- 
# Cria o servidor escutando na porta 80 
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] 
s = socket.socket() 
s.bind(addr) 
s.listen(1) 
print('Servidor HTTP aguardando conexões...') 
# --- Loop Principal do Servidor --- 
while True: 
# Aceita conexão de cliente 
cl, addr = s.accept() 
print('Cliente conectado de', addr) 
 
    request = cl.recv(1024)  # Recebe requisição HTTP 
    request = str(request) 
    print('Requisição:', request) 
 
    # Processa comandos recebidos via URL 
    if '/ligar' in request: 
        led.value(1)  # Liga atuador 
        response = 'Ligado' 
        print('LED Ligado') 
    elif '/desligar' in request: 
        led.value(0)  # Desliga atuador 
        response = 'Desligado' 
        print('LED Desligado') 
    else: 
        response = 'Comando desconhecido' 
        print('Comando desconhecido') 
 
    # Responde ao cliente HTTP 
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n') 
    cl.send(response) 
    cl.close() 
