from django.db import models

# *********** MAIN DATA TABLES ************ #


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class TranslationState(models.Model):
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.state


class Link(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Suggestion(models.Model):
    translation = models.CharField(max_length=100)
    separate_gender_form = models.BooleanField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.translation


class Translation(models.Model):
    translation = models.CharField(max_length=100)
    separate_gender_form = models.BooleanField()
    description = models.TextField()
    type = models.CharField(max_length=100)
    # I do not approve of this
    female_form = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.translation


class EnglishEntry(models.Model):
    entry = models.CharField(max_length=100)
    use_case = models.TextField()
    # NOTE: translation_state can be None, always check this value
    translation_state = models.ForeignKey(TranslationState, on_delete=models.SET_NULL, null=True, blank=True)
    translation_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    links = models.ManyToManyField(Link, blank=True)
    suggestions = models.ManyToManyField(Suggestion, blank=True)
    translations = models.ManyToManyField(Translation, blank=True)

    class Meta:
        verbose_name_plural = "English entries"

    def __str__(self):
        return self.entry


class RelatedEntry(models.Model):
    # TODO: Source and related entry are stupid names. Fix to imply symmetry of relation.
    source_entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE, related_name='english_entry_source')
    related_entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE, related_name='english_entry_related')
    comment = models.TextField()

    class Meta:
        verbose_name_plural = "Related entries"

    def __str__(self):
        return str(self.source_entry) + " - " + str(self.related_entry)


# These are useless now because of the stupid "female_form" attribute

class Gender(models.Model):
    gender = models.CharField(max_length=50)
    # An abbreviation for gender (eg. M, F, N...)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.gender


class GenderVariant(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    # TODO: Is this a good idea?
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.translation
