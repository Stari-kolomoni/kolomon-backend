from django.db import models

# *********** MAIN DATA TABLES ************ #


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"


class TranslationState(models.Model):
    state = models.CharField(max_length=50)


class Link(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)


class EnglishEntry(models.Model):
    entry = models.CharField(max_length=100)
    use_case = models.TextField()
    # NOTE: translation_state can be None, always check this value
    translation_state = models.ForeignKey(TranslationState, on_delete=models.SET_NULL, null=True, blank=True)
    translation_comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "English entries"


class Suggestion(models.Model):
    translation = models.CharField(max_length=100)
    separate_gender_form = models.BooleanField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Translation(models.Model):
    translation = models.CharField(max_length=100)
    separate_gender_form = models.BooleanField()
    description = models.TextField()
    type = models.CharField(max_length=100)
    # NOTE: translation_female can be None, always check this value
    translation_female = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Gender(models.Model):
    gender = models.CharField(max_length=50)
    # An abbreviation for gender (eg. M, F, N...)
    abbr = models.CharField(max_length=10)


class GenderVariant(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    # TODO: Is this a good idea?
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)


# *********** MANY TO MANY RELATION TABLES ************ #
# NOTE: All these have models.CASCADE on - when one object is deleted, the linking entry is deleted as well.
# The remaining entry is left without link. When this is not intended, it needs to be handled explicitly.


class RelatedEntry(models.Model):
    # TODO: Source and related entry are stupid names. Fix to imply symmetry of relation.
    source_entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE, related_name='english_entry_source')
    related_entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE, related_name='english_entry_related')
    comment = models.TextField()

    class Meta:
        verbose_name_plural = "Related entries"


class Entry2Category(models.Model):
    entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Entry2Link(models.Model):
    entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)


class Entry2Suggestion(models.Model):
    entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)


class Entry2Translation(models.Model):
    entry = models.ForeignKey(EnglishEntry, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)


class Translation2GenderVariant(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    gender_variant = models.ForeignKey(GenderVariant, on_delete=models.CASCADE)
