import urequests
import time


class ApiClient:
    def __init__(self, base_url, token, device_uid):
        self.base_url = base_url
        self.token = token
        self.device_uid = device_uid

    def send_daily_average(self, avg_moisture):
        t = time.localtime()
        date_str = "{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2])

        body = {
            "device_uid": self.device_uid,
            "date": date_str,
            "avg_moisture": avg_moisture,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }

        response = None
        try:
            response = urequests.post(self.base_url + "/api/v1/daily-moisture", json=body, headers=headers)
            return response.status_code
        except OSError:
            return None
        finally:
            if response is not None:
                response.close()
