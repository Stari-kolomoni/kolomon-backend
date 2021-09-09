from django.contrib import admin
from . import models

model_set = (models.Gender, models.GenderVariant,
             models.TranslationState,
             models.Category, models.Link,
             models.Suggestion,
             models.SloveneEntry,
             models.EnglishEntry)

admin.site.register(model_set)
