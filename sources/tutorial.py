class TutorialSource:
    name = "Tutorial"

    def update(self, ttyc=None, src_changed=None):
        output = "Welcome to Dial-A-Type\n"
        output += "Please dial your selection...\n"
        n = 0
        for src in ttyc._sources[1:]:
            n += 1
            output += f"{n}: {src.name}\n"
        output += "Dial your selection on the phone at the TTY switchboard.\n\n"

        return output
