from machine import Pin, ADC
import time


class SoilSensor:
    def __init__(self, pin, dry_raw, wet_raw):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.dry_raw = dry_raw
        self.wet_raw = wet_raw

    def read_percent(self):
        raw = self.adc.read()
        raw = max(min(raw, self.dry_raw), self.wet_raw)
        span = self.dry_raw - self.wet_raw
        percent = (self.dry_raw - raw) / span * 100
        return round(percent, 1)


class PumpController:
    def __init__(self, pin):
        self.relay = Pin(pin, Pin.OUT)
        self.relay.value(0)
        self.last_run_end = 0

    def cooldown_remaining(self, cooldown_seconds):
        elapsed = time.time() - self.last_run_end
        return max(0, cooldown_seconds - elapsed)

    def run_for(self, seconds):
        self.relay.value(1)
        time.sleep(seconds)
        self.relay.value(0)
        self.last_run_end = time.time()
