import network
import time


def connect(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                raise RuntimeError("WiFi kapcsolat sikertelen")
            time.sleep(0.5)

    return wlan.ifconfig()


def is_connected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()
