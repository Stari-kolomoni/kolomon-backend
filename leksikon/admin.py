from django.contrib import admin
from . import models

model_set = (models.Gender, models.GenderVariant,
             models.TranslationState,
             models.EnglishEntry, models.RelatedEntry,
             models.Category, models.Link,
             models.Suggestion,
             models.Translation)

admin.site.register(model_set)
