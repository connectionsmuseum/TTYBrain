import os
import random


class ArtSource:
    name = "Baudot Art"

    def update(self, ttyc=None, src_changed=None):
        data = ""
        files = list(filter(lambda f: f.lower().endswith(".txt"), os.listdir("./art")))
        choice = random.choice(files)
        print(choice)
        with open("./art/" + choice, "r") as myfile:
            for line in myfile.readlines():
                data += line.rstrip() + "\n"
        return data
