import requests
from time import sleep
from decouple import config
import textwrap
import xml.etree.ElementTree as ET


class WeatherSource:
    name = "Current Weather"

    _feedUrl = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KBFI&hoursBeforeNow=1"

    _loops = 0
    _loops_max = 15
    _retry = config("RETRY_AFTER", default=10)
    _data = ""

    def update(self, src_changed=False, ttyc=None):
        self._loops += 1
        if (self._loops > self._loops_max) or src_changed:
            self._loops = 0
            try:
                ttyc.print("Fetching the latest weather...", override=True)
                req = requests.get(self._feedUrl, timeout=5)
                if not req.ok:
                    raise Exception(
                        "Weather Machine Breaky, Got status " + req.status_code
                    )

                root = ET.fromstring(req.text)

                data = textwrap.fill(root.find("./data/METAR/raw_text").text, width=70)
                data += "\n\n"

            except Exception as e:
                print(e)
                ttyc.print(
                    f"Error fetching weather :(\nRetrying in {self._retry} seconds"
                )
                for i in range(self._retry):
                    ttyc.print(".".encode("ascii"))
                    if ttyc._source_changed:
                        return ""
                    sleep(1)
                ttyc.print("\n")

                self._data = self.update()

        return self._data
