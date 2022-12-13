from datetime import datetime
import requests
from time import sleep
from decouple import config
import textwrap
import xml.etree.ElementTree as ET

language = "en"
d_type = "selected"
today = datetime.now()


class HistorySource:
    name = "Today In History"

    _feedUrl = f"https://api.wikimedia.org/feed/v1/wikipedia/{language}/onthisday/{d_type}/{today.month:0>2}/{today.day:0>2}"

    _loops = 0
    _loops_max = 15
    _retry = config("RETRY_AFTER", default=10)
    _data = ""

    def update(self, src_changed=False, ttyc=None):
        self._loops += 1
        if (self._loops > self._loops_max) or src_changed:
            self._loops = 0
            try:
                ttyc.print("Fetching On This Day from Wikimedia...\n", override=True)
                req = requests.get(self._feedUrl, timeout=5)
                if not req.ok:
                    raise Exception(
                        "History Machine Breaky, Got status " + req.status_code
                    )

                root = req.json()
                self._data = ""
                for element in root[d_type]:
                    year = element["year"]
                    headline = textwrap.fill(element["text"], width=70)
                    self._data += f"{today:%d %b} {year}\n{headline}\n\n"

            except Exception as e:
                print(e)
                ttyc.print(
                    f"Error fetching history :(\nRetrying in {self._retry} seconds"
                )
                for i in range(self._retry):
                    ttyc.print(".".encode("ascii"))
                    if ttyc._source_changed:
                        return ""
                    sleep(1)
                ttyc.print("\n")

                self._data = self.update()

        return self._data
