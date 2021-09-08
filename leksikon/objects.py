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

    @staticmethod
    def object_list(queryset):
        object_list = []
        for query in queryset:
            object_list.append(Word(query))
        return object_list

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

    @staticmethod
    def object_list(queryset):
        object_list = []
        id_list = []
        for query in queryset:
            query_obj = Pair(query)
            if not query_obj.check_duplicates(id_list):
                object_list.append(query_obj)
                if query_obj.slovene:
                    id_list.append(query_obj.slovene.id)
                if query_obj.english:
                    id_list.append(query_obj.english.id)
        return object_list

    def __str__(self):
        label = ""
        if self.slovene:
            label += self.slovene.word + ", "
        if self.english:
            label += self.english.word
        return label


class EnglishWord:

    def __init__(self, entry: models.EnglishEntry):
        self.id = entry.pk
        self.word = entry.entry
        self.description = entry.use_case
        self.translation_state = entry.translation_state
        self.created_at = entry.created
        self.edited_at = entry.last_modified

    @staticmethod
    def object_list(queryset):
        object_list = []
        for query in queryset:
            object_list.append(EnglishWord(query))
        return object_list
