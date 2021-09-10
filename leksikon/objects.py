from leksikon import models


class Pong:

    def __init__(self):
        self.message = "Pong!"


class BasicWord:

    def __init__(self, entry):
        self.id = entry.pk
        self.word = entry.entry
        self.description = entry.use_case


class ExtendedWord(BasicWord):
    def __init__(self, entry):
        super().__init__(entry)
        self.created_at = entry.created
        self.edited_at = entry.last_modified


class Word(BasicWord):

    def __init__(self, entry):
        super().__init__(entry)
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


class EnglishWord(ExtendedWord):

    def __init__(self, entry):
        super().__init__(entry)
        self.translation_state = entry.translation_state

    @staticmethod
    def object_list(queryset):
        object_list = []
        for query in queryset:
            object_list.append(EnglishWord(query))
        return object_list


class ExtendedEnglishWord(EnglishWord):

    def __init__(self, entry):
        super().__init__(entry)
        self.translation_comment = entry.translation_comment
        events = models.History.objects.filter(word=entry)
        if events:
            user = events[0].user
            self.edited_by = user.pk
        else:
            self.edited_by = -1
        self.categories = Category.object_list(entry.categories.all())
        self.links = Link.object_list(entry.links.all())
        self.suggestions = Suggestion.object_list(entry.suggestions.all())
        self.related_words = Relation.object_list(entry.related.all())

    @staticmethod
    def object_list(queryset):
        entry_list = []
        for query in queryset:
            entry_list.append(ExtendedEnglishWord(query))
        return entry_list


class SloveneWord(ExtendedWord):

    def __init__(self, entry):
        super().__init__(entry)
        self.word_female_form = entry.female_form
        self.type = entry.type
        self.related_words = Relation.object_list(entry.related.all())


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


class Category:

    def __init__(self, category):
        self.id = category.pk
        self.name = category.name
        self.description = category.description

    @staticmethod
    def object_list(queryset):
        category_list = []
        for query in queryset:
            category_list.append(Category(query))
        return category_list


class Link:

    def __init__(self, link):
        self.title = link.title
        self.url = link.link

    @staticmethod
    def object_list(queryset):
        link_list = []
        for query in queryset:
            link_list.append(Link(query))
        return link_list


class Suggestion:

    def __init__(self, suggestion):
        self.suggestion = suggestion.translation
        self.separate_gender_form = suggestion.separate_gender_form
        self.comment = suggestion.description
        self.created_at = suggestion.created
        self.edited_at = suggestion.last_modified

    @staticmethod
    def object_list(queryset):
        suggestion_list = []
        for query in queryset:
            suggestion_list.append(Suggestion(query))
        return suggestion_list


class Relation:

    def __init__(self, entry):
        self.id = entry.pk
        self.name = entry.entry

    @staticmethod
    def object_list(queryset):
        relation_list = []
        for query in queryset:
            relation_list.append(Relation(query))
        return relation_list
