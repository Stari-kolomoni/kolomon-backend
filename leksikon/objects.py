from leksikon import models


class Pong:

    def __init__(self):
        self.message = "Pong!"


class Word:

    def __init__(self, entry):
        self.id = entry.pk
        self.word = entry.entry
        self.description = entry.use_case
        self.language = ''
        if hasattr(entry, 'englishentry') and isinstance(entry.englishentry, models.EnglishEntry):
            self.language = 'en'
        elif hasattr(entry, 'sloveneentry') and isinstance(entry.sloveneentry, models.SloveneEntry):
            self.language = 'sl'

    def __str__(self):
        return self.word + " (" + str(self.id) + ")"


class Pair:

    def __init__(self, entry):
        self.slovene = None
        self.english = None

        word_obj = Word(entry)
        if word_obj.language == 'en':
            self.english = word_obj
            translations = entry.englishentry.translations.all()
            if translations:
                self.slovene = Word(translations[0])
        elif word_obj.language == 'sl':
            self.slovene = word_obj
            english_entries = entry.sloveneentry.englishentry_set.all()
            if english_entries:
                self.english = Word(english_entries[0])

    def check_duplicates(self, id_list):
        for word_id in id_list:
            if self.slovene.id == word_id or self.english.id == word_id:
                return True
        return False

    def __str__(self):
        label = ""
        if self.slovene:
            label += self.slovene.word + ", "
        if self.english:
            label += self.english.word
        return label
