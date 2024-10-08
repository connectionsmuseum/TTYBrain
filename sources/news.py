import tty
import requests
from time import sleep
from decouple import config
import textwrap
import xml.etree.ElementTree as ET


class NewsSource:
    name = "Current News"

    # this link requests a custom RSS feed from Google which includes articles containing a URL published within the last 24 hours
    # we're using AP because the main Teletype we demo is labeled "Associated Press"
    _feedUrl = "https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en"

    _loops = 0
    _loops_max = 15
    _retry = config("RETRY_AFTER", default=10)
    _data = ""

    def update(self, src_changed=False, ttyc=None):
        self._loops += 1
        if (self._loops > self._loops_max) or src_changed:
            self._loops = 0
            try:
                ttyc.print("Fetching news from the Associated Press...\n", override=True)
                req = requests.get(self._feedUrl, timeout=5)
                if not req.ok:
                    raise Exception(
                        "News Machine Breaky, Got status " + req.status_code
                    )

                root = ET.fromstring(req.text)

                self._data = "Latest News from the Associated Press:\n"
                for item in root.findall("./channel/item"):
                    pubDate = item.find("pubDate").text
                    # truncate the last 23 characters from the title since it will always say " - The Associated Press"
                    title = textwrap.fill(item.find("title").text[:-23], width=70)

                    self._data += f"{pubDate}\n{title}\n\n"

            except Exception as e:
                print(e)
                ttyc.print(f"Error fetching news :(\nRetrying in {self._retry} seconds")
                for i in range(self._retry):
                    ttyc.print(".".encode("ascii"))
                    if ttyc._source_changed:
                        return ""
                    sleep(1)
                ttyc.print("\n")

                self._data = self.update()

        return self._data
