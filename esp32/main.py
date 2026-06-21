import time

import config
import wifi_manager
from sensors import SoilSensor, PumpController
from api_client import ApiClient


def current_day():
    return time.localtime()[2]


def main():
    wifi_manager.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    soil_sensor = SoilSensor(
        config.SOIL_SENSOR_PIN,
        config.MOISTURE_DRY_RAW,
        config.MOISTURE_WET_RAW,
    )
    pump = PumpController(config.PUMP_RELAY_PIN)
    api = ApiClient(config.SERVER_URL, config.API_TOKEN, config.DEVICE_UID)

    day_sum = 0.0
    day_count = 0
    tracked_day = current_day()

    while True:
        moisture_percent = soil_sensor.read_percent()

        if moisture_percent < config.MOISTURE_THRESHOLD_PERCENT:
            if pump.cooldown_remaining(config.PUMP_COOLDOWN_SECONDS) == 0:
                pump.run_for(config.PUMP_RUN_SECONDS)

        day_sum += moisture_percent
        day_count += 1

        if current_day() != tracked_day:
            avg_moisture = round(day_sum / day_count, 1)

            if not wifi_manager.is_connected():
                try:
                    wifi_manager.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
                except RuntimeError:
                    pass

            api.send_daily_average(avg_moisture)

            day_sum = 0.0
            day_count = 0
            tracked_day = current_day()

        time.sleep(config.MEASURE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
