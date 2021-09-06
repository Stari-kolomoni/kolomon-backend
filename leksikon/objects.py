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

        elif isinstance(entry, models.Translation):
            self.id = entry.pk
            self.word = entry.translation
            self.description = entry.description
            self.language = "sl"

    def __str__(self):
        return self.word + " (" + str(self.id) + "," + self.language + ")"


class Pair:

    def __init__(self, entry):
        self.slovene = None
        self.english = None
        if isinstance(entry, models.EnglishEntry):
            self.english = Word(entry)
            slovene_translations = entry.translations.all()
            if slovene_translations:
                self.slovene = Word(slovene_translations[0])

        elif isinstance(entry, models.Translation):
            self.slovene = Word(entry)

    def __str__(self):
        label = ""
        if self.slovene:
            label += self.slovene.word
        if self.english:
            label += self.english.word
        return label
