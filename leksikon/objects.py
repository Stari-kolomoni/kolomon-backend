from leksikon import models


class Pong:

    def __init__(self):
        self.message = "Pong!"


class Word:

    def __init__(self, entry):
        if isinstance(entry, models.EnglishEntry):
            self.id = entry.pk
            self.word = entry.entry
            self.description = entry.use_case
            self.language = "en"
        if isinstance(entry, models.Translation):
            self.id = entry.pk
            self.word = entry.translation
            self.description = entry.description
            self.language = "sl"

    def __str__(self):
        return self.word + " (" + str(self.id) + "," + self.language + ")"
