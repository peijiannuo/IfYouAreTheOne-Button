import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests
import board
import digitalio

wifi_ssid = os.getenv("WIFI_SSID", "")
wifi_password = os.getenv("WIFI_PASSWORD", "")
url = os.getenv("URL", "")
id = int(os.getenv("ID", ""))

button_1 = digitalio.DigitalInOut(board.GP10)
button_1.switch_to_input(pull=digitalio.Pull.DOWN)

button_2 = digitalio.DigitalInOut(board.GP15)
button_2.switch_to_input(pull=digitalio.Pull.DOWN)

wifi.radio.connect(wifi_ssid, wifi_password)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


def generate_query(userid, mode):
    query = f'mutation{{updateLight(userid:{userid},mode:"{mode}"){{userid mode}}}}'
    return {"query": query}


while True:
    try:
        if not button_1.value:
            response = requests.post(url, json=generate_query(id, "off"))
            print("Text Response: ", response.text)
            response.close()
            time.sleep(1)
        elif not button_2.value:
            response = requests.post(url, json=generate_query(id, "blast"))
            print("Text Response: ", response.text)
            response.close()
            time.sleep(1)
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
