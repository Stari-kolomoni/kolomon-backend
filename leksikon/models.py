from django.contrib.auth.models import User
from django.db import models



class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

# *********** MAIN DATA TABLES ************ #


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class TranslationState(BaseModel):
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.state


class Link(BaseModel):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Suggestion(BaseModel):
    translation = models.CharField(max_length=100)
    separate_gender_form = models.BooleanField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.translation


class Word(BaseModel):
    entry = models.CharField(max_length=100)
    use_case = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def mark_event(self, event_type, user, date):
        instance = History(word=self,
                           user=user,
                           type=event_type,
                           date=date)
        instance.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        super().save(force_insert, force_update, using, update_fields)
        print("Hrani!")


class SloveneEntry(Word):
    separate_gender_form = models.BooleanField()
    type = models.CharField(max_length=100)
    # I do not approve of this
    female_form = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Slovene entries"

    def __str__(self):
        return self.entry


class EnglishEntry(Word):
    # NOTE: translation_state can be None, always check this value
    translation_state = models.ForeignKey(TranslationState, on_delete=models.SET_NULL, null=True, blank=True)
    translation_comment = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    links = models.ManyToManyField(Link, blank=True)
    suggestions = models.ManyToManyField(Suggestion, blank=True)
    translations = models.ManyToManyField(SloveneEntry, blank=True)
    related = models.ManyToManyField('EnglishEntry', blank=True)

    class Meta:
        verbose_name_plural = "English entries"

    def __str__(self):
        return self.entry


class History(BaseModel):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100)
    date = models.DateTimeField()


# These are useless now because of the stupid "female_form" attribute

class Gender(BaseModel):
    gender = models.CharField(max_length=50)
    # An abbreviation for gender (eg. M, F, N...)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.gender


class GenderVariant(BaseModel):
    translation = models.ForeignKey(SloveneEntry, on_delete=models.CASCADE)
    # TODO: Is this a good idea?
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.translation
