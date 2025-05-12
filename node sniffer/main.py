from network import LoRa
import socket
import time
import ubinascii

# Initializing in LoRa mode
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# socket LoRa
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

# Vector of SF ranging from 7 to 12 (more SF can be tried)
spreading_factors = [7]

# Timeout for each SF in seconds
listen_time = 20000

print("LoRa sniffer started...")

while True:
    for sf in spreading_factors:
        print("\n[+] Setting SF: {}".format(sf))

        # Configura il modem LoRa con lo SF attuale
        lora.init(mode=LoRa.LORA,
                  region=LoRa.EU868,
                  sf=sf,
                  bandwidth=LoRa.BW_125KHZ,
                  coding_rate=LoRa.CODING_4_5,
                  preamble=8,
                  tx_iq=False)

        start_time = time.time()
        while time.time() - start_time < listen_time:
            data = s.recv(256)
            if data:
                print("[PKT][SF{}][{} B] {}".format(
                    sf, len(data), ubinascii.hexlify(data)))
            time.sleep(0.1)  # Per non saturare la CPU
